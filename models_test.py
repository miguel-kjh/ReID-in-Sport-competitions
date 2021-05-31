import sys
sys.path.append('../../')
import numpy as np
import torch
from torchvision import transforms
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm
from PIL import Image, ImageOps
import matplotlib.patches as patches
from scipy.spatial.transform import Rotation
import pandas as pd
from scipy.spatial import distance
import time
import os
import math
import scipy.io as sio
from img2pose.utils.renderer import Renderer
from img2pose.utils.image_operations import expand_bbox_rectangle
from img2pose.utils.pose_operations import get_pose
from img2pose.img2pose import img2poseModel
from img2pose.model_loader import load_model
import re
from time import time

import cv2
from matplotlib import pyplot as plt
from retinaface.pre_trained_models import get_model
from retinaface.utils import vis_annotations

model = get_model("resnet50_2020-07-20", max_size=2048, device = "cuda")
model.eval()

np.set_printoptions(suppress=True)

renderer = Renderer(
    vertices_path="img2pose/pose_references/vertices_trans.npy",
    triangles_path="img2pose/pose_references/triangles.npy"
)

threed_points = np.load('img2pose/pose_references/reference_3d_68_points_trans.npy')

def render_plot(img,image,annot, poses, bboxes):
    (w, h) = img.size

    trans_vertices = renderer.transform_vertices(img, poses)
    img = renderer.render(img, trans_vertices, alpha=1)

    plt.figure(figsize=(8, 8))
    #fig, (ax1, ax2) = plt.subplots(1, 2)

    for bbox in bboxes:
        plt.gca().add_patch(patches.Rectangle((round(bbox[0]), round(bbox[1])), round(bbox[2] - bbox[0]), round(bbox[3] - bbox[1]),linewidth=3,edgecolor='b',facecolor='none'))

    if annot[0]['score'] != -1:
        plt.imshow(vis_annotations(image, annot))
    else:
        plt.imshow(image)
    plt.show()

transform = transforms.Compose([transforms.ToTensor()])

DEPTH = 18
MAX_SIZE = 1400
MIN_SIZE = 600

POSE_MEAN = "img2pose/models/WIDER_train_pose_mean_v1.npy"
POSE_STDDEV = "img2pose/models/WIDER_train_pose_stddev_v1.npy"
MODEL_PATH = "img2pose/models/img2pose_v1.pth"

pose_mean = np.load(POSE_MEAN)
pose_stddev = np.load(POSE_STDDEV)

img2pose_model = img2poseModel(
    DEPTH, MIN_SIZE, MAX_SIZE,
    pose_mean=pose_mean, pose_stddev=pose_stddev,
    threed_68_points=threed_points,
)
load_model(img2pose_model.fpn_model, MODEL_PATH, cpu_mode=str(img2pose_model.device) == "cpu", model_only=True)
img2pose_model.evaluate()

# change to a folder with images, or another list containing image paths
images_path = "data/TGC_places/Teror"

threshold = 0.8

def isImage(filename: str):
    return re.search(".jpg$", filename)

if __name__ == '__main__':
    if os.path.isfile(images_path):
        img_paths = pd.read_csv(images_path, delimiter=" ", header=None)
        img_paths = np.asarray(img_paths).squeeze()
    else:
        img_paths = [
            os.path.join(images_path, img_path)
            for img_path in os.listdir(images_path)
            if isImage(img_path)
        ]
    length = 0
    time_retina = 0
    time_img2pose = 0
    for img_path in tqdm(img_paths):
        length += 1
        img = Image.open(img_path).convert("RGB")
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        start_time = time()
        annotation = model.predict_jsons(image)
        time_retina += time() - start_time
        aumentation_faces = 0
        for i,a in enumerate(annotation[0]['bbox']):
            if i >= 2:
                annotation[0]['bbox'][i] += aumentation_faces
            else:
                annotation[0]['bbox'][i] -= aumentation_faces
                if annotation[0]['bbox'][i] < 0:
                    annotation[0]['bbox'][i] = 0
        image_name = os.path.split(img_path)[1]

        (w, h) = img.size
        image_intrinsics = np.array([[w + h, 0, w // 2], [0, w + h, h // 2], [0, 0, 1]])

        start_time = time()
        res = img2pose_model.predict([transform(img)])[0]
        time_img2pose += time() - start_time

        all_bboxes = res["boxes"].cpu().numpy().astype('float')

        poses = []
        bboxes = []
        for i in range(len(all_bboxes)):
            if res["scores"][i] > threshold:
                bbox = all_bboxes[i]
                pose_pred = res["dofs"].cpu().numpy()[i].astype('float')
                pose_pred = pose_pred.squeeze()

                poses.append(pose_pred)
                bboxes.append(bbox)

        render_plot(img.copy(),image,annotation, poses, bboxes)

    print("Retinaface", time_retina/length)
    print("Img2pose", time_img2pose/length)