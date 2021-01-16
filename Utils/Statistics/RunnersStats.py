class RunnerStats:

    def __init__(self, dorsal: int):
        self.dorsal = dorsal
        self.target = {
            "Arucas": [],
            "Ayagaures": [],
            "ParqueSur": [],
            "PresaDeHornos": [],
            "Teror": []
        }

    def addPosition(self, place: str, position: int):
        self.target[place].append(position)

    def __repr__(self):
        return "%i - %s" %(self.dorsal, self.target)

class RunnersStats:

    def __init__(self):
        self.runners = []

    def addRunner(self, dorsal):
        self.runners.append(RunnerStats(dorsal))

    def addPosition(self, dorsal, place, position):
        self.runners[dorsal][place].append(position)

    def isRunner(self, dorsal) -> bool:
        return len(list(filter(lambda runner: runner.dorsal == dorsal, self.runners))) > 1