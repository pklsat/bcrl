import argparse
import json
from pathlib import Path
from datetime import datetime
import time
from typing import Dict, List


class DummyResponseGenerator:
    def __init__(self, response_dir: Path):
        self.response_dir = response_dir
        self.response_dir.mkdir(parents=True, exist_ok=True)

    def generate_schedule(self) -> List[Dict]:
        return [
            {"hour": 0, "minute": 0, "soc": 65.3},
            {"hour": 1, "minute": 0, "soc": 66.1},
            {"hour": 2, "minute": 0, "soc": 67.5},
            {"hour": 3, "minute": 0, "soc": 68.2},
        ]

    def generate_metadata(self, request_soc: float) -> Dict:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "request_soc": request_soc,
            "request_date": now,
            "generated_at": now,
            "message": "Generated successfully",
        }

    def generate_response(self, req_id: str) -> Dict:
        request_soc = 65.3  # デモ用の固定値（将来パラメータ化も可能）
        schedule = self.generate_schedule()
        metadata = self.generate_metadata(request_soc)
        return {
            "api": "soc",
            "req_id": req_id,
            "message": "success",
            "soc_response": {
                "schedule": schedule,
                "metadata": metadata,
            },
        }

    def save_response(self, req_id: str):
        response_data = self.generate_response(req_id)
        file_path = self.response_dir / f"{req_id}.json"

        if file_path.exists():
            print(f"[MAIN] [INFO] Response file {file_path} already exists.")
            return

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4, ensure_ascii=False)
        print(f"[MAIN] [INFO] Response data saved to {file_path}")

    def run(self, req_id: str):
        print(f"[MAIN] [INFO] Processing req_id: {req_id}")
        time.sleep(30)  # Simulate processing time
        self.save_response(req_id)
        print(f"[MAIN] [INFO] Job {req_id} completed.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("req_id", type=str, help="Request ID")
    parser.add_argument(
        "--response-dir",
        type=Path,
        default=Path("/shared/bcrlapi/response/"),
        help="Directory to save response JSON",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    generator = DummyResponseGenerator(response_dir=args.response_dir)
    generator.run(args.req_id)


if __name__ == "__main__":
    main()
