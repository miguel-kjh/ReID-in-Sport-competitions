from Domain.Face import Face
from Domain.FacesCollection import FacesCollection
from Services.FacesLocator import FacesLocator
from img2pose.img2pose import img2poseModel
from img2pose.model_loader import load_model
from PIL import Image
from torchvision import transforms
import numpy as np
from Utils.constant import FACE_ENHANCEMENT_FACTOR


class Img2PoseLocatorService(FacesLocator):

    def __init__(self):
        self.transform = transforms.Compose([transforms.ToTensor()])
        DEPTH = 18
        MAX_SIZE = 1400
        MIN_SIZE = 600

        POSE_MEAN = "img2pose/models/WIDER_train_pose_mean_v1.npy"
        POSE_STDDEV = "img2pose/models/WIDER_train_pose_stddev_v1.npy"
        MODEL_PATH = "img2pose/models/img2pose_v1.pth"

        pose_mean = np.load(POSE_MEAN)
        pose_stddev = np.load(POSE_STDDEV)

        threed_points = np.load('img2pose/pose_references/reference_3d_68_points_trans.npy')

        self.img2pose_model = img2poseModel(
            DEPTH, MIN_SIZE, MAX_SIZE,
            pose_mean=pose_mean, pose_stddev=pose_stddev,
            threed_68_points=threed_points,
        )
        load_model(
            self.img2pose_model.fpn_model,
            MODEL_PATH,
            cpu_mode=str(self.img2pose_model.device) == "cpu", model_only=True
        )
        self.img2pose_model.evaluate()
        self.threshold = 0.8


    def _createFaces(self, bboxes: list, res: dict) -> FacesCollection:
        collection = FacesCollection(model = "Img2Pose")
        for index, box in enumerate(bboxes):
            if res["scores"][index] > self.threshold:
                posX   = round(box[0])
                #if posX < 0: posX = 0
                posY   = round(box[1])
                #if posY < 0: posY = 0
                width  = round(box[2])
                height = round(box[3])
                score  = res["scores"][index].cpu().item()
                collection.addFace(Face(index, posX, posY, width, height, score))
        return collection

    def locate(self, file: str) -> FacesCollection:
        img = Image.open(file).convert("RGB")
        res = self.img2pose_model.predict([self.transform(img)])[0]

        all_bboxes = res["boxes"].cpu().numpy().astype('float')

        return self._createFaces(all_bboxes, res)