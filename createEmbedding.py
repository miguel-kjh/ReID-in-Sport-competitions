from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.constant import PLACES
from Utils.fileUtils import isImage, isPcafile

import os

PROBE = 'data/Probe_faces_retinaface_none/Arucas/5_Arucas_frame_01_26_18_000_0_faces.jpg'

GALLERIES = ["data/Probe_faces_retinaface_none"]

MODELS = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]

facesRecognition = FacesRecognitionService()

def createEmbedding():
    for gallery in GALLERIES:
        for place in PLACES:
            for model in MODELS:
                facesRecognition.verifyImageInDataBase(PROBE, os.path.join(gallery, place), model = model)

def reductionDimension():
    for gallery in GALLERIES:
        for place in PLACES:
            for dirpath, _, filenames in os.walk(os.path.join(gallery, place)):
                for filename in filenames:
                    if not isImage(filename) and not isPcafile(filename):
                        facesRecognition.reductionFacesDimension(
                            os.path.join(dirpath, filename),
                            os.path.join(dirpath, filename.replace(".pkl", "_pca.pkl"))
                        )

if __name__ == '__main__':
    #createEmbedding()
    reductionDimension()