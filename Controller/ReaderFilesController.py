from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()

    def run(self, folder: str) -> None:
        print(
            self.faceLocatorService.locator(1, "../data/TGC2020v0.3_PRL/1/1_ParqueSur_frame_12_40_15_000.jpg")
        )