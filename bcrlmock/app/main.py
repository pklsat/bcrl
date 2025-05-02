import json
from pathlib import Path
import sys
from datetime import datetime
import status_monitor
import time

REPONSE_DIR = Path("/shared/bcrlapi/response/")
SIMULATION_INTERVAL_SECONDS = 30  # sec

def generate_dummy_data() -> dict:
    schedule = [
        {"hour": 0, "minute": 0, "SoC": 50.0},
        {"hour": 0, "minute": 30, "SoC": 50.1},
        {"hour": 1, "minute": 0, "SoC": 50.2},
        {"hour": 1, "minute": 30, "SoC": 50.3},
        {"hour": 23, "minute": 0, "SoC": 54.6},
        {"hour": 23, "minute": 30, "SoC": 54.7}
    ]

    metadata = {
        "request_soc": 65.3,
        "request_date": "9/1 0:30",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Success"
    }

    return {
        "schedule": schedule,
        "metadata": metadata
    }

def create_response(req_id: str):
    response_data = generate_dummy_data()
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
    status_monitor.update_status(req_id, "completed")
    print(f"[MAIN] [INFO] Job {req_id} completed.")
    return None

if __name__ == "__main__":
    main()
