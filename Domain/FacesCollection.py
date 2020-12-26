from Domain.Face import Face

class FacesCollection:
    def __init__(self):
        self.facesCollection = []

    def addFace(self, face: Face) -> None:
        self.facesCollection.append(face)

    def getRepresentation(self) -> dict:
        return {
            face.id:face.packData() for face in self.facesCollection
        }

    def getFace(self, index: int) -> Face:
        return self.facesCollection[index]

    def size(self) -> int:
        return len(self.facesCollection)

    def isEmpty(self) -> bool:
        return self.size() == 0


