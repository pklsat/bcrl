from pydantic import BaseModel
from typing import List
from uuid import UUID as uuid

# Job API(Common)
class JobSubmitResponse(BaseModel):
    api: str = None
    req_id: uuid = None
    message: str = None

class JobStatusResponse(BaseModel):
    req_id: uuid = None
    api: str = None
    status: str = None

#SOC API
class SocRequest(BaseModel):
    api: str = None
    current_soc: float = None
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
    req_id: uuid = None
    schedule: List[SocSchedule] = None
    metadata: SocMetadata = None