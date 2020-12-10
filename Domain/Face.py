class Face:
    def __init__(self, id, posX: int, posY: int, width: int, height: int):
        self.id: int     = id
        self.posX: int   = posX
        self.posY: int   = posY
        self.width: int  = width
        self.height: int = height

    def packData(self):
        return {
            "id": self.id,
            "posX": self.posX,
            "posY": self.posY,
            "width": self.width,
            "height": self.height
        }
