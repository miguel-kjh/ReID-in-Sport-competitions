from Controller.AlignedReIDController import AlignedReIDController


FOLDER = "data/TGC_places"
controller = AlignedReIDController()

def computeEmbeddings():
    controller.computedEmbeddings(FOLDER, compression=True)

def computeBodyAndFacesEmbeddings(faces, bodies, filename):
    controller.compactedEmbeddings(faces, bodies, filename)

if __name__ == '__main__':
    #computeEmbeddings()
    computeBodyAndFacesEmbeddings(
        'data/Probe_faces_retinaface_none/Ayagaures/representations_facenet.pkl',
        'data/TCG_alignedReId/Ayagaures.pkl',
        'Ayagaures_retinface_none'
    )