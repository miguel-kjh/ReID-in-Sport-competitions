import cv2
from IPython.display import display, Javascript
from base64 import b64decode
from PIL import Image
import numpy as np

from matplotlib import pyplot as plt
from retinaface.pre_trained_models import get_model
from retinaface.utils import vis_annotations

class FindFacesServices:
    pass