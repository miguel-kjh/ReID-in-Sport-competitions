import numpy as np
import pandas as pd

class ReidentificationRepository:


    def __init__(self):
        self.filename = 'data/Results/ReidentificationTests.csv'
        self.df: pd.DataFrame = pd.read_csv(self.filename)

    def _getQuery(self, faceModel: str, heuristics: str, identificationModel: str, metric: str) -> str:
        return 'Face_Model =="%s" and Heuristics =="%s" and Identification_Model =="%s" and Metric =="%s"' %(
            faceModel, heuristics, identificationModel, metric
        )

    def _save(self):
        self.df = self.df.loc[:,~self.df.columns.str.match("Unnamed")]
        self.df.to_csv(self.filename)

    def addTest(self, faceModel: str, heuristics: str, identificationModel: str, metric: str,
                values: np.array, mAPtop1: float, mAPtop5: float):
        queryResult = self.df.query(self._getQuery(faceModel, heuristics, identificationModel, metric),
                                    inplace = False)

        values = ",".join(map(lambda x: str(x), list(values)))

        if queryResult.empty:
            row = {'Face_Model': faceModel,
             'Heuristics': heuristics,
             'Identification_Model': identificationModel,
             'Metric': metric,
             'Values': values,
             'mAPtop1': mAPtop1,
             'mAPtop5': mAPtop5}
            self.df = self.df.append(row, ignore_index=True)
            self._save()
        else:
            self.df.iloc[queryResult.index,  self.df.columns.get_loc('mAPtop1')] = mAPtop1
            self.df.iloc[queryResult.index,  self.df.columns.get_loc('mAPtop5')] = mAPtop5
            self.df.iloc[queryResult.index,  self.df.columns.get_loc('Values')]  = values
            self._save()