from Domain.FacesCollection import FacesCollection
from Services.SaveFacesServices import SaveFacesServices
import json

class SaveFacesJson(SaveFacesServices):

    def saveFaces(self, folder: str, filename: str, facesCollection: FacesCollection, heuristic: str = "none") -> None:
        details = {
            "name": filename,
            "num_faces": facesCollection.size(),
            "faces": facesCollection.getRepresentation(),
            "model": facesCollection.model
        }
        filename = filename.replace('.jpg', '_%s_heuristic_faces.json' % heuristic)
        with open('%s/%s' %(folder,filename), 'w') as json_file:
            json.dump(details, json_file)