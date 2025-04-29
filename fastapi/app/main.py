from fastapi import FastAPI, Body
import json
from pathlib import Path

from app.models import SocRequest
from app.models import SocResponse

app = FastAPI()


def writeRequestJson(
    data,
):
    path = (
        Path(__file__).parent.parent.parent
        / "shared"
        / "bcrlapi"
        / "json"
        / "request.json"
    )
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def readResponseJson():
    path = Path(__file__).parent.parent / "response.json"
    with open(path, "r") as f:
        return json.load(f)


@app.post("/simulate/", response_model=SocResponse)
def simulate_json(req: SocRequest = Body(...)):
    reqdict = req.dict()
    reqjson = json.dumps(reqdict)
    writeRequestJson(reqjson)
    resjson = readResponseJson()
    res = SocResponse.parse_obj(resjson)
    return res
