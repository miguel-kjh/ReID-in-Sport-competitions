import torch
import os
from Utils.FeatureExtractor import FeatureExtractor
from torchvision import transforms
from IPython import embed
import models
from scipy.spatial.distance import cosine, euclidean
from Utils.utils import *
from Utils.distance import compute_dist, shortest_dist
from sklearn.preprocessing import normalize
from Utils.pool2d import pool2d

class AlignedReIDServices:

    def __init__(self,
                 folder: str,
                 checkpoint: str = os.path.join("models", "weights", "checkpoint_ep300.pth.tar")
                 ):
        self.folder = folder

        # Initialize Cuda device
        os.environ['CUDA_VISIBLE_DEVICES'] = "0"
        self.use_gpu = torch.cuda.is_available()
        print("Disponibilidad de la GPU: " ,torch.cuda.is_available())

        # Create model
        self.model = models.init_model(name='resnet50', num_classes=751, loss={'softmax', 'metric'}, use_gpu=self.use_gpu,aligned=True)
        checkpoint = torch.load(checkpoint)
        self.model.load_state_dict(checkpoint['state_dict'])

        # name checkpoint
        self.checkpoint = checkpoint

        # FeatureExtractor
        exact_list = ['7']
        self.extractor = FeatureExtractor(self.model, exact_list)

        #Image transforms
        self.img_transform = transforms.Compose([
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def imgToEmbedding(self, baseImg: str) -> dict:

        # Read image from path
        imgBase = read_image(baseImg)
        imgBase = img_to_tensor(imgBase, self.img_transform)

        # Using cuda for compute the image
        if self.use_gpu:
            self.model = self.model.cuda()
            imgBase = imgBase.cuda()

        self.model.eval()
        fBase = self.extractor(imgBase)
        aBase = normalize(pool2d(fBase[0], type='max'))

        print(aBase)
        return {}