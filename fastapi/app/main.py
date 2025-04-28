from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path

# SocRequest Model
class SocRequest(BaseModel):
    current_soc: float
    month: int
    day: int
    hour: int
    minute: int

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

app = FastAPI()

def writeRequestJson(data, ):
    path = Path(__file__).parent.parent.parent/ 'shared' / 'bcrlapi' / 'json' / 'request.json'
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def readResponseJson():
    path = Path(__file__).parent.parent / 'response.json'
    with open(path, "r") as f:
        return json.load(f)

@app.post("/simulate/", response_model=SocResponse)
async def simulate_json(req: SocRequest):
    reqdict = req.dict()
    reqjson = json.dumps(reqdict)
    writeRequestJson(reqjson)
    resjson = readResponseJson()
    res = SocResponse.parse_obj(resjson)
    return res