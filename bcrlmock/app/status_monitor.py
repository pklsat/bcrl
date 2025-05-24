import json
import time
import subprocess
import traceback
import sys
import argparse
from typing import Dict, List


class StatusManager:
    def __init__(self, status_file: str):
        self.status_file = status_file

    def load(self) -> Dict:
        """Load the status JSON from file."""
        try:
            with open(self.status_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"jobs": {}}
        if "jobs" not in data:
            data["jobs"] = {}
        return data

    def save(self, data: Dict):
        """Save the status JSON to file."""
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def find_jobs(self, data: Dict, key: str, value: str) -> List[str]:
        """Find job req_ids matching given key/value pair."""
        return [
            req_id
            for req_id, job in data.get("jobs", {}).items()
            if isinstance(job, dict) and job.get(key) == value
        ]

    def update_status(self, data: Dict, req_id: str, status: str) -> bool:
        """Update status of a given job and save."""
        if req_id in data.get("jobs", {}):
            data["jobs"][req_id]["status"] = status
            self.save(data)
            print(f"[MONITOR] [INFO] Updated status for req_id: {req_id} to {status}")
            return True
        else:
            print(f"[MONITOR] [WARN] No job found for req_id: {req_id}")
            return False


class JobRunner:
    def __init__(self, main_script: str, status_manager: StatusManager):
        self.main_script = main_script
        self.status_manager = status_manager

    def run(self, req_id: str):
        """Run the main script for the given job and update its status."""
        try:
            subprocess.run(
                ["python", self.main_script, req_id],
                check=True
            )
            status_data = self.status_manager.load()
            self.status_manager.update_status(status_data, req_id, "Completed")
            print(f"[MONITOR] [INFO] Job {req_id} completed.")
        except subprocess.CalledProcessError as e:
            print(f"[MONITOR] [ERROR] Failed to run script for job {req_id}: {e}")
            raise


class JobMonitor:
    def __init__(self, interval: int, status_manager: StatusManager, job_runner: JobRunner):
        self.interval = interval
        self.status_manager = status_manager
        self.job_runner = job_runner

    def start(self):
        """Start the monitoring loop."""
        while True:
            try:
                status_data = self.status_manager.load()
                pending_jobs = self.status_manager.find_jobs(status_data, "status", "Pending")

                if not pending_jobs:
                    print(f"[MONITOR] [INFO] No pending jobs. Rechecking in {self.interval} seconds.")
                    time.sleep(self.interval)
                    continue

                req_id = pending_jobs[0]
                self.status_manager.update_status(status_data, req_id, "Processing")
                self.job_runner.run(req_id)

            except Exception as e:
                print(f"[MONITOR] [ERROR] {e}")
                traceback.print_exc()
                sys.exit(1)

            time.sleep(self.interval)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("interval", type=int, help="Interval (in seconds) between checks.")
    parser.add_argument("--status-file", default="/shared/bcrlapi/request/status.json", help="Path to status JSON.")
    parser.add_argument("--main-script", default="/bcrlmock/app/main.py", help="Main script to execute.")
    return parser.parse_args()


def main():
    args = parse_args()

    status_manager = StatusManager(args.status_file)
    job_runner = JobRunner(args.main_script, status_manager)
    monitor = JobMonitor(args.interval, status_manager, job_runner)

    monitor.start()


if __name__ == "__main__":
    main()
