"""1D steady-state diffusion-reaction solver with saturation-dependent D_eff.

Governing equation (steady-state):
    d/dx[ D_eff(S) dC/dx ] = - R
with R = k_r * C * krg(S)

This module provides `solve(...)` which returns a dict with keys: `x`, `C`, `S`, `D`.
"""
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


def solve(D0=1.0, n=2.0, k_r=0.0, L=1.0, N=101, C_left=1.0, C_right=0.0, saturation=None):
    """Solve 1D steady-state diffusion-reaction with Dirichlet BCs.

    Parameters
    - D0: bulk diffusivity
    - n: relative-permeability exponent used in krg(S)
    - k_r: first-order reaction constant (multiplies C * krg(S))
    - L: domain length
    - N: number of grid points (>=3)
    - C_left, C_right: Dirichlet BCs at x=0 and x=L
    - saturation: None (uniform zero), callable(x) or array of length N

    Returns dict: { 'x': x, 'C': C, 'S': s, 'D': D_nodes }
    """
    if N < 3:
        raise ValueError("N must be >= 3")

    x = np.linspace(0.0, L, N)
    dx = x[1] - x[0]

    # saturation field
    if saturation is None:
        s = np.zeros_like(x)
    elif callable(saturation):
        s = np.asarray(saturation(x), dtype=float)
    else:
        s = np.asarray(saturation, dtype=float)
        if s.shape != x.shape:
            raise ValueError("saturation must be None, callable, or array of length N")

    # Effective diffusivity at nodes
    D_nodes = effective_diffusivity(s, D0=D0, n=n)

    # Interfacial diffusivity (harmonic mean) between nodes i and i+1
    # avoid divide-by-zero when D_nodes == 0 by flooring small values
    eps = 1e-12
    D_safe = np.where(D_nodes <= 0.0, eps, D_nodes)
    D_iface = 2.0 / (1.0 / D_safe[:-1] + 1.0 / D_safe[1:])

    # Unknowns are interior nodes 1..N-2
    M = N - 2
    A = np.zeros((M, M), dtype=float)
    b = np.zeros(M, dtype=float)

    for i in range(M):
        j = i + 1  # global node index
        d_minus = D_iface[j - 1]  # between j-1 and j
        d_plus = D_iface[j] if j < N - 1 else D_iface[-1]

        aW = d_minus / dx ** 2
        aE = d_plus / dx ** 2
        aP = aW + aE + k_r * krg(s[j], n=n)

        A[i, i] = aP
        if i > 0:
            A[i, i - 1] = -aW
        if i < M - 1:
            A[i, i + 1] = -aE

        # Boundary contributions
        if i == 0:
            b[i] += aW * C_left
        if i == M - 1:
            b[i] += aE * C_right

    # Solve linear system
    if M > 0:
        C_int = np.linalg.solve(A, b)
        C = np.empty(N, dtype=float)
        C[0] = C_left
        C[1:-1] = C_int
        C[-1] = C_right
    else:
        # trivial two-point domain
        C = np.array([C_left, C_right])

    return {"x": x, "C": C, "S": s, "D": D_nodes}


if __name__ == "__main__":
    # quick sanity run
    res = solve(D0=1.0, n=2.0, k_r=1.0, L=1.0, N=51, C_left=1.0, C_right=0.0,
                saturation=lambda x: 0.5 * (1.0 + 0.0 * x))
    print("x.shape", res["x"].shape, "C.min", res["C"].min(), "C.max", res["C"].max())
