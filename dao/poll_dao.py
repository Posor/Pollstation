from sqlalchemy.orm import Session
from models.models import Poll, Option, Vote
from schemas.schemas import PollCreate

def create_poll(db: Session, poll_data: PollCreate):
    db_poll = Poll(question=poll_data.question, closes_at=poll_data.closes_at)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    for option_text in poll_data.options:
        db_option = Option(text=option_text, poll_id=db_poll.id)
        db.add(db_option)
    
    db.commit()
    db.refresh(db_poll)
    return db_poll

def get_polls(db: Session, skip: int = 0, limit: int | None = 10): # Utilisation de skip et limit pour répondre au bonus de pagination
    query = db.query(Poll).offset(skip) # Si skip est à 0 (par défaut), on commence à partir du premier résultat
    
    if limit is not None: # Si limit est à None, on ne limite pas le nombre de résultats retournés
        query = query.limit(limit)
        
    return query.all()

def get_poll_by_id(db: Session, poll_id: int):
    return db.query(Poll).filter(Poll.id == poll_id).first() # utilisation de .first() afin de récupérer le premier résultat du filtre

def delete_poll(db: Session, poll: Poll):
    db.delete(poll)
    db.commit()

def get_option_by_id(db: Session, option_id: int):
    return db.query(Option).filter(Option.id == option_id).first() # utilisation de .first() afin de récupérer le premier résultat du filtre

def get_vote_by_token_and_poll(db: Session, voter_token: str, poll_id: int):
    return db.query(Vote).filter(Vote.voter_token == voter_token, Vote.poll_id == poll_id).first()

def create_vote(db: Session, poll_id: int, option_id: int, voter_token: str):
    db_vote = Vote(poll_id=poll_id, option_id=option_id, voter_token=voter_token)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def count_polls(db: Session):
    return db.query(Poll).count() # utilisation de .count() afin de compter le nombre de résultats retournés par la requête 

def count_votes(db: Session):
    return db.query(Vote).count() # utilisation de .count() afin de compter le nombre de résultats retournés par la requête 