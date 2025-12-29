from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

# Satellite
class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    service_life = Column(Integer) 
    orbit_radius = Column(Float)

    broadcasts = relationship("Broadcast", back_populates="satellite")

# TVChannel
class TVChannel(Base):
    __tablename__ = "tv_channels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    broadcast_language = Column(String, nullable=False)
    country = Column(String, nullable=False)
    company = Column(String)
    specifics = Column(String)

    metadata_json = Column(JSON)

    broadcasts = relationship("Broadcast", back_populates="tv_channel")

# Broadcast
class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True)
    satellite_id = Column(Integer, ForeignKey("satellites.id"))
    tv_channel_id = Column(Integer, ForeignKey("tv_channels.id"))
    frequency = Column(Float, nullable=False)
    coverage_from = Column(Integer)
    coverage_to = Column(Integer)

    satellite = relationship("Satellite", back_populates="broadcasts")
    tv_channel = relationship("TVChannel", back_populates="broadcasts")
