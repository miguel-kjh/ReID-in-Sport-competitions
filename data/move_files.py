import os
import re
from shutil import copyfile

folder = "TGC2020v0.3_PRL"
metrics_folder = "TGC_places"

def _isImage(filename: str):
    return re.search("000.jpg$", filename)

def TGC_places():
    list_news_folders = []
    for index in range(1,822):
        for dirpath, dirnames, filenames in os.walk(os.path.join(folder, str(index))):
            for filename in filenames:
                if _isImage(filename):
                    match = re.search(r'\d+_(\w+)_f', filename)
                    name = match.group(1)
                    fold = os.path.join(metrics_folder, name)
                    if name not in list_news_folders:
                        list_news_folders.append(name)
                        os.mkdir(fold)
                        copyfile(os.path.join(dirpath,filename), os.path.join(fold,filename))
                    else:
                        copyfile(os.path.join(dirpath,filename), os.path.join(fold,filename))
    print(list_news_folders)

def create_probe_by_places(gallery, name_probe):
    pass




if __name__ == '__main__':
    TGC_places()