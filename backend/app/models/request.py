from pydantic import BaseModel


class EmbedRubricRequest(BaseModel):
    user_id: str
    """The user ID of the namespace in which to embed the document"""


class EmbedTextRequest(BaseModel):
    user_id: str
    text: str
    """The user ID of the namespace in which to embed the document"""


class QueryRequest(BaseModel):
    question: str
    student_response: str
    user_id: str
    """Search query for retrieving relevant documents."""
