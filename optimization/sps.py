from pymoo.model.sampling import Sampling
import numpy as np
import random

class SPS(Sampling):

    def __init__(self, sparsity, sampled_mask=[]):
        self.sparsity = sparsity
        self.sampled_mask = sampled_mask

    def _do(self, problem, n_samples, **kwargs):

        X = np.zeros((n_samples, len(problem.xl)))

        for row in range(np.size(X,0)):

            # Where to put the samples 
            genome_size = np.shape(X)[1]
            indices = random.sample(range(genome_size), round(genome_size*self.sparsity))

            # Include any indices that alwasy need to be non-zero
            indices = list(set(indices).union(self.sampled_mask))
            indices = np.array(indices) 

            ranges = problem.xu - problem.xl
            
            indices_len = np.size(indices,0)
            # Put those samples in!
            X[row,indices]  = problem.xl[indices] + ranges[indices]*np.random.ranf(indices_len)

        return X


