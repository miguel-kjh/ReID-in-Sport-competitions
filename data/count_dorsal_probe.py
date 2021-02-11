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

    """for key, elements in dorsals.items():
        print(key)
        print(len(dorsals[key]))
        dorsals[key] = list(filter(
            lambda dorsal: dorsal in dorsalsRepeated,
            elements
        ))
        print(len(dorsals[key]))"""

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            if isImage(file) and getNumber(file) not in dorsalsRepeated:
                os.remove(os.path.join(dirpath,file))



if __name__ == '__main__':
    main()

    # TDD
    # {[]} -> []
    # [1,1,2], [4,5,6] -> []
    # [1,1,2], [1,2,3] -> [1,2]
    # [1,1,2], [1,3,2], [1,2,4,5,6] -> [1,2]
    # [1,1,2], [3,3,3], [3,3,4,5,6] -> []
    print(extractRepeatedDorsal({}) == [])
    print(extractRepeatedDorsal({
        "a": [1,1,2],
        "b": [4,5,6]
    }) == [])
    print(extractRepeatedDorsal({
        "a": [1,1,2],
        "b": [1,2,3]
    }) == [1,2])
    print(extractRepeatedDorsal({
        "a": [1,1,2],
        "b": [1,3,2],
        "c": [1,2,4,5,6]
    }) == [1,2])
    print(extractRepeatedDorsal({
        "a": [1,1,2],
        "b": [3,3,3],
        "c": [3,3,4,5,6]
    }) == [])