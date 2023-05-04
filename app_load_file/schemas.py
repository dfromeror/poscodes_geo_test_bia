from typing import List, Optional

from pydantic import BaseModel


class PostcodesGeoZip(BaseModel):
    zip: int

class PostcodesGeoBase(BaseModel):
    lat: float
    lon: float
    zip: Optional[int] = None

class PostcodesGeoCreate(PostcodesGeoBase):
    pass

class PostcodesGeo(PostcodesGeoBase):
    id: int

    class Config:
        orm_mode = True