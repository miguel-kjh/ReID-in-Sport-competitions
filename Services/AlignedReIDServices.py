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

from sklearn.decomposition import PCA
import numpy as np

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

        #compression
        self._compression_factor = 0.95


    def _computedVectors(self, dirpath: str, filenames: list) -> BodyCollection:
        collection = BodyCollection()

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
                    embedding.reshape(embedding.shape[0] * embedding.shape[1]),
                    baseImg
                ))

        return collection

    def _computedVectorsPCA(self, dirpath: str, filenames: list) -> BodyCollection:
        collection = BodyCollection()
        pca = PCA(n_components = self._compression_factor)

        embeddings = []
        runners = []
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

                embeddings.append(embedding.reshape(embedding.shape[0] * embedding.shape[1]))
                runners.append(getNumber(baseImg))

        embeddings = np.array(embeddings)
        print(embeddings.shape)
        embeddings = pca.fit_transform(embeddings)
        print(embeddings.shape)

        for runner, embedding, file in zip(runners, embeddings, filenames):
            collection.addBody(Body(runner, embedding, file))

        return collection

    def imgToEmbedding(self, folder: str, compression: bool = False) -> dict:

        embeddingCollection = {}

        for dirpath, _, filenames in os.walk(folder):
            place = os.path.basename(dirpath)

            if filenames:
                embeddingCollection[place] = self._computedVectorsPCA(dirpath, filenames) \
                    if compression else self._computedVectors(dirpath, filenames)

        return embeddingCollection

    def compactedEmbeddings(self, faces: np.array, bodyCollection: BodyCollection, compression: bool = False) -> None:

        runners = [getNumber(os.path.basename(a[0])) for a in faces]
        dim = len(faces[0][1])

        for body in bodyCollection.bodies:
            try:
                index = runners.index(body.dorsal)
                body.embedding = np.append(body.embedding, faces[index][1])
            except:
                body.embedding = np.append(body.embedding, np.zeros(dim))

        if compression:
            pass