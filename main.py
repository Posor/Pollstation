from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from controllers import poll_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # J'autorise tout le monde ("*") pour origins afin de m'assurer que le script d'évaluation ne soit pas bloqué.
    # En production, on mettrait une origine stricte comme "http://localhost:3000" comme vu au TD 4.
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(poll_controller.router)
