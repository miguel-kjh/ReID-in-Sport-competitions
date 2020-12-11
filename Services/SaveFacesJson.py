from Domain.FacesCollection import FacesCollection
from Services.SaveFacesServices import SaveFacesServices
import json

class SaveFacesJson(SaveFacesServices):

    def saveFaces(self, folder: str, filename: str, faceCollection: FacesCollection) -> None:
        details = {
            "name": filename,
            "num_faces": faceCollection.size(),
            "faces": faceCollection.getRepresentation()
        }
        filename = filename.replace('jpg', '_faces.json')
        with open('%s/%s' %(folder,filename), 'w') as json_file:
            json.dump(details, json_file)