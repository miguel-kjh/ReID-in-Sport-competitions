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
from Utils.fileUtils import getNumber, isImage
from Domain.Body import Body
from Domain.BodyCollection import BodyCollection

class AlignedReIDServices:

    def __init__(self,checkpoint: str = os.path.join("models", "weights", "checkpoint_ep300.pth.tar")):

        # Initialize Cuda device
        os.environ['CUDA_VISIBLE_DEVICES'] = "0"
        self.use_gpu = torch.cuda.is_available()

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

    def imgToEmbedding(self, folder: str) -> dict:

        embeddingCollection = {}

        for dirpath, _, filenames in os.walk(folder):
            collection = BodyCollection()
            place = os.path.basename(dirpath)

            for baseImg in filenames:
                if isImage(baseImg):
                    imgBase = read_image(os.path.join(dirpath, baseImg))
                    imgBase = img_to_tensor(imgBase, self.img_transform)

                    if self.use_gpu:
                        self.model = self.model.cuda()
                        imgBase = imgBase.cuda()

                    self.model.eval()
                    fBase = self.extractor(imgBase)
                    embedding = normalize(pool2d(fBase[0], type='max'))

                    collection.addBody(Body(
                        getNumber(baseImg),
                        embedding
                    ))

            if filenames:
                embeddingCollection[place] = collection

        return embeddingCollection