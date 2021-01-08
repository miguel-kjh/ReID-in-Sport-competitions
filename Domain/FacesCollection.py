from Domain.Face import Face

class FacesCollection:
    def __init__(self, model: str = ""):
        self.facesCollection = []
        self.model = model

    def addFace(self, face: Face) -> None:
        self.facesCollection.append(face)

    def addFaces(self, faces: list) -> None:
        self.facesCollection[len(self.facesCollection):] = faces

    def getRepresentation(self) -> dict:
        return {
            face.id: face.packData() for face in self.facesCollection
        }

    def getFace(self, index: int) -> Face:
        return self.facesCollection[index]

    def size(self) -> int:
        return len(self.facesCollection)

    def isEmpty(self) -> bool:
        return self.size() == 0


