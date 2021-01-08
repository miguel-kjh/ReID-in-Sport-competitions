from abc import abstractmethod
from Domain.FacesCollection import FacesCollection


class FacesLocator:

    @abstractmethod
    def locate(self, file: str) -> FacesCollection:
        pass