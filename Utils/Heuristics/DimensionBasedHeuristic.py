from Utils.Heuristics import FaceHeuristic
from Domain.FacesCollection import FacesCollection

class DimensionBasedHeuristic(FaceHeuristic):

    def filterFaces(self, faceCollection: FacesCollection) -> FacesCollection:
        newCollection = FacesCollection()
        newCollection.addFace(max(faceCollection))
        return newCollection