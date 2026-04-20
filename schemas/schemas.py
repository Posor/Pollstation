from pydantic import BaseModel
from datetime import datetime

class OptionBase(BaseModel):
    text: str

class OptionResponse(OptionBase):
    id: int

    model_config = { "from_attributes": True }

class PollCreate(BaseModel):
    question: str
    options: list[str]
    closes_at: datetime | None = None

class PollResponse(BaseModel):
    id: int
    question: str
    status: str
    closes_at: datetime | None = None

    model_config = { "from_attributes": True }

class PollDetailResponse(PollResponse):
    options: list[OptionResponse]

class VoteRequest(BaseModel):
    voter_token: str
    option_id: int

class VoteResponse(BaseModel):
    id: int
    poll_id: int
    option_id: int

    model_config = { "from_attributes": True }