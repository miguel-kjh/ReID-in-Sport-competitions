from Utils.Heuristics.FaceHeuristic import *


class HeuristicCreator:

    def __init__(self):
        self.heuristics = {
            "none": NonHeuristic(),
            "dimension": DimensionBasedHeuristic(),
            "score": ScoreBasedHeuristic()
        }

    def getHeuristic(self, nameOfHeuristic: str) -> FaceHeuristic:
        return self.heuristics[nameOfHeuristic]