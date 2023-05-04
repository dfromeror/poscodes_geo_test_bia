from typing import List, Optional

from pydantic import BaseModel


class PoscodesGeoBase(BaseModel):
    lat: float
    lon: float

class PoscodesGeoCreate(PoscodesGeoBase):
    pass

class PoscodesGeo(PoscodesGeoBase):
    id: int

    class Config:
        orm_mode = True