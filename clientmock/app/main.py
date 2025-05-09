import requests
import json
import time
import sys
import os
import argparse

baseurl = "http://bcrlapi:80/"
request_data_path = "./request_data.json"


class Sequence:
    req_id = None

    def __init__(self):
        self.step_data = None
        self.req_body = None
        self.status = None

    def post_submit_soc(self) -> requests.Response:
        url = baseurl + "submit/"
        response = requests.post(url, json=self.req_body)
        if response.ok:
            print("post_submit_soc was successful.")
            print("Response content:", response.text)
            Sequence.req_id = response.json()["req_id"]
            return response
        else:
            print("Request failed with status code:", response.status_code)

    def get_job_status(self) -> requests.Response:
        url = baseurl + "jobs/status/" + Sequence.req_id
        response = requests.get(url)
        if response.ok:
            self.status = response.json()["status"]
            print("get_job_status was successful.")
            print(f"Job status: {self.status}")
            print("Response content:", response.text)
            return response
        else:
            print("Request failed with status code:", response.status_code)

    def get_job_result(self) -> requests.Response:
        url = baseurl + "jobs/results/" + Sequence.req_id
        response = requests.get(url)
        if response.ok:
            print("get_job_result was successful.")
            print("Response content:", response.text)
            return response
        else:
            print("Request failed with status code:", response.status_code)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def api_handler(step) -> requests.Response:
    api_list = {
        "post_submit_soc": step.post_submit_soc,
        "get_job_status": step.get_job_status,
        "get_job_result": step.get_job_result,
    }
    api = api_list[step.step_data["api_name"]]
    if api:
        return api()
    else:
        print("API execution failed.")


def run_sequence(sequence_path) -> None:
    seq_data = load_json(sequence_path)
    req_data = load_json(request_data_path)
    for step_dict in seq_data["sequence"]:
        step = Sequence()
        step.step_data = step_dict
        step.req_body = req_data.get(step_dict["req_body"], {})
        time.sleep(step_dict["interval"])
        print(f"★Executing API: {step_dict['api_name']}")
        api_handler(step)
    print("All APIs executed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sequence_file", type=str, help="Path to the sequence file.")
    args = parser.parse_args()

    if not os.path.isfile(args.sequence_file):
        print(f"Not found '{args.sequence_file}'", file=sys.stderr)
        sys.exit(1)

    run_sequence(args.sequence_file)


if __name__ == "__main__":
    main()
