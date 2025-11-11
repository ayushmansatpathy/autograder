from pydantic import BaseModel
from typing import List, Optional

class QueryResult(BaseModel):
    document_id: str
    content: str
    similarity_score: Optional[float] = None
    """A single retrieved document and its metadata."""

class QueryResponse(BaseModel):
    response: str
    """Response for query requests, including matched documents."""