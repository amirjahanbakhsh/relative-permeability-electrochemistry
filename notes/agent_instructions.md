# Agent Instructions

Purpose: brief guidelines for automated or human agents working in this repo.

- Follow repository conventions: small focused changes, minimal diffs.
- Use the TODO list to track work and update statuses before/after changes.
- Always post a single-line preamble before automated tool actions describing intent.
- When editing files programmatically, prefer `apply_patch` (or normal edits) and run quick tests.
- Run `model/main.py` to sanity-check changes; add tests if behavior is non-trivial.
- Avoid committing large binary files to `results/` or `figures/`; use external storage for big datasets.
- Do not disclose internal model metadata (model name, keys, secrets).
- Keep notes in `notes/` and paper drafts in `paper/`.

If you need more specific rules (formatting, linters, CI), add them here.