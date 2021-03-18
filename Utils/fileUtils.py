import re
import os
import shutil
from datetime import timedelta

def isImage(filename: str):
    return re.search(".jpg$", filename)

def getTime(filename: str) -> timedelta:
    matchs = re.findall(r'(\d{2})', filename)
    step = 1 if len(matchs) == 5 else 0
    return timedelta(hours = int(matchs[0 + step]), minutes = int(matchs[1 + step]), seconds = int(matchs[2 + step]))

def getPlace(filename: str) -> str:
    match = re.search(r'\d+_(\w+)_frame', filename)
    return match.group(1)

def getNumber(filename: str) -> int:
    match = re.search(r'^\d+', filename)
    return int(match.group(0))

def findFile(file: str, folder: str) -> int:
    for _, _, filenames in os.walk(folder):
        try:
            return filenames.index(file)
        except:
            return None
    raise RuntimeError("File not found")

def createFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

def extractModelAndHeuristics(folderName: str) -> tuple:
    split = folderName.replace(r'/', "").split("_")
    model = split[-2]
    heuristic = split[-1]
    return model,heuristic