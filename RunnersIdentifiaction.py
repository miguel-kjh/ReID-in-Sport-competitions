import argparse
import os

from Controller.FacesRecognitionsController import FacesRecognitionsController

def indentification(database, model, metric):
    rs = FacesRecognitionsController()
    print(
        rs.identificationPeople(
            database,
            model,
            metric
        )
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", action='store', type=str, required=True, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, required=True,  help="introduce the model")
    parser.add_argument("--metric", action='store', type=str, required=True,  help="introduce the model")
    args = parser.parse_args()
    indentification(args.database, args.model, args.metric)