from typing import List, Optional

from pydantic import BaseModel


class PostcodesGeoBase(BaseModel):
    lat: float
    lon: float

class PostcodesGeoCreate(PostcodesGeoBase):
    pass

class PostcodesGeo(PostcodesGeoBase):
    id: int

    class Config:
        orm_mode = True