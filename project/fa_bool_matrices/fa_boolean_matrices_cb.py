import pycubool as cb

from project.fa_bool_matrices.fa_bool_matrices import FABooleanMatrices

__all__ = ["FABooleanMatricesCB"]


class FABooleanMatricesCB(FABooleanMatrices):
    """Class representing boolean adjacency matrices
    for each finite automaton label using pycubool matrices"""

    def __init__(self):
        super().__init__()

    def get_transitive_closure(self):
        tc = cb.Matrix.empty(shape=(self.num_states, self.num_states))
        for bm in self.bool_matrices.values():
            tc.ewiseadd(bm, out=tc)
        prev_nnz = tc.nvals
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc.mxm(tc, out=tc, accumulate=True)
            prev_nnz, new_nnz = new_nnz, tc.nvals

        return tc

    @staticmethod
    def _kron(bm1, bm2):
        return bm1.kronecker(bm2)

    @staticmethod
    def _create_bool_matrix(shape):
        return cb.Matrix.empty(shape)

    @staticmethod
    def _get_nonzero(bm):
        return zip(*bm.to_lists())
