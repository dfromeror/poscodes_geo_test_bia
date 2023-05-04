from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from repositories import PoscodesGeoRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
import requests

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

import schemas as schemas

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



@app.put('/poscodes_geo', tags=["PoscodesGeo"])
def get_poscodes_geo(poscodes_geo_request: schemas.PoscodesGeo):
    """
    Update an hired_employee jobd in the database
    """
    zip_code = PoscodesGeoRepo.generate_zip_code(lat=poscodes_geo_request.lat, lon=poscodes_geo_request.lon)

    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }

    json_data = {
        'zip': zip_code,
    }

    response = requests.put(f'http://127.0.0.1:8080/update_zip_code/{poscodes_geo_request.id}', headers=headers, json=json_data)

    return "OK"

@app.get("/mars")
@limiter.limit("5/minute")
async def homepage(request: Request):
    return {"key": "value"}

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def health_chech():
    return {'healthcheck': 'Everything OK!'}


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)