from Face import Face

class FacesCollection:
    def __init__(self):
        self.faceCollection = []

    def addFace(self, id, posX, posY, width, height) -> None:
        self.faceCollection.append(
            Face(id,posX, posY, width, height)
        )

    def getRepresentation(self) -> set:
        return {
            face.packData() for face in self.faceCollection
        }

