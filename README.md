.. -*- mode: rst -*-

|pypi_version|_ |pypi_downloads|_

.. |pypi_version| image:: https://img.shields.io/pypi/v/cluster-shapley.svg
.. _pypi_version: https://pypi.python.org/pypi/cluster-shapley/

.. |pypi_downloads| image:: https://pepy.tech/badge/cluster-shapley/month
.. _pypi_downloads: https://pepy.tech/project/cluster-shapley

=====
ClusterShapley
=====

ClusterShapley is a technique to explain non-linear dimendionality reduction results. You can explain the cluster formation after reducing the dimensionality to 2D. Read the `preprint <https://arxiv.org/abs/2103.05678>`_ or `publisher <https://doi.org/10.1016/j.eswa.2021.115020>`_ versions for further details.

-----------
Installation
-----------

ClusterShapley depends upon common machine learning libraries, such as ``scikit-learn`` and ``NumPy``. It also depends on SHAP.

Requirements:

* shap
* numpy
* scipy
* scikit-learn
* pybind11

If you have these requirements installed, use PyPI:

.. code:: bash

    pip install cluster-shapley

--------------
Usage examples
--------------

ClusterShapley package follows the same idea of sklearn classes, in which you need to fit and transform data.

**Explaining cluster formation**

Suppose you want to investigate the decisions of a dimensionality reduction (DR) technique to impose a projection on 2D. The first thing to do is to project the dataset.

.. code:: python
	
	import umap
	
	import matplotlib.pyplot as plt

	from sklearn.datasets import load_iris


	data = load_iris()
	X, y = data.data, data.target

	reducer = umap.UMAP(verbose=0, random_state=0)
	embedding = reducer.fit_transform(X)
	plt.scatter(embedding[:, 0], embedding[:, 1], c=y)

.. image:: docs/artwork/iris.png
	:alt: UMAP embedding of the Iris dataset

**Compute explanations**

Now, you can generate explanations to understand why UMAP (or any other DR technique) imposed that cluster formation.

.. code:: python

	import random
	import numpy as np
	# our library
	import dr_explainer as dre


	# fit the dataset
	clusterShapley = dre.ClusterShapley()
	clusterShapley.fit(X, y)

	# compute explanations for data subset 

	to_explain = np.array(random.sample(X.tolist(), int(X.shape[0] * 0.2)))

	shap_values = clusterShapley.transform(to_explain)

The matrix shap_values of shape (3, 30, 4) contains: 
	* the features' contributions for each class (3);
	* upon the samples used to generate explanations (30);
	* for each feature (4).

**Visualize the contributions using SHAP plot**

For now, you can rely on SHAP library to visualize the contributions

.. code:: python

	klass = 0
	c_exp = shap.Explanation(shap_values[klass], data=to_explain, feature_names=data.feature_names)
	shap.plots.beeswarm(c_exp)


.. image:: docs/artwork/explanation_iris0.png
	:alt: Contributions for the embedding of class 0

The plot shows the contributions of each feature for the cohesion of the selected class. Example for 'petal length (cm)':

	* Low feature values (blue) contribute for the cohesion of the selected class.
	* Higher feature values (red) *do not* contribute for the cohesion.


**Defining your own clusters**

Suppose you want to investigate why UMAP clustered 2 classes together while projecting the third one distant in 2D.

To understand that, we can use ClusterShapley to explain how the features contribute to these two major clusters.


.. code:: python

	# fit KMeans with two clusters (see notebooks/ for the complete code)


.. image:: docs/artwork/kmeans_clusters.png
	:alt: Two clusters returned by KMeans on the embedding

Lets generate explanations knowing that cluster 0 is on right and cluster 1 is on left.

.. code:: python

	clusterShapley = dre.ClusterShapley()
	clusterShapley.fit(X, kmeans.labels_)

	shap_values = clusterShapley.transform(to_explain)

	
***For the right cluster***

.. code:: python

	c_exp = shap.Explanation(shap_values[0], data=to_explain, feature_names=data.feature_names)
	shap.plots.beeswarm(c_exp)

.. image:: docs/artwork/explanation0.png
	:alt: Features' contributions for cluster 0

The right cluster is characterized by the low values of petal length (cm), petal width (cm), sepal length (cm).


***For the left cluster***

.. code:: python

	c_exp = shap.Explanation(shap_values[1], data=to_explain, feature_names=data.feature_names)
	shap.plots.beeswarm(c_exp)

.. image:: docs/artwork/explanation1.png
	:alt: Features' contributions for cluster 1

On the other hand, the left cluster (composed by two classes) is characterized by high values of petal length (cm), petal width (cm), sepal length (cm).


--------
Citation
--------

Please, use the following reference to further details and to cite ClusterShapley in your work:

.. code:: bibtex

    @article{MarcilioJr2021_ClusterShapley,
	title = {Explaining dimensionality reduction results using Shapley values},
	journal = {Expert Systems with Applications},
	volume = {178},
	pages = {115020},
	year = {2021},
	issn = {0957-4174},
	doi = {https://doi.org/10.1016/j.eswa.2021.115020},
	url = {https://www.sciencedirect.com/science/article/pii/S0957417421004619},
	author = {Wilson E. Marcílio-Jr and Danilo M. Eler}
	}


-------
License
-------

ClusterShapley follows the 3-clause BSD license.

ClusterShapley uses the open-source SHAP implementation from `SHAP <https://github.com/slundberg/shap>`_.


......



