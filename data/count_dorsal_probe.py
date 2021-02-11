from Utils.Utils import getNumber,isImage
import os
import collections


def countDorsal(database: str) -> dict:
    places = {}

    for dirpath, _, filenames in os.walk(database):
        if filenames:
            places[dirpath] = list(map(
                lambda file: getNumber(file),
                filter(
                    lambda file: isImage(file),
                    filenames
                )
            ))
    return places

def extractRepeatedDorsal(dorsals: dict) -> list:

    listDorsals = []
    for key, elements in dorsals.items():
        listDorsals[len(listDorsals):] = set(elements)

    return [item for item, count in collections.Counter(listDorsals).items() if count == len(dorsals)]

def main():
    database = 'TGC_places'
    dorsals  = countDorsal(database)
    dorsalsRepeated = extractRepeatedDorsal(dorsals)

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            if isImage(file) and getNumber(file) not in dorsalsRepeated:
                os.remove(os.path.join(dirpath,file))



if __name__ == '__main__':
    main()