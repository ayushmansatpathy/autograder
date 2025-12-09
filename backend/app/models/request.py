from pydantic import BaseModel
from typing import Optional


class EmbedRubricRequest(BaseModel):
    user_id: str


class EmbedTextRequest(BaseModel):
    user_id: str
    filename: str
    text: str


class QueryRequest(BaseModel):
    user_id: str
    question: str
    student_response: str