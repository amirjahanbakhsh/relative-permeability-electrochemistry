# Project

Starter project for relative-permeability electrochemistry modelling.

Structure:

project/
│── README.md
│── TODO.md
│── notes/
│     └── framework.md
│     └── literature.md
│── model/
│     └── main.py
│     └── solver.py
│     └── physics.py
│── results/
│── figures/
│── paper/
│     └── outline.md

## Usage

Install dependencies (recommended in a virtual environment):

```bash
pip install -r requirements.txt
```

Run the example that computes normalized current vs saturation and writes a CSV:

```bash
python examples/run_example.py
# output: results/j_vs_S.csv (and figures/j_vs_S.png if matplotlib is installed)
```

Run unit tests:

```bash
python -m unittest discover -v
```

Run the simple model entry point:

```bash
python model/main.py
```

Files of interest:

- `examples/run_example.py` — example runner that writes `results/j_vs_S.csv`.
- `model/solver.py` — 1D steady-state diffusion-reaction solver (saturation-dependent D_eff).
- `model/plot.py` — optional plotting helper (requires `matplotlib`).
- `tests/test_solver.py` — unit tests for core solver behavior.

If you want a quick plot but don't have `matplotlib`, install it with:

```bash
pip install matplotlib
```

