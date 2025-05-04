import json
from pathlib import Path
import sys
from datetime import datetime
import status_monitor
import time

REPONSE_DIR = Path("/shared/bcrlapi/response/")
SIMULATION_INTERVAL_SECONDS = 30  # sec

def generate_dummy_data(req_id:str) -> dict:
    schedule= [
        {"hour": 0, "minute": 0, "soc": 65.3},
        {"hour": 1, "minute": 0, "soc": 66.1},
        {"hour": 2, "minute": 0, "soc": 67.5},
        {"hour": 3, "minute": 0, "soc": 68.2}
    ]
    metadata = {
        "request_soc": 65.3,
        "request_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Generated successfully"
    }
    soc_response = {
        "schedule": schedule,
        "metadata": metadata
    }
    return {
        "api": "soc",
        "req_id": req_id,
        "message": "success",
        "soc_response": soc_response
    }

def create_response(req_id: str):
    response_data = generate_dummy_data(req_id)
    response_file_path = REPONSE_DIR / f"{str(req_id)}.json"
    if response_file_path.exists(): 
        print(f"[MAIN] [INFO] Response file {response_file_path} already exists.")
        return
    with open(response_file_path, "w", encoding="utf-8") as f:
        json.dump(response_data, f, indent=4, ensure_ascii=False)
    print(f"[MAIN] [INFO] Response data saved to {response_file_path}")

def main():
    if len(sys.argv) != 2:
        print("[MAIN] [ERROR] A UUID is required as an argument.")
        sys.exit(1)

    try:
        req_id = sys.argv[1]
    except ValueError:
        print("[MAIN] [ERROR] Invalid UUID format.")
        sys.exit(1)
    
    print(f"[MAIN] [INFO] Processing req_id: {req_id}")
    time.sleep(SIMULATION_INTERVAL_SECONDS)
    create_response(req_id)
    status_monitor.update_status(req_id, "Completed")
    print(f"[MAIN] [INFO] Job {req_id} Completed.")
    return None

if __name__ == "__main__":
    main()
