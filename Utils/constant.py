MODELS  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
METRICS = ['cosine', 'euclidean', 'euclidean_l2']
PLACES  = ["Arucas", "Ayagaures", "ParqueSur", "PresaDeHornos", "Teror"]

PLACES_PROBE_TEST   = "ParqueSur"
PLACES_GALLERY_TEST = "Ayagaures"

COMPRESSION_FACTOR = 0.95

from enum import Enum

compressionMethod = Enum('compressionMethod', 'none pca tsne')