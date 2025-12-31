from pydantic import BaseModel
from typing import Optional, Dict

# Satellite

class SatelliteBase(BaseModel):
    name: str
    country: str
    service_life: Optional[int]
    orbit_radius: Optional[float]


class SatelliteCreate(SatelliteBase):
    pass


class SatelliteResponse(SatelliteBase):
    id: int

    class Config:
        orm_mode = True

# TVChannel

class TVChannelBase(BaseModel):
    name: str
    broadcast_language: str
    country: str
    company: Optional[str]
    specifics: Optional[str]
    metadata_json: Optional[Dict]


class TVChannelCreate(TVChannelBase):
    pass


class TVChannelResponse(TVChannelBase):
    id: int

    class Config:
        orm_mode = True

# Broadcast

class BroadcastBase(BaseModel):
    satellite_id: int
    tv_channel_id: int
    frequency: float
    coverage_from: Optional[int]
    coverage_to: Optional[int]


class BroadcastCreate(BroadcastBase):
    pass


class BroadcastResponse(BroadcastBase):
    id: int

    class Config:
        orm_mode = True

