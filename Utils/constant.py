MODELS  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
METRICS = ['cosine', 'euclidean', 'euclidean_l2']
PLACES  = ["Arucas","Teror", "PresaDeHornos",  "Ayagaures", "ParqueSur" ] # sorted by run's control point
FACES_MODELS = ["retinaface","retinafaceliif50", "retinafaceliif100", "retinafaceliif300",
                "img2pose", "img2poseliif50", "img2poseliif100", "img2poseliif300"]
HEURISTICS = ["none", "dimension"]

PLACES_PROBE_TEST   = "Ayagaures"
PLACES_GALLERY_TEST = "PresaDeHornos"

COMPRESSION_FACTOR = 0.95

FACE_ENHANCEMENT_FACTOR = 25

from datetime import timedelta

timers = [
    timedelta(minutes=10, seconds=16),
    timedelta(hours=6, minutes=34, seconds=50),
    timedelta(hours=3, minutes=28, seconds=56),
    timedelta(hours=1, minutes=17, seconds=25)]

MINIMUM_DURATION = None