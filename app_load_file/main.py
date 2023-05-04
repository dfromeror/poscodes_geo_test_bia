import csv
import codecs
import uvicorn
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from repositories import PoscodesGeoRepo
from db import get_db, engine
import schemas as schemas
import models as models

from fastapi import FastAPI, UploadFile, status, Depends


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    duration= await PoscodesGeoRepo.load(db=db, all_data=csvReader)
    
    return {'duration': duration}


@app.get('/poscodes_geo/{id}', tags=["PoscodesGeo"],response_model=schemas.PoscodesGeo)
def get_department(id: int,db: Session = Depends(get_db)):
    """
    Get the department with the given ID provided by User departmentd in database
    """
    db_departments = PoscodesGeoRepo.fetch_by_id(db,id)
    # if db_departments is None:
    #     raise HTTPException(status_code=404, detail="department not found with the given ID")
    return db_departments


@app.put('/update_zip_code/{id}', tags=["PoscodesGeo"],response_model=schemas.PoscodesGeo)
async def update_zip_code(id: int, poscodes_geo_request: schemas.PoscodesGeoZip, db: Session = Depends(get_db)):
    """
    Update an hired_employee jobd in the database
    """
    db_oscodes_geo = PoscodesGeoRepo.fetch_by_id(db, id)
    if db_oscodes_geo:
        update_hired_employee_encoded = jsonable_encoder(poscodes_geo_request)
        db_oscodes_geo.zip = update_hired_employee_encoded['zip']
        return await PoscodesGeoRepo.update(db=db, store_data=db_oscodes_geo)
    # else:
    #     raise HTTPException(status_code=400, detail="hired_employee not found with the given ID")

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def health_chech():
    return {'healthcheck': 'Everything OK!'}




if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)