MODELS  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
METRICS = ['cosine', 'euclidean', 'euclidean_l2']
PLACES  = ["Arucas","Teror", "PresaDeHornos",  "Ayagaures", "ParqueSur" ] # sorted by run's control point
FACES_MODELS = ["retinaface","retinafaceliif50", "retinafaceliif100", "retinafaceliif300",
                "img2pose", "img2poseliif50", "img2poseliif100", "img2poseliif300"]
HEURISTICS = ["none", "dimension"]

PLACES_PROBE_TEST   = "ParqueSur"
PLACES_GALLERY_TEST = "Ayagaures"

COMPRESSION_FACTOR = 0.95

#from enum import Enum

#compressionMethod = Enum('compressionMethod', 'none pca tsne')