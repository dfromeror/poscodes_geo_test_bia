import csv
import codecs
import uvicorn
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from repositories import PostcodesGeoRepo
from db import get_db, engine
import schemas as schemas
import models as models

from fastapi import FastAPI, UploadFile, status, Depends


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API for Load data",
    description="API for load data from CSV files",
    version="1.0.0",)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    duration= await PostcodesGeoRepo.load(db=db, all_data=csvReader)
    
    return {'duration': duration}


@app.get('/postcodes_geo/{id}', tags=["PostcodesGeo"],response_model=schemas.PostcodesGeo)
def get_department(id: int,db: Session = Depends(get_db)):
    """
    Get the postcodes with the given ID provided by User departmentd in database
    """
    db_departments = PostcodesGeoRepo.fetch_by_id(db,id)
    # if db_departments is None:
    #     raise HTTPException(status_code=404, detail="department not found with the given ID")
    return db_departments


@app.put('/update_zip_code/{id}', tags=["PostcodesGeo"],response_model=schemas.PostcodesGeo)
async def update_zip_code(id: int, postcodes_geo_request: schemas.PostcodesGeoZip, db: Session = Depends(get_db)):
    """
    Update an hired_employee jobd in the database
    """
    db_oscodes_geo = PostcodesGeoRepo.fetch_by_id(db, id)
    if db_oscodes_geo:
        update_hired_employee_encoded = jsonable_encoder(postcodes_geo_request)
        db_oscodes_geo.zip = update_hired_employee_encoded['zip']
        return await PostcodesGeoRepo.update(db=db, store_data=db_oscodes_geo)
    # else:
    #     raise HTTPException(status_code=400, detail="hired_employee not found with the given ID")

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def health_chech():
    return {'healthcheck': 'Everything OK!'}




if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)