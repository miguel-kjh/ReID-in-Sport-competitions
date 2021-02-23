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

def identificationByBody(metric):
    rs = RecognitionsController()
    repository = ReidentificationRepository()

    """for probe in PLACES:
        for gallery in PLACES:
            if probe != gallery:
                print("[ %s - %s]" % (probe, gallery))
                cmc, mAP = rs.identificationRunnersByBody(
                    os.path.join("data/TCG_alignedReId/%s.pkl" %probe),
                    metric,
                    os.path.join("data/TCG_alignedReId/%s.pkl" %gallery)
                )

                repository.addTest("AlignedReId", "None", "ResNet50", metric, cmc, mAP, probe, gallery)"""
    cmc, mAP = rs.identificationRunnersByBody(
        os.path.join("data/TCG_alignedReId/%s.pkl" %PLACES_PROBE_TEST),
        metric,
        os.path.join("data/TCG_alignedReId/%s.pkl" %PLACES_GALLERY_TEST)
    )

    repository.addTest("AlignedReId", "None", "ResNet50", metric, cmc, mAP, PLACES_PROBE_TEST, PLACES_GALLERY_TEST)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", action='store', type=str, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, help="introduce the model")
    parser.add_argument("--all",action='count', help="test with all models and metrics")
    parser.add_argument("--aligenReId", action='count', help="using only body information")
    args = parser.parse_args()
    if args.aligenReId:
        identificationByBody(args.metric)
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