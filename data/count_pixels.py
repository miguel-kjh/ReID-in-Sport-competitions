import matplotlib.pyplot as plt
import os
import json

model     = "retinaface"
heuristic = "none"
database  = "TGC2020v0.3_json_%s_%s" %(model, heuristic)

def pixelsCount():

    pixels_count = []

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            with open(os.path.join(dirpath, file)) as f:
                faces = json.load(f)

            pixels_count[len(pixels_count):] = list(
                map(lambda key: abs(faces['faces'][key]['height'] - faces['faces'][key]['posY']), faces['faces'])
            )

    return pixels_count

def printBar(data: dict):
    plt.bar(data.keys(), data.values())
    plt.title(
        "%s height of images" %model
    )
    plt.show()

def filterPixels(cond, pixels):
    return len(list(filter(cond, pixels)))


if __name__ == '__main__':
    pixels_count = pixelsCount()
    print(len(pixels_count))
    cutPoints = range(15,300,15)


    data = {
        "%s" % cutPoints[index]: filterPixels(lambda x: cutPoints[index - 1] < x < cutPoints[index], pixels_count)
        for index in range(1,len(cutPoints))
    }
    data[">= 300"] = filterPixels(lambda x: x >= 300, pixels_count)
    printBar(data)