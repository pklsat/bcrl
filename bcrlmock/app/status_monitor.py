import json
import time
import subprocess
import traceback
import sys

STATUS_FILE = "/shared/bcrlapi/request/status.json"
MAIN_SCRIPT = "/bcrlmock/app/main.py"

CHECK_INTERVAL_SECONDS = 10 #sec

# status.jsonを読み込みjobsを取得
def load_status()-> dict:
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # ファイルがない、または読み込みエラーの場合
        status_data = {"jobs": []}  # 初期化
    if "jobs" not in status_data:
        status_data["jobs"] = []
    return status_data

# jobsのkeyとvalueを指定してstatus.jsonの中から該当するjobのindexリストを取得
def find_jobs(status_json, key, value) -> list:
    job_index_list = []
    for i, job in enumerate(status_json["jobs"]):
        if job.get(key) == value:
            job_index_list.append(i)
    return job_index_list

# status.jsonに書き込む
def save_status(status_data):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)

# status.jsonの中のjobのstatusを更新する
def update_status(req_id: str, status: str):
    status_json = load_status()
    job_index_list = find_jobs(status_json, "req_id", req_id)
    if job_index_list:
        status_json["jobs"][job_index_list[0]]["status"] = status
        save_status(status_json)
        print(f"[MONITOR] [INFO] Updated status for req_id: {req_id} to {status}")
    else:
        print(f"[MONITOR] [INFO] No job found for req_id: {req_id}")
    return

def monitor_jobs():
    while True:
        try:
            status_json = load_status()
            job_index_list = find_jobs(status_json, "status", "pending")
            if not job_index_list:
                print(f"[MONITOR] [INFO] Monitoring... Rechecking in {CHECK_INTERVAL_SECONDS} seconds.")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue
            status_json["jobs"][job_index_list[0]]["status"] = "Processing"
            req_id = status_json["jobs"][job_index_list[0]]["req_id"]
            # status更新
            print(f"[MONITOR] [INFO] Updated status for req_id: {req_id} to Processing")
            save_status(status_json)
            # main.pyを実行
            subprocess.run(["python", MAIN_SCRIPT, req_id], check=True)
            # main.pyの実行が成功したらstatusをcompletedに更新
            update_status(req_id, "completed")
            print(f"[MONITOR] [INFO] Job {req_id} completed.")
            time.sleep(CHECK_INTERVAL_SECONDS)
        except Exception as e:
            print(f"[MONITOR] [ERROR] Error: {e}")
            traceback.print_exc()
            sys.exit(1)

# mainloop
def main():
    monitor_jobs()
        
if __name__ == "__main__":
    main()
