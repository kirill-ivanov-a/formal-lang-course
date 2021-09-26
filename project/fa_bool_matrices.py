from scipy import sparse
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton

__all__ = ["FABooleanMatrices"]


class FABooleanMatrices:
    """Class representing boolean adjacency matrices
    for each finite automaton label
    """

    def __init__(self):
        self.num_states = 0
        self.start_states = set()
        self.final_states = set()
        self.bool_matrices = {}
        self.state_indices = {}

    def to_automaton(self):
        automaton = NondeterministicFiniteAutomaton()
        for label, bool_matrix in self.bool_matrices.items():
            for s_from, s_to in zip(*bool_matrix.nonzero()):
                automaton.add_transition(s_from, label, s_to)

        for state in self.start_states:
            automaton.add_start_state(State(state))

        for state in self.final_states:
            automaton.add_final_state(State(state))

        return automaton

    def get_transitive_closure(self):
        tc = sum(bm for bm in self.bool_matrices.values())
        prev_nnz = tc.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc += tc @ tc
            prev_nnz, new_nnz = new_nnz, tc.nnz

        return tc

    @classmethod
    def from_automaton(cls, automaton):
        bm = cls()
        bm.num_states = len(automaton.states)
        bm.start_states = automaton.start_states
        bm.final_states = automaton.final_states
        bm.state_indices = {state: idx for idx, state in enumerate(automaton.states)}
        bm.bool_matrices = bm._create_bool_matrices(automaton)
        return bm

    @staticmethod
    def intersect(fst_bm, snd_bm):
        """Returns a new class object containing
        the Kronecker products for given matrices
        """
        bm_res = FABooleanMatrices()
        bm_res.num_states = fst_bm.num_states * snd_bm.num_states
        common_labels = fst_bm.bool_matrices.keys() & snd_bm.bool_matrices.keys()

        for label in common_labels:
            bm_res.bool_matrices[label] = sparse.kron(
                fst_bm.bool_matrices[label], snd_bm.bool_matrices[label], format="dok"
            )

        for s_fst, s_fst_idx in fst_bm.state_indices.items():
            for s_snd, s_snd_idx in snd_bm.state_indices.items():
                new_state = new_state_idx = s_fst_idx * snd_bm.num_states + s_snd_idx
                bm_res.state_indices[new_state] = new_state_idx

                if s_fst in fst_bm.start_states and s_snd in snd_bm.start_states:
                    bm_res.start_states.add(new_state)

                if s_fst in fst_bm.final_states and s_snd in snd_bm.final_states:
                    bm_res.final_states.add(new_state)

        return bm_res

    def _create_bool_matrices(self, automaton):
        bool_matrices = {}
        for s_from, trans in automaton.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.state_indices[s_from]
                    idx_to = self.state_indices[s_to]
                    if label not in bool_matrices:
                        bool_matrices[label] = sparse.dok_matrix(
                            (self.num_states, self.num_states), dtype=bool
                        )
                    bool_matrices[label][idx_from, idx_to] = True

        return bool_matrices
