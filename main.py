import sys, os
sys.pycache_prefix = os.path.join(os.getcwd(), "__pycache__")

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from modules.storage import Storage
from pathlib import Path
from modules.embedder import embedder
from modules.generator import generator
from schemas.models import Document, Prompt, Search
from config import BLOCK, MESSAGE

app = FastAPI()

storage = Storage('data/vectors', 1536, 'data/metadata', embedder)
storage.vector_store.save()
storage.doc_store.save()


@app.post("/documents")
def push_one_document(doc: Document):
    try:
        idx = storage.push([doc])
        return idx[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при добавлении документов")

@app.get("/documents")
def get_all_documents():
    try:
        docs = storage.get_all_documents()
        return docs
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении базы документов")

@app.get("/documents/search")
def search_in_documents(query: Search):
    try:
        if not query.query:
            return JSONResponse(content={"detail": "Запрос пуст"}, status_code=400)
        docs = storage.search(query.query, query.count)
        return docs
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при получении базы документов")

@app.delete("/documents/{id}")
def delete_one_document(id: int):
    try:
        result = storage.delete([id])[id]
        if result == "deleted":
            return JSONResponse(content={"detail": "Документ удален"}, status_code=200)
        elif result == "already_deleted":
            return JSONResponse(content={"detail": "Документ не существует"}, status_code=400)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при удалении документа")

@app.post("/ask")
def smart_search(query: Prompt):
    try:
        hits = storage.search(query.prompt, 5)
        print(hits)
        if not hits:
            return JSONResponse(content={"details": "Ничего не найдено"}, status_code=500) 
        blocks = [BLOCK.format(content=doc.content, source=doc.source) for _, doc in hits]
        print(blocks)
        prompt = MESSAGE.format(query=query.prompt, blocks='\n---\n'.join(blocks))
        print(prompt)
        answer = generator(prompt)
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка при умном нейро-поиске")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)