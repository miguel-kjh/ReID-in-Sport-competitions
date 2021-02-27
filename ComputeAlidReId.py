from Controller.AlignedReIDController import AlignedReIDController
from Utils.constant import PLACES, MODELS


FOLDER = "data/TGC_places"
controller = AlignedReIDController()

def computeEmbeddings():
    controller.computedEmbeddings(FOLDER, compression=True)

def computeBodyAndFacesEmbeddings(faces, bodies, filename):
    controller.compactedEmbeddings(faces, bodies, filename, compression=True)

if __name__ == '__main__':
    #computeEmbeddings()
    for place in PLACES:
        for model in MODELS:
            model = model.lower().replace('-', '_')
            computeBodyAndFacesEmbeddings(
                'data/Probe_faces_retinaface_none/%s/representations_%s.pkl' %(place, model),
                'data/TCG_alignedReId/%s.pkl' %place,
                '%s_retinaface_none_%s_pca' % (place, model)
            )