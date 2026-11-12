"""Monte Carlo checks of the book's stochastic claims (run by `make verify`).
Each check simulates a claim from the text and fails if the text's value is outside the 95% interval."""
import numpy as np
rng = np.random.default_rng(2026)
fails = []

def check(name, samples, claim):
    m, se = samples.mean(), samples.std(ddof=1) / np.sqrt(len(samples))
    ok = abs(m - claim) <= 1.96 * se + 1e-12
    print(f"{'ok  ' if ok else 'FAIL'} {name}: sim {m:.4f} ± {1.96*se:.4f}, text {claim}")
    if not ok: fails.append(name)

# --- checks are added chapter by chapter below ---

raise SystemExit(1 if fails else 0)
