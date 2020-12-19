from Domain.Face import Face

class FacesCollection:
    def __init__(self):
        self.faceCollection = []

    def addFace(self, face: Face) -> None:
        self.faceCollection.append(face)

    def getRepresentation(self) -> dict:
        return {
            face.id:face.packData() for face in self.faceCollection
        }

    def getFace(self, index: int) -> Face:
        return self.faceCollection[index]

    def size(self) -> int:
        return len(self.faceCollection)

    def isEmpty(self) -> bool:
        return self.size() == 0


