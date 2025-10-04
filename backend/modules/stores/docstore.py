import json
import os

class DocumentStore:
    def __init__(self, path):
        self.path = path + '.json'
        self.docs = {}

        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.docs = json.load(f)

    def set(self, ids, documents):
        if isinstance(ids, (int, str)):
            ids = [ids]
            documents = [documents]
        for i, doc in zip(ids, documents):
            self.docs[str(i)] = doc

    def delete(self, ids) -> dict:
        if isinstance(ids, (int, str)):
            ids = [ids]

        results = {}
        for i in ids:
            key = str(i)
            if key in self.docs:
                self.docs.pop(key)
                results[i] = "deleted"
            else:
                results[i] = "already_deleted"
        return results

    def get_all_ids(self):
        return [int(x) for x in list(self.docs.keys())]

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)

    def reset(self):
        self.docs.clear()