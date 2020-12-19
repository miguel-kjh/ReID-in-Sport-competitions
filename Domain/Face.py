class Face:
    def __init__(self, id, posX: int, posY: int, width: int, height: int):
        self.id: int     = id
        self.posX: int   = posX
        self.posY: int   = posY
        self.width: int  = width
        self.height: int = height

    def packData(self) -> dict:
        return {
            "posX": self.posX,
            "posY": self.posY,
            "width": self.width,
            "height": self.height
        }

    def getArea(self) -> float:
        return self.width * self.height

    def __lt__(self, other) -> bool:
        return self.getArea() < other.getArea()

    def __le__(self, other):
        return self.getArea() <= other.getArea()

    def __eq__(self, other):
        return self.getArea() == other.getArea()

    def __ne__(self, other):
        return self.__eq__(other)

    def __gt__(self, other) -> bool:
        return not self.__lt__(other)

    def __ge__(self, other):
        return not self.__le__(other)

    def __str__(self) -> str:
        return "id: %s | position: (%s,%s) | dim: (%s,%s)" %(self.id, self.posY, self.posY, self.width, self.height)


