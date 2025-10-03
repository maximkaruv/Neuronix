from .stores.vectorstore import VectorStore
from .stores.docstore import DocumentStore
from schemas.models import Document

class Storage:
    def __init__(self, vector_store_path: str, dim: int, doc_store_path: str, embedder):
        self.vector_store = VectorStore(vector_store_path, dim)
        self.doc_store = DocumentStore(doc_store_path)
        self.embedder = embedder

    def push(self, documents: list[Document]):
        existing_ids = list(map(int, self.doc_store.get_all_ids()))
        start_id = max(existing_ids, default=0) + 1
        ids = [start_id + i for i in range(len(documents))]

        self.doc_store.set(ids, [doc.model_dump() for doc in documents])
        vectors = [self.embedder(doc.content) for doc in documents]  # только content
        self.vector_store.set(ids, vectors)

        self.doc_store.save()
        self.vector_store.save()

        return ids

    def update(self, ids: list[int], documents: list[Document]):
        self.doc_store.set(ids, [doc.model_dump() for doc in documents])
        vectors = [self.embedder(doc.content) for doc in documents]  # только content
        self.vector_store.set(ids, vectors)
        self.doc_store.save()
        self.vector_store.save()

    def delete(self, ids: list[int]):
        self.doc_store.delete(ids)
        self.vector_store.delete(ids)
        self.doc_store.save()
        self.vector_store.save()

    def get_all_documents(self) -> list[tuple[int, Document]]:
        ids = list(map(int, self.doc_store.get_all_ids()))
        return [(i, Document(**self.doc_store.docs[str(i)])) for i in ids]

    def search(self, query: str, k: int) -> list[Document]:
        vector = self.embedder(query)  # передаем только текст content
        ids_list = self.vector_store.search(vector, k)[0]  # FAISS возвращает список списков

        results = []
        all_ids = set(map(int, self.doc_store.get_all_ids()))
        for doc_id in ids_list:
            if doc_id in all_ids:
                doc_data = self.doc_store.docs[str(doc_id)]
                # results.append((doc_id, Document(**doc_data)))
                results.append(Document(**doc_data))
        return results

    def reset(self):
        self.doc_store.reset()
        self.vector_store.reset()
        self.doc_store.save()
        self.vector_store.save()
