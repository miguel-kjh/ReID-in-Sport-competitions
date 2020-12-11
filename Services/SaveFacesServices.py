from abc import abstractmethod
from Domain.FacesCollection import FacesCollection

class SaveFacesServices:

    @abstractmethod
    def saveFaces(self, folder: str, filename: str, faceCollection: FacesCollection) -> None:
        pass