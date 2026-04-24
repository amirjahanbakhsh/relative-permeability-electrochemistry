"""Plot helpers for solver results.

This module provides a small convenience function that plots concentration
and saturation across the 1D domain. Matplotlib is optional; the function
raises an ImportError with install instructions if matplotlib is missing.
"""
from typing import Tuple

def plot_solution(res, show: bool = True):
    """Plot concentration `C` and saturation `S` vs `x` from solver result.

    Parameters
    - res: dict returned by `solve()` with keys `'x'`, `'C'`, `'S'`.
    - show: if True, call `plt.show()`.

    Returns (fig, ax) for further customization.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception as e:
        raise ImportError("matplotlib is required for plotting — install with `pip install matplotlib`") from e

    x = res["x"]
    C = res["C"]
    S = res["S"]

    fig, ax1 = plt.subplots()
    ax1.plot(x, C, label="C (concentration)", color="C0")
    ax1.set_xlabel("x")
    ax1.set_ylabel("C", color="C0")
    ax1.tick_params(axis="y", labelcolor="C0")

    ax2 = ax1.twinx()
    ax2.plot(x, S, label="S (saturation)", color="C1", linestyle="--")
    ax2.set_ylabel("S", color="C1")
    ax2.tick_params(axis="y", labelcolor="C1")

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2)

    fig.tight_layout()
    if show:
        plt.show()
    return fig, ax1
