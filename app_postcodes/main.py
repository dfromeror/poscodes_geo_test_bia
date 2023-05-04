from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from repositories import PostcodesGeoRepo
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
app = FastAPI(title="PostCodes API",
    description="API for generate PostCodes from Lat and Lon",
    version="1.0.0",)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



@app.put('/postcodes_geo', tags=["PostcodesGeo"])
def get_postcodes_geo(postcodes_geo_request: schemas.PostcodesGeo):
    """
    Get postcode from Lat and Lon
    """
    zip_code = PostcodesGeoRepo.generate_zip_code(lat=postcodes_geo_request.lat, lon=postcodes_geo_request.lon)

    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }

    json_data = {
        'zip': zip_code,
    }

    response = requests.put(f'http://127.0.0.1:8080/update_zip_code/{postcodes_geo_request.id}', headers=headers, json=json_data)

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