from abc import ABC, abstractmethod
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton
from pyformlang.cfg import Variable

__all__ = ["FABooleanMatrices"]

from project import RSM, Box


class FABooleanMatrices(ABC):
    """Base class representing boolean adjacency matrices
    for each finite automaton label
    """

    def __init__(self):
        self.num_states = 0
        self.start_states = set()
        self.final_states = set()
        self.bool_matrices = {}
        self.state_indices = {}
        self.states_to_box_variable = {}

    def to_automaton(self):
        automaton = NondeterministicFiniteAutomaton()
        for label, bool_matrix in self.bool_matrices.items():
            for s_from, s_to in self._get_nonzero(bool_matrix):
                automaton.add_transition(s_from, label, s_to)

        for state in self.start_states:
            automaton.add_start_state(State(state))

        for state in self.final_states:
            automaton.add_final_state(State(state))

        return automaton

    def get_states(self):
        return self.state_indices.keys()

    def get_start_states(self):
        return self.start_states.copy()

    def get_final_states(self):
        return self.final_states.copy()

    def intersect(self, other):
        """Returns a new class object containing
        the Kronecker products for given matrices
        """
        bm_res = self.__class__()
        bm_res.num_states = self.num_states * other.num_states
        common_labels = self.bool_matrices.keys() & other.bool_matrices.keys()

        for label in common_labels:
            bm_res.bool_matrices[label] = self._kron(
                self.bool_matrices[label], other.bool_matrices[label]
            )

        for s_fst, s_fst_idx in self.state_indices.items():
            for s_snd, s_snd_idx in other.state_indices.items():
                new_state = new_state_idx = s_fst_idx * other.num_states + s_snd_idx
                bm_res.state_indices[new_state] = new_state_idx

                if s_fst in self.start_states and s_snd in other.start_states:
                    bm_res.start_states.add(new_state)

                if s_fst in self.final_states and s_snd in other.final_states:
                    bm_res.final_states.add(new_state)

        return bm_res

    @classmethod
    def from_automaton(cls, automaton):
        bm = cls()
        bm.num_states = len(automaton.states)
        bm.start_states = automaton.start_states
        bm.final_states = automaton.final_states
        bm.state_indices = {state: idx for idx, state in enumerate(automaton.states)}
        bm.bool_matrices = bm._create_bool_matrices(automaton)
        return bm

    @classmethod
    def from_rsm(cls, rsm: RSM):
        bm = cls()
        bm.num_states = sum(len(box.dfa.states) for box in rsm.boxes)
        box_idx = 0
        for box in rsm.boxes:
            for idx, state in enumerate(box.dfa.states):
                new_name = bm._rename_rsm_box_state(state, box.variable)
                bm.state_indices[new_name] = idx + box_idx
                if state in box.dfa.start_states:
                    bm.start_states.add(bm.state_indices[new_name])
                if state in box.dfa.final_states:
                    bm.final_states.add(bm.state_indices[new_name])
            bm.states_to_box_variable.update(
                {
                    (
                        bm.state_indices[
                            bm._rename_rsm_box_state(box.dfa.start_state, box.variable)
                        ],
                        bm.state_indices[bm._rename_rsm_box_state(state, box.variable)],
                    ): box.variable.value
                    for state in box.dfa.final_states
                }
            )
            bm.bool_matrices.update(bm._create_box_bool_matrices(box))
            box_idx += len(box.dfa.states)
        return bm

    def get_nonterminals(self, s_from, s_to):
        return self.states_to_box_variable.get((s_from, s_to))

    def _rename_rsm_box_state(self, state: State, box_var: Variable):
        return State(f"{state.value}#{box_var.value}")

    def _create_box_bool_matrices(self, box: Box):
        bool_matrices = {}
        for s_from, trans in box.dfa.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.state_indices[
                        self._rename_rsm_box_state(s_from, box.variable)
                    ]
                    idx_to = self.state_indices[
                        self._rename_rsm_box_state(s_to, box.variable)
                    ]
                    label = str(label)
                    if label in self.bool_matrices:
                        self.bool_matrices[label][idx_from, idx_to] = True
                        continue
                    if label not in bool_matrices:
                        bool_matrices[label] = self._create_bool_matrix(
                            (self.num_states, self.num_states)
                        )
                    bool_matrices[label][idx_from, idx_to] = True

        return bool_matrices

    def _create_bool_matrices(self, automaton):
        bool_matrices = {}
        for s_from, trans in automaton.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.state_indices[s_from]
                    idx_to = self.state_indices[s_to]
                    label = str(label)
                    if label not in bool_matrices:
                        bool_matrices[label] = self._create_bool_matrix(
                            (self.num_states, self.num_states)
                        )
                    bool_matrices[label][idx_from, idx_to] = True

        return bool_matrices

    @abstractmethod
    def get_transitive_closure(self):
        pass

    @staticmethod
    @abstractmethod
    def _kron(bm1, bm2):
        pass

    @staticmethod
    @abstractmethod
    def _get_nonzero(bm):
        pass

    @staticmethod
    @abstractmethod
    def _create_bool_matrix(shape):
        pass
