import argparse
import os

from Controller.RecognitionsController import RecognitionsController
from Services.ReidentificationRepository import ReidentificationRepository
from Utils.fileUtils import extractModelAndHeuristics
from Utils.constant import PLACES_PROBE_TEST, PLACES_GALLERY_TEST, MODELS, METRICS, PLACES



def indentificationByFaces(database, model, metric):
    rs = RecognitionsController()
    repository = ReidentificationRepository()

    cmc, mAP = rs.identificationRunnersByFaces(
        os.path.join(database, PLACES_PROBE_TEST),
        model,
        metric,
        PLACES_GALLERY_TEST
    )
    faceModel, heuristic = extractModelAndHeuristics(database)
    repository.addTest(faceModel, heuristic, model, metric, cmc, mAP, PLACES_PROBE_TEST, PLACES_GALLERY_TEST)

def identificationByBody(metric, compression):
    rs = RecognitionsController()
    repository = ReidentificationRepository()
    folder = "data/TCG_alignedReId/%s.pkl" if not compression else "data/TCG_alignedReId/%s_tsne.pkl"

    """for probe in PLACES:
        for gallery in PLACES:
            if probe != gallery:
                print("[ %s - %s]" % (probe, gallery))
                cmc, mAP = rs.identificationRunnersByBody(
                    os.path.join(folder %probe),
                    metric,
                    os.path.join(folder %gallery)
                )

                repository.addTest("AlignedReId", "None", "ResNet50", metric, cmc, mAP, probe, gallery)"""
    cmc, mAP = rs.identificationRunnersByBody(
        os.path.join( folder %'%s_retinaface_none_all' % PLACES_PROBE_TEST),
        metric,
        os.path.join( folder %'%s_retinaface_none_all' % PLACES_GALLERY_TEST),
    )
    print(cmc, mAP)
    if compression:
        print('compresion')
        metric = "%s + %s" %('tsne', metric)
    #repository.addTest("AlignedReId + Retinaface", "None", "VGG-Face", metric, cmc, mAP, PLACES_PROBE_TEST, PLACES_GALLERY_TEST)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", action='store', type=str, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, help="introduce the model")
    parser.add_argument("--all", action='count', help="test with all models and metrics")
    parser.add_argument("--aligenReId", action='count', help="using only body information")
    parser.add_argument("--pca", action='count', help="apply pca to reduction the dimensions")


    args = parser.parse_args()
    if args.aligenReId:
        identificationByBody(args.metric, args.pca)
    else:
        if not args.all:
           indentificationByFaces(args.database, args.model, args.metric)
        else:
            hastag = "#" * 10
            for model in MODELS:
                for metric in METRICS:
                    print("%s - %s + %s - %s" %(hastag, model, metric, hastag))
                    indentificationByFaces(args.database, model, metric)

        #print("%s - [ Ensemble ] - %s" %(hastag, hastag))
        #indentification(args.database, "Ensemble")