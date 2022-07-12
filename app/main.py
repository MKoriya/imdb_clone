from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from . import models
from .database import engine
from .routers import movie, user, auth, watchlist
from fastapi.middleware.cors import CORSMiddleware

# FastAPI application
app = FastAPI()

# Creates Database using ORM models
models.Base.metadata.create_all(bind=engine)

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user.router)
app.include_router(movie.router)
app.include_router(auth.router)
app.include_router(watchlist.router)



@app.get("/")
def index():
    return RedirectResponse("/docs/")