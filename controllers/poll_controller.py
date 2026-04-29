from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from schemas.schemas import PollCreate, PollResponse, PollDetailResponse, VoteRequest, VoteResponse
from services import poll_service

router = APIRouter()

@router.post("/polls", response_model=PollResponse, status_code=201)
def create_poll(data: PollCreate, db: Session = Depends(get_db)):
    return poll_service.create_poll(db, data)

@router.get("/polls", response_model=list[PollResponse], status_code=200)
def get_polls(
    status: str | None = None,
    skip: int = 0, # Ajout de skip pour la pagination
    limit: int = 10, # Ajout de limit pour la pagination
    db: Session = Depends(get_db)
    ):
    return poll_service.get_polls(db, status, skip, limit) # Passage de skip et limit pour la pagination bonus

@router.get("/polls/{poll_id}", response_model=PollDetailResponse, status_code=200)
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    return poll_service.get_poll_by_id(db, poll_id)

@router.delete("/polls/{poll_id}", status_code=204)
def delete_poll(poll_id: int, db: Session = Depends(get_db)):
    poll_service.delete_poll(db, poll_id)
    return Response(status_code=204)

@router.post("/polls/{poll_id}/vote", response_model=VoteResponse, status_code=201)
def vote(poll_id: int, data: VoteRequest, db: Session = Depends(get_db)):
    return poll_service.create_vote(db, poll_id, data)

@router.get("/polls/{poll_id}/results", status_code=200)
def get_results(poll_id: int, db: Session = Depends(get_db)):
    return poll_service.get_poll_results(db, poll_id)

@router.get("/stats", status_code=200)
def get_stats(db: Session = Depends(get_db)):
    return poll_service.get_stats(db)
