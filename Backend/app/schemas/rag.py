from pydantic import BaseModel, Field

class RAGSearchRequest(BaseModel):

    query: str = Field(..., min_length=3)

    top_k: int = Field(default=5, ge=1, le=20)

class RetrievedDocument(BaseModel):

    title: str

    source: str

    score: float

    content: str

class RAGSearchResponse(BaseModel):

    query: str

    retrieved_documents: list[RetrievedDocument]