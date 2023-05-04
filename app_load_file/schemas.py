from typing import List, Optional

from pydantic import BaseModel


class PoscodesGeoZip(BaseModel):
    zip: int

class PoscodesGeoBase(BaseModel):
    lat: float
    lon: float
    zip: Optional[int] = None

class PoscodesGeoCreate(PoscodesGeoBase):
    pass

class PoscodesGeo(PoscodesGeoBase):
    id: int

    class Config:
        orm_mode = True