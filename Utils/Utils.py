import re
import os

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