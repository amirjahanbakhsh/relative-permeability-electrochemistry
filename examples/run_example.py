"""Simple example: compute j vs S and save CSV.

Writes `results/j_vs_S.csv` with columns: S, j, j_rel
Optionally saves `figures/j_vs_S.png` if matplotlib is installed.
"""
import sys
import os
import csv
import numpy as np

# Ensure project root is on `sys.path` so `from model.solver import ...` works
# when running this script directly from any working directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import solve, krg


def compute_j_for_S(S, D0=1.0, n=2.0, k_r=1.0, L=1.0, N=101, C_left=1.0, C_right=0.0):
    """Compute integrated reaction (proportional to current) for uniform saturation S."""
    sat_func = lambda x: S + 0.0 * x
    res = solve(D0=D0, n=n, k_r=k_r, L=L, N=N, C_left=C_left, C_right=C_right, saturation=sat_func)
    x = res['x']
    dx = x[1] - x[0]
    R = k_r * res['C'] * krg(res['S'], n=n)
    J = np.sum(R) * dx
    return J


def main():
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
    fig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    S_list = np.linspace(0.0, 0.95, 20)

    # baseline at S=0
    J0 = compute_j_for_S(0.0)

    rows = []
    for S in S_list:
        J = compute_j_for_S(S)
        rows.append((float(S), float(J), float(J / J0 if J0 != 0 else 0.0)))

    csv_path = os.path.join(out_dir, 'j_vs_S.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['S', 'j', 'j_rel'])
        writer.writerows(rows)

    print(f'Wrote {csv_path}')

    # optional plot
    try:
        import matplotlib.pyplot as plt
        S_vals = [r[0] for r in rows]
        j_vals = [r[1] for r in rows]
        j_rel = [r[2] for r in rows]
        plt.figure()
        plt.plot(S_vals, j_rel, '-o')
        plt.xlabel('S (liquid saturation)')
        plt.ylabel('j / j_max')
        plt.grid(True)
        fig_path = os.path.join(fig_dir, 'j_vs_S.png')
        plt.savefig(fig_path, dpi=200)
        print(f'Saved plot to {fig_path}')
    except Exception:
        print('matplotlib not available; skipping plot')


if __name__ == '__main__':
    main()
