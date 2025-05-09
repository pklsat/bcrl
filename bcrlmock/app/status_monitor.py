import json
import time
import subprocess
import traceback
import sys
import argparse

STATUS_FILE = "/shared/bcrlapi/request/status.json"
MAIN_SCRIPT = "/bcrlmock/app/main.py"


def load_status() -> dict:
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status_data = json.load(f)
    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ):  # ファイルがない、または読み込みエラーの場合
        status_data = {"jobs": {}}  # 初期化
    if "jobs" not in status_data:
        status_data["jobs"] = {}
    return status_data


def save_status(status_data):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)


# jobsのkeyとvalueを指定してstatus.jsonの中から該当するjobのindexリストを取得
def find_jobs(status_json, key, value) -> list:
    job_index_list = []
    # jobsは辞書型でreq_idをキーにしてjobデータが格納されていることを確認
    for req_id, job in status_json["jobs"].items():
        if isinstance(job, dict) and job.get(key) == value:  # jobが辞書型であることを確認
            job_index_list.append(req_id)  # req_idをリストに追加
    return job_index_list


# status.jsonの中のjobのstatusを更新する
def update_status(req_id: str, status: str):
    status_json = load_status()
    job_index_list = find_jobs(status_json, "req_id", req_id)
    if job_index_list:
        status_json["jobs"][req_id]["status"] = status
        save_status(status_json)
        print(f"[MONITOR] [INFO] Updated status for req_id: {req_id} to {status}")
    else:
        print(f"[MONITOR] [INFO] No job found for req_id: {req_id}")
    return


def monitor_jobs(check_interval_seconds):
    while True:
        try:
            status_json = load_status()
            job_index_list = find_jobs(status_json, "status", "Pending")
            if not job_index_list:
                print(
                    f"[MONITOR] [INFO] Monitoring... Rechecking in {check_interval_seconds} seconds."
                )
                time.sleep(check_interval_seconds)
                continue
            # 一番上のPending jobに対して処理する
            req_id = job_index_list[0]
            status_json["jobs"][req_id]["status"] = "Processing"
            print(f"[MONITOR] [INFO] Updated status for req_id: {req_id} to Processing")
            save_status(status_json)
            # メインスクリプトを実行し完了を待つ
            subprocess.run(["python", MAIN_SCRIPT, req_id, str(check_interval_seconds)], check=True)
            update_status(req_id, "Completed")
            print(f"[MONITOR] [INFO] Job {req_id} completed.")
            time.sleep(check_interval_seconds)
        except Exception as e:
            print(f"[MONITOR] [ERROR] Error: {e}")
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "interval", type=int, help="Interval in seconds to check for new jobs."
    )
    args = parser.parse_args()
    monitor_jobs(args.interval)


if __name__ == "__main__":
    main()
