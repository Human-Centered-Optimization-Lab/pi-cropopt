from pymoo.core.sampling import Sampling
import numpy as np
import random

class SPS(Sampling):

    def __init__(self, sparsity, base_sampler_class, nz_indices=[], block_xu=None, block_xl=None,**kwargs):
        self.sparsity = sparsity
        self.nz_indices = nz_indices
        self.base_sampler_class = base_sampler_class 
        self.block_xu = block_xu
        self.block_xl = block_xl

        super().__init__(**kwargs)

    def _do(self, problem, n_samples, **kwargs):

        ## Problem initialization
        X = np.zeros((n_samples, len(problem.xl)))

        base_sampler = self.base_sampler_class(block_xu = self.block_xu, 
                                               block_xl = self.block_xl, 
                                               uni_indices=self.nz_indices)

        # Initial population sampling 
        X = base_sampler._do(problem, n_samples, **kwargs)

        for row in range(np.size(X,0)):

            # Where to put the zeros
            genome_size = np.shape(X)[1]
            indices = random.sample(range(genome_size), round(genome_size*self.sparsity))

            # Exclude any indices that always need to be non-zero
            indices = list(set(indices) -  set(self.nz_indices))
            indices = np.array(indices) 

            # Zero out 
            X[row,indices]  = 0

        assert np.all(X <= problem.xu), "Sampled solutions out of bounds"
        assert np.all(X >= problem.xl), "Sampled solutions out of bounds"
 

        return X


