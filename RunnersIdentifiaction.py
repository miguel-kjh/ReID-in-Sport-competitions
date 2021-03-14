import argparse
import os

from Controller.RecognitionsController import RecognitionsController
from Services.ReidentificationRepository import ReidentificationRepository
from Utils.fileUtils import extractModelAndHeuristics
from Utils.constant import PLACES_PROBE_TEST, PLACES_GALLERY_TEST, MODELS, METRICS, PLACES


def printResults(cmc, mAP):
    print("rank 1:", cmc[0])
    print("rank 5:", cmc[4])
    print("mAP(%):", round(mAP*100,4))


def indentificationByFaces(database, model, metric):
    rs = RecognitionsController()
    repository = ReidentificationRepository()

    cmc, mAP = rs.identificationRunnersByFaces(
        os.path.join(database, PLACES_PROBE_TEST),
        model,
        metric,
        os.path.join(database, PLACES_GALLERY_TEST)
    )
    faceModel, heuristic = extractModelAndHeuristics(database)
    printResults(cmc, mAP)
    repository.addTest(faceModel, heuristic, model, metric, cmc, mAP, PLACES_PROBE_TEST, PLACES_GALLERY_TEST)

def identificationByBody(metric, compression):
    rs = RecognitionsController()
    repository = ReidentificationRepository()
    folder = "data/TCG_alignedReId/%s.pkl" if not compression else "data/TCG_alignedReId/%s_pca.pkl"
    nameMetric = metric

    if compression:
        nameMetric = "%s + %s" %('pca', nameMetric)

    for probe in PLACES:
        for gallery in PLACES:
            if probe != gallery:
                print("[ %s - %s]" % (probe, gallery))
                cmc, mAP = rs.identificationRunnersByBody(
                    os.path.join(folder %probe),
                    metric,
                    os.path.join(folder %gallery)
                )
                repository.addTest("AlignedReId", "None", "ResNet50", nameMetric, cmc, mAP, probe, gallery)

def identificationByBodyAndFaces(model, heuristics, metric, embedding, compression):
    rs = RecognitionsController()
    repository = ReidentificationRepository()
    folder = "data/TCG_alignedReId/%s.pkl" if not compression else "data/TCG_alignedReId/%s_pca.pkl"

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
        os.path.join( folder %'%s_%s_%s_%s' % (PLACES_PROBE_TEST, model, heuristics, embedding)),
        metric,
        os.path.join( folder %'%s_%s_%s_%s' % (PLACES_GALLERY_TEST, model, heuristics, embedding)),
    )
    printResults(cmc, mAP)
    if compression:
        metric = "%s + %s" %('pca', metric)
    repository.addTest("AlignedReId + Retinaface", "None", "VGG-Face", metric, cmc, mAP, PLACES_PROBE_TEST, PLACES_GALLERY_TEST)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", action='store', type=str, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, help="introduce the metric")
    parser.add_argument("--heu", action='store', type=str, help="introduce the heuristic")
    parser.add_argument("--emb", action='store', type=str, help="introduce the heuristic")
    parser.add_argument("--all", action='count', help="test with all models and metrics")
    parser.add_argument("--aligenReId", action='count', help="using only body information")
    parser.add_argument("--combine", action='count', help="using only body information")
    parser.add_argument("--pca", action='count', help="apply pca to reduction the dimensions")


    args = parser.parse_args()
    if args.aligenReId:
        identificationByBody(args.metric, args.pca)
    elif args.combine:
        identificationByBodyAndFaces(args.model, args.heu, args.metric, args.emb, args.pca)
    else:
        if not args.all:
           indentificationByFaces(args.database, args.model, args.metric)
        else:
            hastag = "-" * 5
            for model in MODELS:
                for metric in METRICS:
                    print("%s - %s + %s - %s" %(hastag, model, metric, hastag))
                    indentificationByFaces(args.database, model, metric)

        #print("%s - [ Ensemble ] - %s" %(hastag, hastag))
        #indentification(args.database, "Ensemble")