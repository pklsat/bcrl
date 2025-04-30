from fastapi import FastAPI, Body
import json
from pathlib import Path
import uuid
from datetime import datetime

from app.models import JobSubmitResponse, JobStatusResponse
from app.models import SocRequest, SocResponse

app = FastAPI()

status_path = Path("/shared/bcrlapi/request/status.json")

def add_new_job(req_id: str, api: str):
    newjob = {
        "req_id": req_id,
        "api": api,
        "status": "running",
        "request_date": datetime.now().isoformat()
    }
    with open(status_path, "r") as f:
        status_dict = json.load(f)
    status_dict["jobs"].append(newjob)
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status_dict, f, ensure_ascii=False, indent=4)


@app.post("/submit/", response_model=JobSubmitResponse)
def submit_soc(req: SocRequest = Body(...)):
    req_dict = req.dict()
    req_json = json.dumps(req_dict)
    req_id = str(uuid.uuid4())
    req_path = "/shared/bcrlapi/request/" + req_id + ".json"
    with open(req_path, "w") as f:
        json.dump(req_json, f, indent=4)
    add_new_job(req_id, req.api)
    return JobSubmitResponse(
        api=req.api, message="Job submitted successfully", req_id=req_id
    )


@app.post("/jobs/status/{req_id}", response_model=JobStatusResponse)
def get_soc_status(req_id: str):
    with open(status_path, "r") as f:
        status_dict = json.load(f)
    for job in status_dict["jobs"]:
        if job["req_id"] == req_id:
            msg = job["status"]
            api = job["api"]
            break
    else:
        api = ""
        msg = "not found"
    return JobStatusResponse(req_id=req_id, api=api, status=msg)


@app.post("/jobs/results/{req_id}", response_model=SocResponse)
def get_soc_result(req_id: str):
    path = Path("/shared/bcrlapi/response/" + req_id + ".json")
    with open(path, "r") as f:
        res = json.load(f)
    return SocResponse(**res)
