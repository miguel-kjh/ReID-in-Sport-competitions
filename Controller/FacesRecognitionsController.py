from Services.FacesRecognitionServices import FacesRecognitionService

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()

    def identificationPeople(self, personToSearch: str, database: str) -> str:
        df = self._recognition.verifyImageInDataBase(personToSearch, database)
        return df['identity'][0] if not df.empty else ''
