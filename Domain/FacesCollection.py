from Domain.Face import Face

class FacesCollection:
    def __init__(self, model: str = "", data: dict = None):
        if not data:
            self.facesCollection = []
            self.model = model
        else:
            self.facesCollection = [
                Face(key,
                     face['posX'],
                     face['posY'],
                     face['width'],
                     face['height'],
                     face['score'])
                for key,face in data['faces'].items()
            ]
            self.model = data['model']

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

    def __str__(self) -> str:
        return "model: %s | collection: %s" %(self.model, self.facesCollection)

    def __repr__(self) -> str:
        return self.__str__()




