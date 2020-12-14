from Domain.FacesCollection import FacesCollection
from Services.SaveFacesServices import SaveFacesServices
import json

class SaveFacesJson(SaveFacesServices):

    def saveFaces(self, folder: str, filename: str, facesCollection: FacesCollection) -> None:
        details = {
            "name": filename,
            "num_faces": facesCollection.size(),
            "faces": facesCollection.getRepresentation()
        }
        filename = filename.replace('jpg', '_faces.json')
        with open('%s/%s' %(folder,filename), 'w') as json_file:
            json.dump(details, json_file)