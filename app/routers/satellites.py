from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sqlalchemy as sa

from ..database import get_db
from .. import models, schemas

# CRUD Satellite
router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"]
)
# CREATE AND READ
@router.post("/", response_model=schemas.SatelliteResponse)
def create_satellite(
    satellite: schemas.SatelliteCreate,
    db: Session = Depends(get_db)
):
    db_satellite = models.Satellite(**satellite.dict())
    db.add(db_satellite)
    db.commit()
    db.refresh(db_satellite)
    return db_satellite


@router.get("/", response_model=list[schemas.SatelliteResponse])
def get_satellites(db: Session = Depends(get_db)):
    return db.query(models.Satellite).all()

# UPDATE
@router.put("/{satellite_id}", response_model=schemas.SatelliteResponse)
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
@router.delete("/{satellite_id}")
def delete_satellite(satellite_id: int, db: Session = Depends(get_db)):
    db_satellite = db.query(models.Satellite).filter(
        models.Satellite.id == satellite_id
    ).first()

    if not db_satellite:
        return {"error": "Satellite not found"}

    db.delete(db_satellite)
    db.commit()
    return {"status": "deleted"}
