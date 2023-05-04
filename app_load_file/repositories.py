
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

        
class PostcodesGeoRepo:
    
    async def create(db: Session, postcodes_geo: schemas.PostcodesGeoCreate):
            db_postcodes_geo = models.PostcodesGeo(lat=postcodes_geo.lat, lon=postcodes_geo.lon)
            db.add(db_postcodes_geo)
            db.commit()
            db.refresh(db_postcodes_geo)
            return db_postcodes_geo


    async def load(db: Session, all_data: csv.DictReader):
        start_time = time.time()
        db.bulk_save_objects(
            [models.PostcodesGeo(lat=row['lat'], lon=row['lon']) for row in all_data]
        )
        db.commit()
        duration = time.time() - start_time
        return duration

        
    def fetch_by_id(db: Session,_id:int):
        return db.query(models.PostcodesGeo).filter(models.PostcodesGeo.id == _id).first()
    
    def fetch_by_lat_lon(db: Session,lat:float, lon:float):
        return db.query(models.PostcodesGeo).filter(models.PostcodesGeo.lat == lat, models.PostcodesGeo.lon == lon).first()
    
    async def delete(db: Session,_id:int):
        db_store= db.query(models.PostcodesGeo).filter_by(id=_id).first()
        db.delete(db_store)
        db.commit()
        
    async def update(db: Session,store_data):
        db.merge(store_data)
        db.commit()
        return store_data