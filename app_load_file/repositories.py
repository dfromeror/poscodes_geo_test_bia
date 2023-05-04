
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
import models
import time

import csv

import decimal, datetime, json

import schemas

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

        
class PoscodesGeoRepo:
    
    async def create(db: Session, poscodes_geo: schemas.PoscodesGeoCreate):
            db_poscodes_geo = models.PoscodesGeo(lat=poscodes_geo.lat, lon=poscodes_geo.lon)
            db.add(db_poscodes_geo)
            db.commit()
            db.refresh(db_poscodes_geo)
            return db_poscodes_geo


    async def load(db: Session, all_data: csv.DictReader):
        start_time = time.time()
        db.bulk_save_objects(
            [models.PoscodesGeo(lat=row['lat'], lon=row['lon']) for row in all_data]
        )
        db.commit()
        duration = time.time() - start_time
        return duration

        
    def fetch_by_id(db: Session,_id:int):
        return db.query(models.PoscodesGeo).filter(models.PoscodesGeo.id == _id).first()
    
    def fetch_by_lat_lon(db: Session,lat:float, lon:float):
        return db.query(models.PoscodesGeo).filter(models.PoscodesGeo.lat == lat, models.PoscodesGeo.lon == lon).first()
    
    async def delete(db: Session,_id:int):
        db_store= db.query(models.PoscodesGeo).filter_by(id=_id).first()
        db.delete(db_store)
        db.commit()
        
    async def update(db: Session,store_data):
        db.merge(store_data)
        db.commit()
        return store_data