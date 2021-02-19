from Controller.AlignedReIDController import AlignedReIDController


FOLDER = "data/TGC_places"

def computeEmbeddings():
    controller = AlignedReIDController()

    controller.run(FOLDER)


if __name__ == '__main__':
    computeEmbeddings()