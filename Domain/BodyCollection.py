from Domain.Body import Body

import numpy as np

class BodyCollection:

    def __init__(self, collection=None):
        if collection is None:
            collection = []
        self._bodies = collection

    def addBody(self, body: Body):
        self._bodies.append(body)

    def get_dataset(self) -> tuple:
        X = [body.embedding for body in self.bodies]
        y = [body.dorsal for body in self.bodies]

        return np.array(X), np.array(y)

    def set_embeddings(self, X: np.array):
        for body, x in zip(self.bodies, X):
            body.embedding = x

    @property
    def bodies(self):
        return self._bodies