from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import PoscodesGeoRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

models.Base.metadata.create_all(bind=engine)


@app.get('/poscodes_geo/lat/{lat}/lon/{lon}', tags=["PoscodesGeo"],response_model=schemas.PoscodesGeo)
def get_poscodes_geo(lat: float, lon: float, db: Session = Depends(get_db)):
    """
    Get all the hired_employees jobd in database
    """
    if lat and lon:
        poscodes_geo =[]
        db_poscodes_geo = PoscodesGeoRepo.fetch_by_lat_lon(db,lat, lon)
        poscodes_geo.append(db_poscodes_geo)
        return poscodes_geo
    else:
        return PoscodesGeoRepo.fetch_all(db)



if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)