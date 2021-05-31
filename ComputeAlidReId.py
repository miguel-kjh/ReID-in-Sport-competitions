import os.path

from Controller.AlignedReIDController import AlignedReIDController
from Utils.constant import PLACES, MODELS, FACES_MODELS, HEURISTICS, PLACES_PROBE_TEST, PLACES_GALLERY_TEST
import argparse


FOLDER = "data/TGC_places"
controller = AlignedReIDController()

def computeEmbeddings(compression=False):
    controller.computedEmbeddings(FOLDER, compression=compression)

def computeBodyAndFacesEmbeddings(faces, bodies, filename, compression=False):
    controller.compactedEmbeddings(faces, bodies, filename, compression=compression)

def computeBodyAndAllFacesEmbeddings(places, bodies, filename, compression=False):
    controller.compactedEmbeddingsUsingAllFaces(places, bodies, filename, compression=compression)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--combine", action='count', help="create embedding combine faces and body")
    parser.add_argument("--light", action='count', help="create embedding combine faces and body with logthreid")
    parser.add_argument("--pca", action='count', help="apply pca to reduction the dimensions")

    args = parser.parse_args()
    if not args.combine:
        computeEmbeddings(args.pca)
    else:

        database = os.path.join("data", "TCG_alignedReId")
        if args.light:
            database = os.path.join("data", "TGC_ligthReId")
            controller.setFolder(database)

        for place in PLACES:
            for faceModel in FACES_MODELS:
                print(faceModel)
                for heuristic in HEURISTICS:
                    for model in MODELS:
                        model = model.lower().replace('-', '_')
                        if not args.pca:
                            computeBodyAndFacesEmbeddings(
                                'data/Probe_faces_%s_%s/%s/representations_%s.pkl' %(faceModel, heuristic, place, model),
                                '%s/%s.pkl' %(database, place),
                                '%s_%s_%s_%s' % (place,faceModel, heuristic, model)
                            )
                        else:
                            computeBodyAndFacesEmbeddings(
                                'data/Probe_faces_%s_%s/%s/representations_%s.pkl' %(faceModel, heuristic, place, model),
                                '%s/%s.pkl' %(database, place),
                                '%s_%s_%s_%s_pca' % (place,faceModel, heuristic, model),
                                compression=True
                            )