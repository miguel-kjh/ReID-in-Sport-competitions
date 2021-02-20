from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.constant import PLACES

import os

PROBE = 'data/Probe_faces_retinaface_none/Arucas/5_Arucas_frame_01_26_18_000_0_faces.jpg'

GALLERIES = ['data/Probe_faces_retinaface_none']

MODELS = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]

def createEmbedding():
    frs = FacesRecognitionService()
    for gallery in GALLERIES:
        for place in PLACES:
            for model in MODELS:
                frs.verifyImageInDataBase(PROBE, os.path.join(gallery, place), model = model)

if __name__ == '__main__':
    createEmbedding()