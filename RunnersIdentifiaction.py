import argparse
import os

from Controller.FacesRecognitionsController import FacesRecognitionsController
from Services.ReidentificationRepository import ReidentificationRepository
from Utils.Utils import extractModelAndHeuristics
from Utils.constant import PLACES, MODELS, METRICS



def indentification(database, model, metric):
    rs = FacesRecognitionsController()
    repository = ReidentificationRepository()
    for probe_place in PLACES:
        for gallery_place in PLACES:
            if probe_place != gallery_place:
                values, mAptop_1, mAptop_5 = rs.identificationPeople(
                    os.path.join(database, probe_place),
                    model,
                    metric,
                    gallery_place
                )
                faceModel, heuristic = extractModelAndHeuristics(database)
                repository.addTest(faceModel, heuristic, model, metric, values,  mAptop_1, mAptop_5, probe_place, gallery_place)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", action='store', type=str, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, help="introduce the model")
    parser.add_argument("--all",action='count', help="test with all models and metrics")
    args = parser.parse_args()
    if not args.all:
       indentification(args.database, args.model, args.metric)
    else:
        hastag = "#" * 10
        for model in MODELS:
            for metric in METRICS:
                print("%s - %s + %s - %s" %(hastag, model, metric, hastag))
                indentification(args.database, model, metric)

        #print("%s - [ Ensemble ] - %s" %(hastag, hastag))
        #indentification(args.database, "Ensemble")