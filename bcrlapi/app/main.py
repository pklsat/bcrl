import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict

from fastapi import FastAPI, Body, HTTPException

from app.models import (
    JobResponse,
    JobStatus,
    JobStatusResponse,
    SocRequest,
    Response,
)

app = FastAPI()
status_path = Path("/shared/bcrlapi/request/status.json")


def load_status_json() -> Dict[str, Dict]:
    if not status_path.exists():
        return {"jobs": {}}
    try:
        with open(status_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"jobs": {}}


def save_status_json(status_data: Dict[str, Dict]):
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)


@app.get("/jobs", response_model=JobStatusResponse)
def get_job_list():
    status_data = load_status_json()
    jobs_dict = {
        uuid.UUID(req_id): JobStatus(**job)
        for req_id, job in status_data.get("jobs", {}).items()
    }
    return JobStatusResponse(jobs=jobs_dict)


def add_new_job(req_id: uuid.UUID, api: str):
    status_data = load_status_json()
    job = {
        "req_id": str(req_id),
        "api": api,
        "status": "Pending",
        "req_date": datetime.now().isoformat(),
    }
    status_data.setdefault("jobs", {})[str(req_id)] = job
    save_status_json(status_data)


@app.post("/submit", response_model=JobResponse)
def submit_soc(req: SocRequest = Body(...)):
    req_id = uuid.uuid4()
    req_path = Path(f"/shared/bcrlapi/request/{req_id}.json")
    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(req.dict(), f, indent=4, ensure_ascii=False)
    add_new_job(req_id, req.api)
    return JobResponse(message="Job submitted successfully", req_id=req_id)


@app.get("/jobs/status/{req_id}", response_model=JobStatus)
def get_job_status(req_id: uuid.UUID):
    status_data = load_status_json()
    job = status_data.get("jobs", {}).get(str(req_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(**job)


@app.get("/jobs/results/{req_id}", response_model=Response)
def get_job_result(req_id: uuid.UUID):
    path = Path(f"/shared/bcrlapi/response/{req_id}.json")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Result not found for req_id")
    with open(path, "r", encoding="utf-8") as f:
        res = json.load(f)
    return Response(**res)


@app.delete("/jobs/delete/{req_id}", response_model=JobResponse)
def delete_job(req_id: uuid.UUID):
    status_data = load_status_json()
    job = status_data.get("jobs", {}).get(str(req_id))
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # ジョブがProcessing中やCompletedの場合、その結果ファイルも削除する
    job_status = job.get("status")
    result_path = Path(f"/shared/bcrlapi/response/{req_id}.json")
    
    if job_status in ["Processing", "Completed"] and result_path.exists():
        result_path.unlink()  # 結果ファイルを削除
        
    # ジョブをstatus.jsonから削除
    del status_data["jobs"][str(req_id)]
    save_status_json(status_data)

    return JobResponse(message="Job deleted successfully", req_id=req_id)
