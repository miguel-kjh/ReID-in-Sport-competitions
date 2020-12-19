from abc import abstractmethod
from Domain.FacesCollection import FacesCollection

class SaveFacesServices:

    @abstractmethod
    def saveFaces(self,
                  folder: str,
                  filename: str,
                  facesCollection: FacesCollection,
                  heuristic: str) -> None:
        pass