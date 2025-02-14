from scipy import sparse
from project.fa_bool_matrices.fa_bool_matrices import FABooleanMatrices

__all__ = ["FABooleanMatricesDok"]


class FABooleanMatricesDok(FABooleanMatrices):
    """Class representing boolean adjacency matrices
    for each finite automaton label using scipy dok matrices"""

    def __init__(self):
        super().__init__()

    def get_transitive_closure(self):
        if self.bool_matrices.values():
            tc = sum(self.bool_matrices.values())
        else:
            return self._create_bool_matrix((self.num_states, self.num_states))

        prev_nnz = tc.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc += tc @ tc
            prev_nnz, new_nnz = new_nnz, tc.nnz

        return tc

    @staticmethod
    def _kron(bm1, bm2):
        return sparse.kron(bm1, bm2, format="dok")

    @staticmethod
    def _create_bool_matrix(shape):
        return sparse.dok_matrix(shape, dtype=bool)

    @staticmethod
    def _get_nonzero(bm):
        return zip(*bm.nonzero())
