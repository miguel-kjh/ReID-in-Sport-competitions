from Services.FacesRecognitionServices import FacesRecognitionService
from Services.BodyRecognitionServices import BodyRecognitionServices
from Domain.BodyCollection import BodyCollection
from Services.SaveEmbeddingPkl import SaveEmbeddingPkl
from datetime import timedelta
from Utils.fileUtils import getNumber, getTime
from Utils.constant import PLACES, MINIMUM_DURATION, timers
from sklearn.metrics import average_precision_score
from sklearn.ensemble import RandomForestRegressor
from joblib import parallel_backend


import os
import numpy as np
import pandas as pd

class RecognitionsController:

    def __init__(self, databaseFaces: str = ""):
        self._face_recognition = FacesRecognitionService(databaseFaces)
        self._body_recognition = BodyRecognitionServices()
        self.alignedGallery = os.path.join("data", "TCG_alignedReId")
        file_df = os.path.join("data", "tgc_2020_tiempos_pasos_editado.xlsx")
        self._step_time = 16500 #4800
        self._df = pd.read_excel(file_df)
        keys = self._df.keys()
        self._times = list(keys[7:18])
        self._cls_positions = list(keys[18:])
        self._loadServices = SaveEmbeddingPkl(self.alignedGallery)
        self._jobs = 4

        np.random.seed(1000)

    def _calculateAveragePrecision(self, dorsalList: list, dist: list,  query: int) -> float:
        if not dorsalList or query not in dorsalList:
            return 0.

        gallery_match = np.array([1 if i == query else 0 for i in dorsalList])
        dist = np.array(dist)
        similarity = 1 - dist / np.amax(dist)
        return average_precision_score(gallery_match, similarity, average='macro', pos_label=1)

    def _apply_regression(self, time, classification, runners_times, index):
        regr = RandomForestRegressor(max_depth=10, n_estimators=250)
        y = []
        X = []
        for t, c in zip(runners_times, classification):
            y.append(pd.to_timedelta(self._df[t][index]))
            d = self._df[c][index]
            X.append(d)
        y = abs(time - np.array(y))
        y = [y_.total_seconds() for y_ in y]
        X = np.array(X).reshape(-1, 1)
        with parallel_backend('threading', n_jobs = self._jobs):
            regr.fit(X, y)
            seconds = regr.predict(np.array([index+1]).reshape(-1, 1))[0]
        return timedelta(seconds=seconds + self._step_time)

    def _filter_faces_by_regression(self, query, gallery, classification, runners_times, index):
        time = getTime(query)
        delta = self._apply_regression(time, classification, runners_times, index)
        return [sample for sample in gallery if time - delta <= sample[2] <= time + delta]

    def identificationRunnersByFaces(self, probe: str, model: str, metric: str,
                                     galleryPlace: str, topNum: int = 107,
                                     pca: bool = False, temporalCoherence: bool = False,
                                     filling: bool = False, regression: bool = False) -> tuple:

        self._face_recognition.checkMetricAndModel(model, metric)
        probe_places = os.path.basename(probe)

        matches = np.zeros(topNum)
        average_precision = []
        index_probe = PLACES.index(os.path.basename(probe))
        index_gallery = PLACES.index(os.path.basename(galleryPlace))
        isOrder = index_probe < index_gallery

        model_file = "representations_%s.pkl" % (model if not pca else "%s_pca" % model).lower().replace("-", "_")
        probe = os.path.join(probe, model_file)
        gallery = os.path.join(galleryPlace, model_file)

        probes = self._loadServices.loadInformation(probe)
        gallery = [(getNumber(os.path.basename(file)), embedding, getTime(os.path.basename(file)))
                   for file, embedding in self._loadServices.loadInformation(gallery)]
        probes.sort(key = lambda x: getTime(x[0]))

        last_query = getNumber(os.path.basename(probes[0][0]))
        queries_done = []

        for i, query in enumerate(probes):
            dorsal = getNumber(os.path.basename(query[0]))
            gallery_query = gallery

            if regression:
                if last_query != dorsal:
                    if dorsal in queries_done:
                        queries_done.remove(dorsal)
                    queries_done.append(last_query)
                    last_query = dorsal
                index_probe = self._cls_positions.index(probe_places)
                cls = self._cls_positions[:index_probe]
                runners_times = self._times[:index_probe]
                index = list(self._df[probe_places]).index(i + 1)
                gallery_query = [
                    sample
                    for sample in self._filter_faces_by_regression(query[0], gallery, cls, runners_times, index)
                    if sample[0] not in queries_done
                ]

            classification, dist = self._face_recognition.computeClassification(query, gallery_query, model_file,
                                                                          metric = metric,
                                                                          temporalCoherence=temporalCoherence,
                                                                          index=(index_probe, index_gallery),
                                                                          isOrder=isOrder,
                                                                          filledGallery=filling)
            #print(len(classification))
            try:
                matches[classification.index(dorsal)] += 1
            except Exception:
                pass

            average_precision.append(
                self._calculateAveragePrecision(classification, dist, dorsal)
            )

        cmc = np.cumsum(matches) / len(probes)

        return cmc, np.mean(average_precision)

    def _filter_bodies_by_regression(self, query, gallery, classification, runners_times, index):
        delta = self._apply_regression(query.date, classification, runners_times, index)
        return [sample for sample in gallery.bodies if query.date - delta <= sample.date <= query.date + delta]


    def identificationRunnersByBody(self, probe: str, metric: str, galleryPlace: str,
                                    topNum: int = 107, temporalCoherence: bool = False,
                                    filling: bool = False, regression: bool = False, model: str = "") -> tuple:
        matches = np.zeros(topNum)
        average_precision = []
        probe_places = os.path.basename(probe).replace(".pkl", '').split('_')[0]
        index_probe = PLACES.index(probe_places)
        index_gallery = PLACES.index(os.path.basename(galleryPlace).replace(".pkl", '').split('_')[0])
        isOrder = index_probe < index_gallery

        probe = self._loadServices.loadInformation(probe)
        gallery = self._loadServices.loadInformation(galleryPlace)

        queries = probe.bodies
        queries.sort(key = lambda query: query.date)

        last_query = 1
        queries_done = []

        for i, query in enumerate(queries):

            gallery_query = gallery
            if regression:
                if last_query != query.dorsal:
                    if query.dorsal in queries_done:
                        queries_done.remove(query.dorsal)
                    queries_done.append(last_query)
                    last_query = query.dorsal
                index_probe = self._cls_positions.index(probe_places)
                cls = self._cls_positions[:index_probe]
                runners_times = self._times[:index_probe]
                index = list(self._df[probe_places]).index(i + 1)
                gallery_query = BodyCollection(
                    collection=[
                        sample
                        for sample in self._filter_bodies_by_regression(query, gallery, cls, runners_times, index)
                        if sample.dorsal not in queries_done
                    ]
                )

            classification, dist = self._body_recognition.computeClassification(query,
                                                                          gallery_query,
                                                                          metric,
                                                                          temporalCoherence=temporalCoherence,
                                                                          index=(index_probe, index_gallery),
                                                                          isOrder=isOrder,
                                                                          filledGallery=filling,
                                                                          model=model)

            try:
                matches[classification.index(query.dorsal)] += 1
            except Exception:
                pass

            average_precision.append(
                self._calculateAveragePrecision(classification, dist, query.dorsal)
            )

        cmc = np.cumsum(matches) / len(probe.bodies)
        return cmc, np.mean(average_precision)




