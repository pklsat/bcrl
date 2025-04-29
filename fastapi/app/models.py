from pydantic import BaseModel
from typing import List


# SocRequest Model
class SocRequest(BaseModel):
    current_soc: float
    month: int
    day: int
    hour: int
    minute: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_soc": 65.3,
                    "month": 9,
                    "day": 1,
                    "hour": 0,
                    "minute": 30,
                }
            ]
        }
    }


# SocResponse Model
class Schedule(BaseModel):
    hour: int
    minute: int
    soc: float


class Metadata(BaseModel):
    request_soc: float
    request_date: str
    generated_at: str
    message: str


class SocResponse(BaseModel):
    schedule: List[Schedule]
    metadata: Metadata
