from Controller.AlignedReIDController import AlignedReIDController
from Utils.constant import PLACES, MODELS, compressionMethod


FOLDER = "data/TGC_places"
controller = AlignedReIDController()

def computeEmbeddings():
    controller.computedEmbeddings(FOLDER, compression=True)

def computeBodyAndFacesEmbeddings(faces, bodies, filename):
    controller.compactedEmbeddings(faces, bodies, filename, compression=compressionMethod.tsne)


def computeBodyAndAllFacesEmbeddings(places, bodies, filename):
    controller.compactedEmbeddingsUsingAllFaces(places, bodies, filename, compression=compressionMethod.tsne)

if __name__ == '__main__':
    #computeEmbeddings()
    """for place in ['Ayagaures', 'ParqueSur']:
        for model in ['VGG-Face']:
            model = model.lower().replace('-', '_')
            computeBodyAndFacesEmbeddings(
                'data/Probe_faces_retinaface_none/%s/representations_%s.pkl' %(place, model),
                'data/TCG_alignedReId/%s.pkl' %place,
                '%s_retinaface_none_%s_tsne' % (place, model)
            )"""
    for place in ['Ayagaures', 'ParqueSur']:
        computeBodyAndAllFacesEmbeddings(
            'data/Probe_faces_retinaface_none/%s' %place,
            'data/TCG_alignedReId/%s.pkl' %place,
            '%s_retinaface_none_all' % place
        )