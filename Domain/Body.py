import numpy as np
from datetime import timedelta

class Body:

    def __init__(self, dorsal: int, embedding: np.array, date: timedelta, file: str):
        self._dorsal = dorsal
        self._embedding = embedding
        self._file = file
        self._date = date

    @property
    def dorsal(self):
        return self._dorsal

    @property
    def embedding(self):
        return self._embedding

    @property
    def file(self):
        return self._file

    @property
    def date(self):
        return self._date

    @embedding.setter
    def embedding(self, new_embedding: np.array):
        self._embedding = new_embedding

    def getBodyInformation(self) -> tuple:
        return self._dorsal, self._embedding