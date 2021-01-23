from PIL import Image
import matplotlib.pyplot as plt
import os
import json

model     = "retinaface"
heuristic = "none"
database  = "TGC2020v0.3_json_%s_%s" %(model, heuristic)

def main():

    data = {
        "< 10" : 0,
        "< 50" : 0,
        "< 100" : 0,
        "< 150" : 0,
        ">= 150" : 0
    }

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            with open(os.path.join(dirpath, file)) as f:
                faces = json.load(f)

            for key in faces['faces']:
                count = faces['faces'][key]['height']
                if count < 10:
                    data["< 10"] += 1
                elif count < 50:
                    data["< 50"] += 1
                elif count < 100:
                    data["< 100"] += 1
                elif count < 150:
                    data["< 150"] += 1
                else:
                    data[">= 150"] += 1

    return data

def printBar(data: dict):
    plt.bar(data.keys(), data.values())
    plt.title(
        "%s height of images" %model
    )
    plt.show()


if __name__ == '__main__':
    printBar(main())