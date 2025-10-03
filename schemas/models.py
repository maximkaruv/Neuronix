from numpy import bmat
from pydantic import BaseModel

class Document(BaseModel):
    title: str
    content: str
    source: str

class QueryID(BaseModel):
    id: int

class Prompt(BaseModel):
    prompt: str