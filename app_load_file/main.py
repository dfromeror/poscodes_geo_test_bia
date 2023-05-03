import csv
import codecs
import uvicorn
from sqlalchemy.orm import Session

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
    data = {}
    rows_count_success = 0
    rows_count_fail = 0
    for row in csvReader:  
        try:
            poscodes_geo = schemas.PoscodesGeoCreate(lat=row['lat'], lon=row['lon'])  
            await PoscodesGeoRepo.create(db=db, poscodes_geo = poscodes_geo)
            rows_count_success += 1
        except Exception:
            rows_count_fail += 1
    
    return {'inserted': rows_count_success, 'fail': rows_count_fail}

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def health_chech():
    return {'healthcheck': 'Everything OK!'}




if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)