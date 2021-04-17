import numpy as np

class SFT(object):
    def __init__(self, sigma=0.1):
        self.sigma = sigma

    def __call__(self, emb_org):
        emb_org_norm = np.linalg.norm(emb_org, 2, 1).reshape((-1, 1)).clip(min=1e-12)
        emb_org_norm = emb_org / emb_org_norm
        W = np.matmul(emb_org_norm, emb_org_norm.T)
        W = W / float(self.sigma)

        W_exp = np.exp(W - np.max(W, axis=1))
        T = W_exp / np.sum(W_exp, axis=1).reshape((-1, 1))
        emb_sft = np.matmul(T, emb_org)
        return emb_sft

import pickle
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from Domain.BodyCollection import BodyCollection
import os

def get_embeddings(file) -> BodyCollection:
    with open(file, 'rb') as f:
        data = pickle.load(f)

    return data

def TSNE_plot(data, classes, title):
    X_embedded = TSNE(n_components=2).fit_transform(data)
    plt.scatter(X_embedded[:,0], X_embedded[:,1], c = classes)
    plt.title(title)
    plt.show()

def saveBodyInformation(file: str, collection) -> None:
    with open(file, 'wb') as output:
        pickle.dump(collection, output, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    sft_np_op = SFT(sigma=0.05)
    ps = "../data/TCG_alignedReId/ParqueSur.pkl"
    ay = "../data/TCG_alignedReId/Ayagaures.pkl"

    bc = get_embeddings(ps)
    emb,cls = bc.get_dataset()
    sft = sft_np_op(emb)
    print(cls)
    TSNE_plot(sft, cls, 'PS')
    bc.set_embeddings(sft)
    #saveBodyInformation(ps, bc)

    bc = get_embeddings(ay)
    emb,cls = bc.get_dataset()
    sft = sft_np_op(emb)
    TSNE_plot(sft, cls, 'AY')
    bc.set_embeddings(sft)
    #saveBodyInformation(ay, bc)