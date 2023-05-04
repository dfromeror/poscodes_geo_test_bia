from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base
    
class PoscodesGeo(Base):
    __tablename__ = "poscodes_geo"
    
    id = Column(Integer, primary_key=True,index=True)
    lat = Column(Float, nullable=False, index=True)
    lon = Column(Float, nullable=False, index=True)
    zip = Column(Integer, nullable=True)
    def __repr__(self):
        return 'PoscodesGeo(id=%s, lat=%s, lon=%s, zip=%s)' % (self.id, self.lat,self.lon, self.zip)