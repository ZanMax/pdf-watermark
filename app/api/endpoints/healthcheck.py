from typing import Any
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/healthcheck", response_model=Any)
def site_healthcheck() -> Any:
    now = datetime.now()
    return {"date": f"{now}", "status": "online"}
