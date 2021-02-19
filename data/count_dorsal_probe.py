from Utils.fileUtils import getNumber, isImage, extractModelAndHeuristics
from Utils.constant import PLACES
from shutil import copyfile
import os
import collections

DATABASE = 'TGC_places'


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
    dorsals  = countDorsal(DATABASE)
    dorsalsRepeated = extractRepeatedDorsal(dorsals)

    for dirpath, _, filenames in os.walk(DATABASE):
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

def createGalleries(probe):

    model, heuristics = extractModelAndHeuristics(probe)
    gallery = "Gallery_faces_%s_%s" %(model, heuristics)
    os.mkdir(gallery)
    for place in ["ParqueSur"]:
        gallery_place = os.path.join(gallery, place)
        os.mkdir(gallery_place)
        base_folder = os.path.join(DATABASE, place)

        _, _, filenames_probe = next(os.walk(os.path.join(probe, "Ayagaures")))
        dorsalList = [getNumber(filename) for filename in filenames_probe]
        _, _, filenames_gallery = next(os.walk(base_folder))
        filter_filenames_gallery = [filename for filename in filenames_gallery
                                    if isImage(filename) and
                                    getNumber(filename) in dorsalList]

        for file in filter_filenames_gallery:
            copyfile(os.path.join(base_folder, file), os.path.join(gallery_place, file))

if __name__ == '__main__':
    #modifyGallery()
    #modifyProbes()
    createGalleries("Probe_faces_retinaface_dimension")