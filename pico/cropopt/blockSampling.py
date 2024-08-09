import numpy as np
from pymoo.core.sampling import Sampling


# Essentially, every population member has all the same value in all genome positions
class BlockSampling(Sampling):

    def __init__(self, block_xu = None, block_xl = None, uni_indices=[], **kwargs): 

        self.uni_indices = uni_indices
        self.block_xu = block_xu
        self.block_xl = block_xl

        super().__init__(**kwargs)

    def _do(self, problem, n_samples, **kwargs):

        # these are the solutions that we want to be random and uniform 
        X_uniform = np.random.random((n_samples, problem.n_var))

        # Create one sample per solution 
        X_block = np.random.random((n_samples, 1))

        block_inds = list(set(range(problem.n_var)) - set(self.uni_indices))

        if problem.has_bounds():
            xl, xu = problem.bounds()
            assert np.all(xu >= xl)
           
            X_uniform = xl + (xu - xl) * X_uniform
            xl = self.block_xl
            xu = self.block_xu

            X_block = xl + (xu - xl) * X_block

        X = X_uniform

        X[:, block_inds] = X_block[:]

        return X 


