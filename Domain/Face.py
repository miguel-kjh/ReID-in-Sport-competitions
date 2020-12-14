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

    def __str__(self) -> str:
        return "id: %s | position: (%s,%s) | dim: (%s,%s)" %(self.id, self.posY, self.posY, self.width, self.height)


