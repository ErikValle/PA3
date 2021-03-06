import random

import numpy as np
from matplotlib import pyplot as plt

from sklearn.metrics.pairwise import pairwise_kernels
from sklearn.manifold import spectral_embedding
from sklearn.cluster import KMeans
from sklearn import metrics

from spectral_clustering import SpectralClustering

def _generate_three_circle_data():
    pos_list = []
    num_list = [60, 100, 140]
    ground_truth = []
    rd = random.Random()
    # make the result reproducible across multiple run
    rd.seed(0)
    for i in range(1, 4): # radius: 0.1 * i
        for _ in range(num_list[i - 1]):
            r = 0.1 * i + 0.01 * (2 * rd.random() - 1)
            angle = 2 * np.pi * rd.random()
            pos_list.append([r * np.cos(angle), r * np.sin(angle)])
            ground_truth.append(i)
    return (np.asarray(pos_list), np.asarray(ground_truth))

class SpectralAlgorithm(SpectralClustering):
    '''
    kmeans wrapper with plotting support
    '''
    def __init__(self, input_data, n_clusters):
        self.data = input_data
        self.num = self.data.shape[0] # row, n data points
        self.d = input_data[0, :].shape[0]
        super().__init__(n_clusters)

    def fit(self):
        '''
        fit the model with self.data
        '''
        super().fit(self.data)
    # uncomment the following line if you want to use sklearn implementation
    # def train(self, x_train):
    #    self.affinity_matrix_ = pairwise_kernels(x_train, metric='rbf', gamma=self.gamma)
    #    embedding_features = spectral_embedding(self.affinity_matrix_, n_components=self.n_clusters,
    #        norm_laplacian=False, drop_first=False)
    #    kmeans = KMeans(n_clusters=self.n_clusters)
    #    kmeans.fit(embedding_features)
    #    self.labels_ = kmeans.labels_

    def plot(self, savefig_name):
        color_vector = ['r', 'b', 'g', 'm', 'y', 'c', 'k']
        if self.n_clusters >= 7:
            raise NotImplementedError("plot routine for k >=7 is not implemented")
        if self.d != 2: # this function can only be used for d = 2
            raise NotImplementedError("plot routine for dimension larger than 2 is not implemented")
        for i in range(self.n_clusters):
            category_i = np.where(self.labels_ == i)[0]
            plt.scatter(self.data[category_i, 0], self.data[category_i, 1], color=color_vector[i])

        plt.savefig(savefig_name)
        plt.show()

if __name__ == '__main__':
    X, y = _generate_three_circle_data()
    sp = SpectralAlgorithm(X, 3)
    max_score = 0
    start_gamma = 1
    end_gamma = 2000
    optimal_gamma = start_gamma
    gamma_list = np.linspace(start_gamma, end_gamma)
    inertia_list = []
    # linear grid search
    for gamma in gamma_list:
        sp.gamma = gamma
        sp.fit()
        score = metrics.adjusted_rand_score(sp.labels_, y)
        if score > max_score:
            max_score = score
            optimal_gamma = gamma
    print('max score', max_score)
    print('optimal gamma', optimal_gamma)
    sp.gamma = optimal_gamma
    sp.fit()
    print(metrics.adjusted_rand_score(sp.labels_, y))
    sp.plot('spectral-experiment.svg')
