from PIL import Image
import matplotlib.pyplot as plt
import os
import re

database = "data_base_faces"

def isImage(filename: str):
    return re.search(".jpg$", filename)

def main():

    data = {
        "< 200" : 0,
        "< 500" : 0,
        "< 1000" : 0,
        "< 2000" : 0,
        "> 2000" : 0
    }

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            if isImage(file):
                img   = Image.open(os.path.join(dirpath,file))
                count = img.height * img.width
                if count < 200:
                    data["< 200"] += 1
                elif count < 500:
                    data["< 500"] += 1
                elif count < 500:
                    data["< 1000"] += 1
                elif count < 1000:
                    data["< 1000"] += 1
                elif count < 2000:
                    data["< 2000"] += 1
                else:
                    data["> 2000"] += 1

    return data

def printBar(data: dict):
    plt.bar(data.keys(), data.values())
    plt.show()


if __name__ == '__main__':
    printBar(main())