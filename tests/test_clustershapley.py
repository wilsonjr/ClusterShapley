import shap
import random

import pandas as pd
import numpy as np

import dr_explainer as dre 

from sklearn.datasets import load_iris

def test_clustershapley():

    iris_data = load_iris()

    X, y = iris_data.data, iris_data.target

    to_explain = np.array(random.sample(X.tolist(), int(X.shape[0]*0.2)))
    print(to_explain.shape)

    clusterShapley = dre.ClusterShapley()
    clusterShapley.fit(X, y)

    shap_values = clusterShapley.transform(to_explain)

    assert shap_values.shape == (np.unique(iris_data.target), to_explain.shape[0], to_explain.shape[1])