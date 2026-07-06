from pydantic import BaseModel, Field


# ==========================================================
# Search
# ==========================================================

class RAGSearchRequest(BaseModel):

    query: str = Field(..., min_length=3)

    top_k: int = Field(default=5, ge=1, le=20)


# ==========================================================
# Search Result
# ==========================================================

class RetrievedDocument(BaseModel):

    title: str

    source: str

    score: float

    content: str


# ==========================================================
# Response
# ==========================================================

class RAGSearchResponse(BaseModel):

    query: str

    retrieved_documents: list[RetrievedDocument]