from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    closes_at = Column(DateTime, nullable=True) 
    
    options = relationship("Option", back_populates="poll", cascade="all, delete-orphan") # le paramètre cascade="all, delete-orphan" permet de supprimer les options associées lorsqu'un sondage est supprimé
    votes = relationship("Vote", back_populates="poll", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    
    poll = relationship("Poll", back_populates="options")
    votes = relationship("Vote", back_populates="option", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_token = Column(String, nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"))
    poll_id = Column(Integer, ForeignKey("polls.id"))
    
    option = relationship("Option", back_populates="votes")
    poll = relationship("Poll", back_populates="votes")