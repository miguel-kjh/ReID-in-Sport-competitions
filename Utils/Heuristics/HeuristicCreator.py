from Utils.Heuristics.FaceHeuristic import *


class HeuristicCreator:

    def __init__(self):
        self.heuristics = {
            "none": NonHeuristic("none"),
            "dimension": DimensionBasedHeuristic("dimension")
        }

    def getHeuristic(self, nameOfHeuristic: str) -> FaceHeuristic:
        return self.heuristics[nameOfHeuristic]