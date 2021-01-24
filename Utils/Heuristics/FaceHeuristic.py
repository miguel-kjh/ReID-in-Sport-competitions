from abc import abstractmethod
from Domain.FacesCollection import FacesCollection

class FaceHeuristic:

    @abstractmethod
    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        pass

class NonHeuristic(FaceHeuristic):

    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        return faceCollection


class DimensionBasedHeuristic(FaceHeuristic):

    def __init__(self):
        self.thresholdHeight: int = 100


    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        if faceCollection.isEmpty(): return faceCollection

        newCollection = FacesCollection()
        newCollection.addFaces(list(
            filter(lambda face: face.height > self.thresholdHeight, faceCollection.facesCollection)
        ))
        return newCollection

class ScoreBasedHeuristic(FaceHeuristic):

    def __init__(self):
        self.threshold: int = 0.95

    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        if faceCollection.isEmpty(): return faceCollection

        newCollection = FacesCollection()
        newCollection.addFaces(list(
            filter(lambda face: face.score > self.threshold, faceCollection.facesCollection)
        ))
        return newCollection


