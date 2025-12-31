from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

app = FastAPI(title="TV Broadcasting API")

Base.metadata.create_all(bind=engine)

# CRUD Satellite

# CREATE AND READ
@app.post("/satellites/", response_model=schemas.SatelliteResponse)
def create_satellite(
    satellite: schemas.SatelliteCreate,
    db: Session = Depends(get_db)
):
    db_satellite = models.Satellite(**satellite.dict())
    db.add(db_satellite)
    db.commit()
    db.refresh(db_satellite)
    return db_satellite


@app.get("/satellites/", response_model=list[schemas.SatelliteResponse])
def get_satellites(db: Session = Depends(get_db)):
    return db.query(models.Satellite).all()

# UPDATE
@app.put("/satellites/{satellite_id}", response_model=schemas.SatelliteResponse)
def update_satellite(
    satellite_id: int,
    satellite: schemas.SatelliteCreate,
    db: Session = Depends(get_db)
):
    db_satellite = db.query(models.Satellite).filter(
        models.Satellite.id == satellite_id
    ).first()

    if not db_satellite:
        return {"error": "Satellite not found"}

    for key, value in satellite.dict().items():
        setattr(db_satellite, key, value)

    db.commit()
    db.refresh(db_satellite)
    return db_satellite

# DELETE
@app.delete("/satellites/{satellite_id}")
def delete_satellite(satellite_id: int, db: Session = Depends(get_db)):
    db_satellite = db.query(models.Satellite).filter(
        models.Satellite.id == satellite_id
    ).first()

    if not db_satellite:
        return {"error": "Satellite not found"}

    db.delete(db_satellite)
    db.commit()
    return {"status": "deleted"}

# CRUD TVChannel

# CREATE AND READ
@app.post("/tv-channels/", response_model=schemas.TVChannelResponse)
def create_tv_channel(
    channel: schemas.TVChannelCreate,
    db: Session = Depends(get_db)
):
    db_channel = models.TVChannel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


@app.get("/tv-channels/", response_model=list[schemas.TVChannelResponse])
def get_tv_channels(db: Session = Depends(get_db)):
    return db.query(models.TVChannel).all()

# UPDATE
@app.put("/tv-channels/{channel_id}", response_model=schemas.TVChannelResponse)
def update_tv_channel(
    channel_id: int,
    channel: schemas.TVChannelCreate,
    db: Session = Depends(get_db)
):
    db_channel = db.query(models.TVChannel).filter(models.TVChannel.id == channel_id).first()
    if not db_channel:
        return {"error": "TV channel not found"}

    for key, value in channel.dict().items():
        setattr(db_channel, key, value)

    db.commit()
    db.refresh(db_channel)
    return db_channel

# DELETE
@app.delete("/tv-channels/{channel_id}")
def delete_tv_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = db.query(models.TVChannel).filter(models.TVChannel.id == channel_id).first()
    if not db_channel:
        return {"error": "TV channel not found"}

    db.delete(db_channel)
    db.commit()
    return {"status": "deleted"}


# CRUD Broadcast

# CREATE AND READ
@app.post("/broadcasts/", response_model=schemas.BroadcastResponse)
def create_broadcast(
    broadcast: schemas.BroadcastCreate,
    db: Session = Depends(get_db)
):
    db_broadcast = models.Broadcast(**broadcast.dict())
    db.add(db_broadcast)
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


@app.get("/broadcasts/", response_model=list[schemas.BroadcastResponse])
def get_broadcasts(db: Session = Depends(get_db)):
    return db.query(models.Broadcast).all()

# UPDATE (non trivial)
@app.put("/broadcasts/{broadcast_id}", response_model=schemas.BroadcastResponse)
def update_broadcast_frequency(
    broadcast_id: int,
    new_frequency: float,
    db: Session = Depends(get_db)
):
    db_broadcast = db.query(models.Broadcast).filter(
        models.Broadcast.id == broadcast_id,
        models.Broadcast.frequency < new_frequency
    ).first()

    if not db_broadcast:
        return {"error": "Broadcast not found or condition not met"}

    db_broadcast.frequency = new_frequency
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


# DELETE
@app.delete("/broadcasts/{broadcast_id}")
def delete_broadcast(broadcast_id: int, db: Session = Depends(get_db)):
    db_broadcast = db.query(models.Broadcast).filter(models.Broadcast.id == broadcast_id).first()
    if not db_broadcast:
        return {"error": "Broadcast not found"}

    db.delete(db_broadcast)
    db.commit()
    return {"status": "deleted"}

