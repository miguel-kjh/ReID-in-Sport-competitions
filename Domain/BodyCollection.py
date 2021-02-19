from Domain.Body import Body

class BodyCollection:

    def __init__(self):
        self._bodies = []

    def addBody(self, body: Body):
        self._bodies.append(body)