from abc import abstractmethod
from Domain.FacesCollection import FacesCollection

class FaceHeuristic:

    def __init__(self, type: str):
        self.type = type

    @abstractmethod
    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        pass

class NonHeuristic(FaceHeuristic):

    def __init__(self, type: str):
        super().__init__(type)

    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        return faceCollection


class DimensionBasedHeuristic(FaceHeuristic):

    def __init__(self, type: str):
        super().__init__(type)
        self.thresholdHeight: int   = 50
        self.thresholdScore: float  = 0.80



    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        if faceCollection.isEmpty(): return faceCollection

        newCollection = FacesCollection()
        newCollection.addFaces(list(
            filter(lambda face:
                   abs(face.height - face.posY) > self.thresholdHeight
                   and face.score > self.thresholdScore,
                   faceCollection.facesCollection)
        ))
        return newCollection

