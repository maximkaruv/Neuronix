import faiss
import numpy as np
import os
import pickle

class VectorStore:
    def __init__(self, filepath: str, dimension: int):
        self.dimension = dimension
        self.filepath = filepath
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
        self.id_map = {}

        if os.path.exists(filepath + ".index") and os.path.exists(filepath + ".pkl"):
            self.index = faiss.read_index(filepath + ".index")
            with open(filepath + ".pkl", "rb") as f:
                self.id_map = pickle.load(f)

    def _ensure_2d(self, arr):
        arr = np.array(arr, dtype="float32")
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        return arr

    def set(self, ids, vectors):
        ids = np.atleast_1d(np.array(ids, dtype=np.int64))
        vectors = self._ensure_2d(vectors)
        self.delete(ids)
        self.index.add_with_ids(vectors, ids)
        for i, v in zip(ids, vectors):
            self.id_map[i] = v

    def delete(self, ids):
        ids = np.atleast_1d(np.array(ids, dtype=np.int64))
        self.index.remove_ids(ids)
        for i in ids:
            self.id_map.pop(i, None)

    def search(self, vectors, k):
        vectors = self._ensure_2d(vectors)
        _, I = self.index.search(vectors, k)
        return I.tolist()

    def get_all_ids(self):
        return list(self.id_map.keys())

    def save(self):
        faiss.write_index(self.index, self.filepath + ".index")
        with open(self.filepath + ".pkl", "wb") as f:
            pickle.dump(self.id_map, f)

    def reset(self):
        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(self.dimension))
        self.id_map.clear()
