import argparse
import os
import numpy as np

from Controller.FacesRecognitionsController import FacesRecognitionsController
from Services.ReidentificationRepository import ReidentificationRepository
from Utils.Utils import extractModelAndHeuristics

def indentification(database, model, metric):
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
    parser.add_argument("--database", action='store', type=str, required=True, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, required=True,  help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, required=True,  help="introduce the model")
    args = parser.parse_args()
    indentification(args.database, args.model, args.metric)