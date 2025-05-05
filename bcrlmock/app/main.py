import argparse
import json
from pathlib import Path
from datetime import datetime
import time

REPONSE_DIR = Path("/shared/bcrlapi/response/")
SIMULATION_INTERVAL_SECONDS = 30  # sec


def generate_dummy_data(req_id: str) -> dict:
    schedule = [
        {"hour": 0, "minute": 0, "soc": 65.3},
        {"hour": 1, "minute": 0, "soc": 66.1},
        {"hour": 2, "minute": 0, "soc": 67.5},
        {"hour": 3, "minute": 0, "soc": 68.2},
    ]
    metadata = {
        "request_soc": 65.3,
        "request_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "Generated successfully",
    }
    soc_response = {"schedule": schedule, "metadata": metadata}
    response = {
        "api": "soc",
        "req_id": req_id,
        "message": "success",
        "soc_response": soc_response,
    }
    return response


def create_response(req_id: str):
    response_data = generate_dummy_data(req_id)
    response_file_path = REPONSE_DIR / f"{str(req_id)}.json"
    if response_file_path.exists():
        print(f"[MAIN] [INFO] Response file {response_file_path} already exists.")
        return
    with open(response_file_path, "w", encoding="utf-8") as f:
        json.dump(response_data, f, indent=4, ensure_ascii=False)
    print(f"[MAIN] [INFO] Response data saved to {response_file_path}")


def mock(args):
    print(f"[MAIN] [INFO] Processing req_id: {args.req_id}")
    time.sleep(args.main_interval)
    create_response(args.req_id)
    print(f"[MAIN] [INFO] Job {args.req_id} Completed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argment("req_id", type=str, help="Request ID")
    parser.add_argument("main_interval", type=int, help="Main interval in seconds")
    args = parser.parse_args()

    mock(args)


if __name__ == "__main__":
    main()
