from abc import abstractmethod
from Domain.FacesCollection import FacesCollection

class FaceHeuristic:

    @abstractmethod
    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        pass