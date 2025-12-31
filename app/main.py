from fastapi import FastAPI
from .database import Base, engine
from .routers import tv_channels, broadcasts, satellites

# Create the FastAPI app
app = FastAPI(title="TV Broadcasting API")

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Include routers for modular endpoints
app.include_router(satellites.router)   # Satellites CRUD
app.include_router(tv_channels.router)  # TV Channels CRUD and pagination
app.include_router(broadcasts.router)   # Broadcasts CRUD
