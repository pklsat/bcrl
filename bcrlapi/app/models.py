from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID as uuid


# Job API(Common)
class JobResponse(BaseModel):
    req_id: uuid = None
    message: str = None


class JobStatus(BaseModel):
    req_id: uuid = None
    api: str = None
    status: str = None
    req_date: str = None

class JobStatusResponse(BaseModel):
    jobs: Dict[uuid, JobStatus] = None

# SOC API
class SocRequest(BaseModel):
    api: str = None
    current_soc: float = None
    year: int = None
    month: int = None
    day: int = None
    hour: int = None
    minute: int = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "api": "soc",
                    "current_soc": 65.3,
                    "year": 2022,
                    "month": 9,
                    "day": 1,
                    "hour": 0,
                    "minute": 30,
                }
            ]
        }
    }


class SocSchedule(BaseModel):
    hour: int = None
    minute: int = None
    soc: float = None


class SocMetadata(BaseModel):
    request_soc: float = None
    request_date: str = None
    generated_at: str = None
    message: str = None


class SocResponse(BaseModel):
    schedule: List[SocSchedule] = None
    metadata: SocMetadata = None


class Response(BaseModel):
    api: str = None
    req_id: uuid = None
    message: str = None
    soc_response: SocResponse = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "api": "soc",
                    "req_id": "123e4567-e89b-12d3-a456-426614174000",
                    "message": "Success",
                    "soc_response": {
                        "schedule": [
                            {"hour": 0, "minute": 30, "soc": 65.3},
                            {"hour": 1, "minute": 0, "soc": 66.0},
                        ],
                        "metadata": {
                            "request_soc": 65.3,
                            "request_date": "2023-09-01T00:30:00Z",
                            "generated_at": "2023-09-01T01:00:00Z",
                            "message": "Generated successfully",
                        },
                    },
                }
            ]
        }
    }
