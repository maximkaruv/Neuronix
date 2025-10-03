from fastapi import FastAPI, HTTPException
from numpy import source
from modules.storage import Storage
from modules.embedder import embedder
from modules.generator import generator
from schemas.models import Document, QueryID, Prompt
from config import BLOCK, MESSAGE

app = FastAPI()

storage = Storage('data/vectors', 1536, 'data/metadata', embedder)


@app.post("/documents")
def push_one_document(doc: Document) -> int:
    try:
        idx = storage.push_docs([doc])
        return idx
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении документов")

@app.get("/documents")
def get_all_documents() -> list[tuple[int, Document]]:
    try:
        docs = storage.get_all_documents()
        return docs
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении базы документов")

@app.delete("/documets/{id}")
def delete_one_document(query: QueryID):
    try:
        storage.delete([query.id])
        return 200
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении документа")

@app.post("/ask")
def smart_search(query: Prompt):
    try:
        hits = storage.search(query.prompt, 2)
        blocks = [BLOCK.format(content=hit.content, source=hit.source) for hit in hits]
        prompt = MESSAGE.format(query.prompt, blocks=blocks.split('\n---\n'))
        answer = generator(prompt)
        return answer
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при умном нейро-поиске")


