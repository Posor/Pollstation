from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException
from schemas.schemas import PollCreate, VoteRequest
from dao import poll_dao

def get_current_status(closes_at):
    if closes_at is None:
        return "open"
    # On compare si la date de fermeture est dépassée
    if datetime.now(timezone.utc) > closes_at.replace(tzinfo=timezone.utc):
        return "closed"
    return "open"

def create_poll(db: Session, poll_data: PollCreate):
    if len(poll_data.options) < 2:
        raise HTTPException(status_code=400, detail="A poll must have at least 2 options.")
    
    if poll_data.closes_at:
        if poll_data.closes_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="closes_at cannot be in the past.")
            
    return poll_dao.create_poll(db, poll_data)

def get_polls(db: Session, status: str = None, skip: int = 0, limit: int = 10):
    polls = poll_dao.get_polls(db, skip=skip, limit=limit)  # Utilisation de skip et limit pour répondre au bonus de pagination
    result = []
    for poll in polls:
        poll_status = get_current_status(poll.closes_at)
        if status and poll_status != status:
            continue
        
        result.append({
            "id": poll.id,
            "question": poll.question,
            "status": poll_status,
            "closes_at": poll.closes_at
        })
    return result

def get_poll_by_id(db: Session, poll_id: int):
    poll = poll_dao.get_poll_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll {poll_id} not found.")
    
    return {
        "id": poll.id,
        "question": poll.question,
        "status": get_current_status(poll.closes_at),
        "closes_at": poll.closes_at,
        "options": [{"id": opt.id, "text": opt.text} for opt in poll.options]
    }

def delete_poll(db: Session, poll_id: int):
    poll = poll_dao.get_poll_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll {poll_id} not found.")
    
    if len(poll.votes) > 0:
        raise HTTPException(status_code=409, detail=f"poll {poll_id} has votes and cannot be deleted")
        
    poll_dao.delete_poll(db, poll)

def create_vote(db: Session, poll_id: int, vote_data: VoteRequest):
    poll = poll_dao.get_poll_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll {poll_id} not found.")
        
    if get_current_status(poll.closes_at) == "closed":
        raise HTTPException(status_code=400, detail="Cannot vote on a closed poll.")
        
    existing_vote = poll_dao.get_vote_by_token_and_poll(db, vote_data.voter_token, poll_id)
    if existing_vote:
        raise HTTPException(status_code=409, detail=f"voter_token {vote_data.voter_token} has already voted on poll {poll_id}")
        
    option = poll_dao.get_option_by_id(db, vote_data.option_id)
    if not option or option.poll_id != poll_id:
        raise HTTPException(status_code=400, detail=f"option {vote_data.option_id} does not belong to poll {poll_id}")
        
    return poll_dao.create_vote(db, poll_id, vote_data.option_id, vote_data.voter_token)

def get_poll_results(db: Session, poll_id: int):
    poll = poll_dao.get_poll_by_id(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll {poll_id} not found.")
        
    total_votes = len(poll.votes)
    options_stats = []
    
    for opt in poll.options:
        opt_votes = len(opt.votes)
        percent = (opt_votes / total_votes * 100) if total_votes > 0 else 0.0
        options_stats.append({
            "id": opt.id,
            "text": opt.text,
            "votes": opt_votes,
            "percent": round(percent, 1)
        })
        
    return {
        "poll_id": poll.id,
        "total": total_votes,
        "options": options_stats
    }

def get_stats(db: Session):
    total_polls = poll_dao.count_polls(db)
    total_votes = poll_dao.count_votes(db)
    
    polls = poll_dao.get_polls(db, limit=None) # Récupération de tous les sondages
    top_poll = None
    max_votes = -1
    
    for poll in polls:
        votes_count = len(poll.votes)
        if votes_count > max_votes:
            max_votes = votes_count
            top_poll = {"id": poll.id, "question": poll.question}
            
    return {
        "polls": total_polls,
        "votes": total_votes,
        "top_poll": top_poll if max_votes > 0 else None
    }