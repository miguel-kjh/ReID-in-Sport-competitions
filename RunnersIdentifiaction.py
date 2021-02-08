import argparse

from Controller.FacesRecognitionsController import FacesRecognitionsController
from Services.ReidentificationRepository import ReidentificationRepository
from Utils.Utils import extractModelAndHeuristics

MODELS  = ["VGG-Face", "Facenet", "OpenFace"]
METRICS = ['cosine', 'euclidean', 'euclidean_l2']

def indentification(database, model, metric = "cosine"):
    rs = FacesRecognitionsController()
    repository = ReidentificationRepository()
    values, mAptop_1, mAptop_5 = rs.identificationPeople(
        database,
        model,
        metric
    )
    print(mAptop_1, mAptop_5)
    faceModel, heuristic = extractModelAndHeuristics(database)
    repository.addTest(faceModel, heuristic, model, metric, values,  mAptop_1, mAptop_5)

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