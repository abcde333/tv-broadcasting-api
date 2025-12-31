from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sqlalchemy as sa

from ..database import get_db
from .. import models, schemas
from ..models import Broadcast, TVChannel, Satellite

router = APIRouter(
    prefix="/broadcasts",
    tags=["Broadcasts"]
)

# CREATE
@router.post("/", response_model=schemas.BroadcastResponse)
def create_broadcast(
    broadcast: schemas.BroadcastCreate,
    db: Session = Depends(get_db)
):
    db_broadcast = models.Broadcast(**broadcast.dict())
    db.add(db_broadcast)
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


# READ
@router.get("/", response_model=list[schemas.BroadcastResponse])
def get_broadcasts(db: Session = Depends(get_db)):
    return db.query(models.Broadcast).all()


# UPDATE (non-trivial)
@router.put("/{broadcast_id}", response_model=schemas.BroadcastResponse)
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
@router.delete("/{broadcast_id}")
def delete_broadcast(broadcast_id: int, db: Session = Depends(get_db)):
    db_broadcast = db.query(models.Broadcast).filter(
        models.Broadcast.id == broadcast_id
    ).first()

    if not db_broadcast:
        return {"error": "Broadcast not found"}

    db.delete(db_broadcast)
    db.commit()
    return {"status": "deleted"}


# JOIN
@router.get("/with-details")
 # JOIN Broadcasts + Satellites + TV Channels
def broadcasts_with_details(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Broadcast.id,
            models.Broadcast.frequency,
            models.Satellite.name.label("satellite"),
            models.TVChannel.name.label("channel")
        )
        .join(models.Satellite, models.Broadcast.satellite_id == models.Satellite.id)
        .join(models.TVChannel, models.Broadcast.tv_channel_id == models.TVChannel.id)
        .all()
    )
    return [
        {"id": r.id, "frequency": r.frequency, "satellite": r.satellite, "channel": r.channel}
        for r in results
    ]

# GROUP BY
@router.get("/count-by-satellite")
# Count broadcasts per satellite
def count_by_satellite(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Broadcast.satellite_id,
            sa.func.count(models.Broadcast.id).label("count")
        )
        .group_by(models.Broadcast.satellite_id)
        .all()
    )
    return [{"satellite_id": r.satellite_id, "count": r.count} for r in results]

# ORDER BY (sort by API)
@router.get("/sorted")
def list_broadcasts(
    sort: str = "frequency_asc",
    db: Session = Depends(get_db)
):
    query = db.query(models.Broadcast)

    if sort == "frequency_desc":
        query = query.order_by(models.Broadcast.frequency.desc())
    else:
        query = query.order_by(models.Broadcast.frequency.asc())

    return query.all()

