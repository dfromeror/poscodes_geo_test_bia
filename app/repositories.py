
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
import decimal, datetime, json

import util

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

        
class PoscodesGeoRepo:

    def generate_zip_code(lat: float, lon: float):
        return util.get_zipcode(lat=lat, lon=lon)
        