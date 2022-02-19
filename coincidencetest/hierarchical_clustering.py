import scipy
from scipy.cluster import hierarchy
import numpy as np
import pandas as pd


def gather_hierarchical_clusters(data):
    """
    First discover feature clusters in the data matrix, then assess them
    using the coincidence test.

    Parameters
    ----------
    data : pandas.DataFrame
        A numeric data matrix, with feature names.
    feature_names : list
        The string names of the features.

    Returns
    -------
    signatures : pandas.DataFrame
        Table of clusters found, with frequency of occurrence and p-value for test.
    """
    feature_names = list(data.columns)
    data_matrix = data.to_numpy()
    linkage = hierarchy.linkage(data_matrix.transpose(), method='ward')

    clusters = {}
    n = linkage.shape[0] + 1
    for i in range(linkage.shape[0]):
        set0_index = int(linkage[i, 0])
        if set0_index < n:
            set0 = [set0_index]
        else:
            set0 = clusters[set0_index]

        set1_index = int(linkage[i, 1])
        if set1_index < n:
            set1 = [set1_index]
        else:
            set1 = clusters[set1_index]

        cluster_index = int(n + i)
        clusters[cluster_index] = sorted(list(set(set0).union(set(set1))))

    named_clusters = {
        int(index) : [feature_names[i] for i in cluster]
        for index, cluster in clusters.items()
    }

    binary_data = pd.DataFrame(binarize(data_matrix), columns=feature_names)
    sums = binary_data.apply(lambda row : sum(row), axis=0)
    incidences = {
        index : count_incidence(cluster, binary_data) for index, cluster in named_clusters.items()
    }
    gathered = {
        'number of samples' : binary_data.shape[0],
        'number of features' : binary_data.shape[1],
        'frequencies' : dict(sums),
        'groups' : [{
                'signature' : cluster,
                'number of samples' : incidences[index],
            } for index, cluster in named_clusters.items() if len(cluster) > 1 and incidences[index] > 1
        ],
    }
    return gathered


def binarize(data):
    """
    Parameters
    ----------
    data : numpy.ndarray
        Input numeric data matrix.

    Returns
    -------
    data : numpy.ndarray
        Thresholded matrix with values 0 or 1, obtained using means for each
        feature.
    """
    number_samples = data.shape[0]
    means = [
        sum(column) / number_samples
        for column in data.transpose()
    ]
    return np.array([
        [0 if entry < means[i] else 1 for i, entry in enumerate(row)]
        for row in data
    ])


def count_incidence(cluster, binary_data):
    """
    Parameters
    ----------
    cluster : list
        List of indices for features (columns) of the data matrix.
    binary_data : pandas.DataFrame
        The data matrix.

    Returns
    -------
    incidence : int
        The frequency displayed simultaneously by all features of the cluster.
    """
    restriction = binary_data[cluster]
    number_features = restriction.shape[1]
    sums = [sum(row) for index, row in restriction.iterrows()]
    incidence = len([s for s in sums if s == number_features])
    return incidence
