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

def modifyGallery():
    database = 'TGC_places'
    dorsals  = countDorsal(database)
    dorsalsRepeated = extractRepeatedDorsal(dorsals)

    for dirpath, _, filenames in os.walk(database):
        for file in filenames:
            if isImage(file) and getNumber(file) not in dorsalsRepeated:
                os.remove(os.path.join(dirpath,file))

def modifyProbes():
    probes = ['Probe_faces_img2pose_dimension', 'Probe_faces_img2pose_none',
              'Probe_faces_retinaface_dimension', 'Probe_faces_retinaface_none']

    database = 'TGC_places'
    dorsals  = countDorsal(database)
    dorsalsRepeated = extractRepeatedDorsal(dorsals)
    print(dorsalsRepeated)

    for probe in probes:
        for dirpath, _, filenames in os.walk(probe):
            for file in filenames:
                if isImage(file) and getNumber(file) not in dorsalsRepeated:
                    os.remove(os.path.join(dirpath, file))

if __name__ == '__main__':
    #modifyGallery()
    modifyProbes()