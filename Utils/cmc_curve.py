import matplotlib.pyplot as plt
import numpy as np
import os
import json



def showData(data):
    plt.plot(data)
    plt.xlabel("Posicion en el cmc")
    plt.ylabel("Precision")
    plt.grid(True)
    plt.title("Market1501")

    plt.show()


def getCMC(database, maxTopNumber):
    imagecount = 0
    top = np.zeros(maxTopNumber)

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            with open(os.path.join(dirpath,file)) as jsonFile:
                data = json.load(jsonFile)    


            probeNumber = data['instance'][0]["probeRunnerNumber"]
            count = 0
            for instance in data['instance']:
                if probeNumber == instance['galleryRunnerNumber']:
                    break

                count = count +1

            try:
                top[count] += 1
            except IndexError:
                top[-1] +=1

            imagecount += 1

    cmc = np.cumsum(top) / imagecount
    return cmc




if __name__ == '__main__':
    cmc = getCMC("./json_collection/",1000)
    showData(cmc)
    
