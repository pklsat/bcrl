import json
import uuid
from typing import List
from fastapi import FastAPI, Body, HTTPException
from pathlib import Path
from datetime import datetime

from app.models import JobResponse, JobStatusResponse
from app.models import SocRequest, Response

app = FastAPI()

status_path = Path("/shared/bcrlapi/request/status.json")


@app.get("/jobs/", response_model=List[JobStatusResponse])
def get_job_list():
    with open(status_path, "r") as f:
        status_dict = json.load(f)
    job_list = []
    for job in status_dict["jobs"]:
        job_list.append(
            JobStatusResponse(
                req_id=job["req_id"],
                api=job["api"],
                status=job["status"],
                req_date=job["req_date"],
            )
        )
    return job_list


def add_new_job(req_id: uuid.UUID, api: str):
    newjob = {
        "req_id": req_id,
        "api": api,
        "status": "Pending",
        "req_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        with open(status_path, "r", encoding="utf-8") as f:
            status_data = json.load(f)
    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ):  # ファイルがない、または読み込みエラーの場合
        status_data = {"jobs": []}  # 初期化
    if "jobs" not in status_data:
        status_data["jobs"] = []
    status_data["jobs"].append(newjob)
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=4)


@app.post("/submit/", response_model=JobResponse)
def submit_soc(req: SocRequest = Body(...)):
    req_dict = req.dict()
    req_json = json.dumps(req_dict)
    req_id = str(uuid.uuid4())
    req_path = "/shared/bcrlapi/request/" + req_id + ".json"
    with open(req_path, "w") as f:
        json.dump(req_json, f, indent=4)
    add_new_job(req_id, req.api)
    return JobResponse(message="Job submitted successfully", req_id=req_id)


@app.get("/jobs/status/{req_id}", response_model=JobStatusResponse)
def get_job_status(req_id: str):
    with open(status_path, "r") as f:
        status_dict = json.load(f)
    for job in status_dict["jobs"]:  # TODO: ここを関数化する
        if job["req_id"] == req_id:
            msg = job["status"]
            api = job["api"]
            break
    else:
        api = ""
        msg = "not found"
    return JobStatusResponse(
        req_id=req_id, api=api, status=msg, req_date=job["req_date"]
    )


@app.get("/jobs/results/{req_id}", response_model=Response)
def get_job_result(req_id: str):
    path = Path("/shared/bcrlapi/response/" + req_id + ".json")
    if not path.exists():
        raise HTTPException(
            status_code=404, detail="Result not found for req_id: " + req_id
        )
    with open(path, "r") as f:
        res = json.load(f)
    return Response(**res)


@app.get("/jobs/delete/{req_id}", response_model=JobResponse)
def delete_job(req_id: str):
    with open(status_path, "r") as f:
        status_dict = json.load(f)
    for job in status_dict["jobs"]:
        if job["req_id"] == req_id:
            status_dict["jobs"].remove(job)
            break
    else:
        raise HTTPException(status_code=404, detail="Job not found")
    with open(status_path, "w") as f:
        json.dump(status_dict, f, ensure_ascii=False, indent=4)
    return JobResponse(message="Job deleted successfully", req_id=req_id)
