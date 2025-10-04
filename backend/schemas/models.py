from pydantic import BaseModel

class Document(BaseModel):
    title: str
    content: str
    source: str

class Prompt(BaseModel):
    prompt: str

class Search(BaseModel):
    query: str
    count: int