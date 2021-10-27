from project.automatons.rsm import RSM

__all__ = ["minimize_rsm"]


def minimize_rsm(rsm: RSM) -> RSM:
    return rsm.minimize()
