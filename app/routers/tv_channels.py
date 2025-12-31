from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sqlalchemy as sa

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/tv-channels",
    tags=["TV Channels"]
)

# READ TVChannels WITH PAGINATION

from fastapi import Query, HTTPException

@router.get("/", response_model=list[schemas.TVChannelResponse])
def list_tv_channels(
    page: int = Query(1, gt=0, description="Page number must be > 0"),
    limit: int = Query(20, gt=0, description="Limit must be > 0"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    return db.query(models.TVChannel).offset(offset).limit(limit).all()


# CREATE
@router.post("/", response_model=schemas.TVChannelResponse)
def create_tv_channel(
    channel: schemas.TVChannelCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new TV channel
    """
    db_channel = models.TVChannel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

# UPDATE BY ID
@router.put("/{channel_id}", response_model=schemas.TVChannelResponse)
def update_tv_channel(
    channel_id: int,
    channel: schemas.TVChannelCreate,
    db: Session = Depends(get_db)
):
    """
    Update a TV channel by ID
    """
    db_channel = db.query(models.TVChannel).filter(
        models.TVChannel.id == channel_id
    ).first()

    if not db_channel:
        return {"error": "TV channel not found"}

    for key, value in channel.dict().items():
        setattr(db_channel, key, value)

    db.commit()
    db.refresh(db_channel)
    return db_channel

# DELETE BY ID
@router.delete("/{channel_id}")
def delete_tv_channel(channel_id: int, db: Session = Depends(get_db)):
    """
    Delete a TV channel by ID
    """
    db_channel = db.query(models.TVChannel).filter(
        models.TVChannel.id == channel_id
    ).first()

    if not db_channel:
        return {"error": "TV channel not found"}

    db.delete(db_channel)
    db.commit()
    return {"status": "deleted"}

# SELECT + WHERE (3 conditions)
@router.get("/search")
def search_tv_channels(
    language: str,
    country: str,
    company: str,
    db: Session = Depends(get_db)
):
    """
    Find TV channels by three criteria:
    - broadcast language
    - country
    - company
    """
    return db.query(models.TVChannel).filter(
        models.TVChannel.broadcast_language == language,
        models.TVChannel.country == country,
        models.TVChannel.company == company
    ).all()

# UPDATE (non-trivial)
@router.get("/low-rating-channels")
def low_rating_channels(db: Session = Depends(get_db)):
    """
    Return channels with rating < 3 (from metadata_json).
    """
    channels = db.query(models.TVChannel).all()

    low_rating = [
        {
            "id": c.id,
            "name": c.name,
            "country": c.country,
            "broadcast_language": c.broadcast_language,
            "company": c.company,
            "specifics": c.specifics,
            "metadata_json": c.metadata_json
        }
        for c in channels
        if c.metadata_json and c.metadata_json.get("rating", 0) < 3
    ]

    return {"low_rating_channels": low_rating, "count": len(low_rating)}

# REST API search (regex)
@router.get("/search-metadata")
def search_metadata(
    q: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.TVChannel)
        .filter(
            sa.text("metadata_json::text ~* :pattern")
        )
        .params(pattern=q)
        .all()
    )


