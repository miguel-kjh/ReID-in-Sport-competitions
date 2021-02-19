import numpy as np
import pandas as pd

class ReidentificationRepository:


    def __init__(self):

        self.filename = 'data/Results/ReidentificationTests.csv'
        self.df: pd.DataFrame = pd.read_csv(self.filename)

    def _getQuery(self, faceModel: str, heuristics: str, identificationModel: str,
                  metric: str,  probe_place: str, gallery_place: str) -> str:

        return 'Face_Model =="%s" and Heuristics =="%s" and Identification_Model =="%s" ' \
               'and Metric =="%s"  and Probe_place == "%s" and Gallery_place == "%s"' \
               % (faceModel, heuristics, identificationModel, metric, probe_place, gallery_place)

    def _save(self):

        self.df = self.df.loc[:,~self.df.columns.str.match("Unnamed")]
        self.df.to_csv(self.filename)

    def addTest(self, faceModel: str, heuristics: str, identificationModel: str, metric: str,
                values: np.array, mAP: float, probe_place: str, gallery_place: str):

        queryResult = self.df.query(self._getQuery(faceModel, heuristics, identificationModel, metric, probe_place, gallery_place),
                                    inplace = False)

        values = ",".join(map(lambda x: str(x), list(values)))

        if queryResult.empty:

            row = {'Face_Model': faceModel,
             'Heuristics': heuristics,
             'Identification_Model': identificationModel,
             'Metric': metric if identificationModel != 'Ensemble' else None,
             'Values': values,
             'Probe_place': probe_place,
             'Gallery_place': gallery_place,
             'mAP': mAP}
            self.df = self.df.append(row, ignore_index=True)
            self._save()

        else:

            self.df.iloc[queryResult.index,  self.df.columns.get_loc('Values')]  = values
            self.df.iloc[queryResult.index,  self.df.columns.get_loc('mAP')]     = mAP
            self._save()