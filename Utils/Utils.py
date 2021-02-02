import re
import os
import shutil
def isImage(filename: str):
    return re.search(".jpg$", filename)

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