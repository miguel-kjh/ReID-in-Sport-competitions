from Controller.AlignedReIDController import AlignedReIDController
from Utils.constant import PLACES, MODELS, FACES_MODELS, HEURISTICS


FOLDER = "data/TGC_places"
controller = AlignedReIDController()

def computeEmbeddings(compression=False):
    controller.computedEmbeddings(FOLDER, compression=compression)

def computeBodyAndFacesEmbeddings(faces, bodies, filename, compression=False):
    controller.compactedEmbeddings(faces, bodies, filename, compression=compression)


def computeBodyAndAllFacesEmbeddings(places, bodies, filename, compression=False):
    controller.compactedEmbeddingsUsingAllFaces(places, bodies, filename, compression=compression)

if __name__ == '__main__':
    #computeEmbeddings()
    for place in ['Arucas', 'Teror']:
        for faceModel in FACES_MODELS:
            print(faceModel)
            for heuristic in HEURISTICS:
                for model in MODELS:
                    model = model.lower().replace('-', '_')
                    computeBodyAndFacesEmbeddings(
                        'data/Probe_faces_%s_%s/%s/representations_%s.pkl' %(faceModel, heuristic, place, model),
                        'data/TCG_alignedReId/%s.pkl' %place,
                        '%s_%s_%s_%s' % (place,faceModel, heuristic, model)
                    )
                    computeBodyAndFacesEmbeddings(
                        'data/Probe_faces_%s_%s/%s/representations_%s.pkl' %(faceModel, heuristic, place, model),
                        'data/TCG_alignedReId/%s.pkl' %place,
                        '%s_%s_%s_%s_pca' % (place,faceModel, heuristic, model),
                        compression=True
                    )
    """for place in ['Ayagaures', 'ParqueSur']:
        computeBodyAndAllFacesEmbeddings(
            'data/Probe_faces_retinaface_none/%s' %place,
            'data/TCG_alignedReId/%s.pkl' %place,
            '%s_retinaface_none_all' % place
        )"""