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

def hit_line(a, b, n=40000, dt=1e-3, tmax=6.0):
    """First time W_t = a - b t, with a Brownian-bridge correction between grid points."""
    T = np.full(n, np.nan); w = np.zeros(n); alive = np.ones(n, bool); t = 0.0
    while alive.any() and t < tmax:
        w_new = w + rng.normal(0, np.sqrt(dt), n)
        d0, d1 = (a - b * t) - w, (a - b * (t + dt)) - w_new          # distance below the line
        crossed = (d1 <= 0) | (rng.random(n) < np.exp(-2 * np.maximum(d0, 0) * np.maximum(d1, 0) / dt))
        new = alive & crossed; T[new] = t + dt / 2; alive &= ~new
        w, t = w_new, t + dt
    return T[~np.isnan(T)]

# Ch 7: T = first time W hits 2 - 4t has E T = 1/2 and Var T = 1/32
T = hit_line(2, 4)
check("Ch7 E[T], line 2-4t", T, 0.5)
check("Ch7 E[T^2], line 2-4t", T**2, 9 / 32)

# Ch 8: W hits the rising line 2t-4 (= -W hits 4-2t): E tau = 2, E tau^2 = 4.5, Laplace at s=1
T = hit_line(4, 2, tmax=12)
check("Ch8 E[tau], line 2t-4", T, 2.0)
check("Ch8 E[tau^2], line 2t-4", T**2, 4.5)
check("Ch8 E[exp(-tau)], line 2t-4", np.exp(-T), np.exp(8 - 4 * np.sqrt(6)))

# Ch 7: fair walk stopped at +10 or -5: P(+10 first) = 1/3, E tau = 50
def ruin(A, B, n=20000):
    x = np.zeros(n, int); tau = np.zeros(n, int); alive = np.ones(n, bool)
    while alive.any():
        x[alive] += rng.choice([-1, 1], alive.sum()); tau[alive] += 1
        alive &= (x < A) & (x > -B)
    return x == A, tau
up, tau = ruin(10, 5)
check("Ch7 P(hit +10 before -5)", up.astype(float), 1 / 3)
check("Ch7 E[tau], exit (-5,10)", tau.astype(float), 50)

raise SystemExit(1 if fails else 0)
