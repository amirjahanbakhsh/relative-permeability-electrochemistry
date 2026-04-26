"""Physics helpers: relative permeability, effective diffusivity, reaction."""
import numpy as np


def krg(s, n=2.0):
    """Corey-type relative permeability for gas phase: krg = (1 - S)^n

    s : array-like, saturation (liquid fraction) in [0,1]
    n : exponent
    """
    s = np.asarray(s)
    return np.clip((1.0 - s) ** n, 0.0, 1.0)


def effective_diffusivity(s, D0=1.0, n=2.0):
    """Compute effective diffusivity at nodes: D_eff = D0 * krg(S)"""
    return D0 * krg(s, n=n)


def reaction(C, s, k_r=1.0, n=2.0):
    """First-order reaction term R = k_r * C * krg(S)"""
    return k_r * C * krg(s, n=n)


def compute():
    # Backwards-compatible placeholder
    return {"note": "use krg/effective_diffusivity/reaction for physics computations"}
