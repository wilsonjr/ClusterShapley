import _cluster_shapley

import shap
import random

import numpy as np
import pandas as pd

from scipy 					 import linalg
from sklearn.model_selection import train_test_split
from sklearn.preprocessing   import normalize

class ClusterShapley:

    def __init__(self, verbose=True, background_size=0.8, splits=10):

        self.X = None
        self.y = None

        self.unique_labels = None
        self.centroids = None 

        self.explainer = None

        self.verbose = verbose
        self.background_size = background_size
        self.splits = splits

        assert background_size <= 1.0

    def fit(self, X, y):

        if self.verbose:
            print("Preprocessing data...")

        self._preprocess_data(X, y)

        train_x, test_x, train_y, test_y = train_test_split(self.X, self.y, test_size=1.0-self.background_size, random_state=0)

        if self.verbose:
            print("Creating summary of the background dataset...")

        train_summary = shap.kmeans(train_x, self.splits)

        if self.verbose:
            print("Computing explanations...")        

        self.explainer = shap.KernelExplainer(self._predict_proba, train_summary)

    def transform(self, X):
        shap_values = self.explainer.shap_values(X)
        return np.array(shap_values)

    def _preprocess_data(self, X, y):

        self.X = X
        self.y = y
        self.unique_labels = np.unique(self.y)
        
        self.centroids = np.zeros((len(self.unique_labels), self.X.shape[1]))
        
        for i, label in enumerate(self.unique_labels):
            X_label = self.X[y == label]
            self.centroids[i] = X_label.mean(axis=0)


    def _predict_proba(self, x):
        distances = np.zeros((len(x), self.centroids.shape[0]))

        fast_cs = _cluster_shapley.ClusterShapley()
        distances = fast_cs.compute_distances(x, self.centroids)
        
        # for k in range(distances.shape[0]):
        #     for i in range(distances.shape[1]):
        #         distances[k, i] = np.linalg.norm(self.centroids[i]-x[k])
        
        distances = normalize(distances, 'l1')
        
        return distances


    def num_clusters(self):
        return self.unique_labels.shape[0]

