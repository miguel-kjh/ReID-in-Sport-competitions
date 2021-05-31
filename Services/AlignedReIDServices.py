from Utils.FeatureExtractor import FeatureExtractor
from Utils.constant import COMPRESSION_FACTOR
from torchvision import transforms
import models
from Utils.utils import *
from sklearn.preprocessing import normalize
from Utils.pool2d import pool2d
from Utils.fileUtils import getNumber, isImage, getTime
from Domain.Body import Body
from Domain.BodyCollection import BodyCollection

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
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
        self._pca = PCA(n_components=COMPRESSION_FACTOR)
        REDUCTION = 3
        self._tsne = TSNE(n_components = REDUCTION)


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
                    getTime(baseImg),
                    baseImg
                ))

        return collection

    def _computedVectorsPCA(self, dirpath: str, filenames: list) -> BodyCollection:
        collection = BodyCollection()

        embeddings = []
        runners = []
        filenames = [file for file in filenames if isImage(file)]
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
        embeddings = self._pca.fit_transform(embeddings)

        for runner, embedding, file in zip(runners, embeddings, filenames):
            collection.addBody(Body(runner, embedding, getTime(file), file))

        return collection

    def imgToEmbedding(self, folder: str, compression: bool = False) -> dict:

        embeddingCollection = {}

        for dirpath, _, filenames in os.walk(folder):
            place = os.path.basename(dirpath)

            if filenames:
                embeddingCollection[place] = self._computedVectorsPCA(dirpath, filenames) \
                    if compression else self._computedVectors(dirpath, filenames)

        return embeddingCollection

    def compactedEmbeddings(self, faces: np.array, bodyCollection: BodyCollection,
                            compression: bool = False) -> None:

        #runners = [getNumber(os.path.basename(a[0])) for a in faces]
        files = [os.path.basename(a[0]) for a in faces]
        newBodyCollection = BodyCollection()
        for body in bodyCollection.bodies:
            aux = body.file.replace('.jpg','')
            ocurrences = sorted([file for file in files if aux in file])
            try:
                index = files.index(ocurrences[0]) #runners.index(body.dorsal)
                face_emb = faces[index][1]
                body.embedding = np.append(body.embedding, face_emb)
                newBodyCollection.addBody(body)
            except:
                continue
                #body.embedding = np.append(body.embedding, np.zeros(dim))


        if compression:
            X, _ = newBodyCollection.get_dataset()
            X = self._pca.fit_transform(X)
            newBodyCollection.set_embeddings(X)

        bodyCollection = newBodyCollection


    def compactedAllEmbeddings(self, faces: list, dimension: int,  bodyCollection: BodyCollection,
                               compression: bool = False) -> None:

        files = [os.path.basename(a[0]) for a in faces[0]]

        for body in bodyCollection.bodies:
            aux = body.file.replace('.jpg','')
            ocurrences = sorted([file for file in files if aux in file])
            try:
                index = files.index(ocurrences[0])
                for face in faces:
                    body.embedding = np.append(body.embedding, face[index][1])
            except:
                body.embedding = np.append(body.embedding, np.zeros(dimension))


        if compression:
            X, _ = bodyCollection.get_dataset()
            X = self._pca.fit_transform(X)
            bodyCollection.set_embeddings(X)

