import numpy as np

class Body:

    def __init__(self, dorsal: int, embedding: np.array):
        self._dorsal = dorsal
        self._embedding = embedding

    @property
    def dorsal(self):
        return self._dorsal

    @property
    def embedding(self):
        return self._embedding

    def getBodyInformation(self) -> tuple:
        return self._dorsal, self._embedding