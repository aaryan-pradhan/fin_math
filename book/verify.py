"""Monte Carlo checks of the book's stochastic claims (run by `make verify`).
Each check simulates a claim from the text and fails if the text's value is outside the 99.9% interval
(3.29 standard errors: with many checks per run, 95% would raise false alarms)."""
import numpy as np
rng = np.random.default_rng(2026)
fails = []

def check(name, samples, claim):
    m, se = samples.mean(), samples.std(ddof=1) / np.sqrt(len(samples))
    ok = abs(m - claim) <= 3.29 * se + 1e-12
    print(f"{'ok  ' if ok else 'FAIL'} {name}: sim {m:.4f} ± {3.29*se:.4f}, text {claim}")
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

# Ch 11: roulette ruin, p = 18/38, from 10 to 20: P = 0.2585, D = 91.76
def ruin_p(p, i, N, n=20000):
    x = np.full(n, i); tau = np.zeros(n); alive = np.ones(n, bool)
    while alive.any():
        x[alive] += np.where(rng.random(alive.sum()) < p, 1, -1); tau[alive] += 1
        alive &= (x > 0) & (x < N)
    return (x == N).astype(float), tau
win, dur = ruin_p(18 / 38, 10, 20)
check("Ch11 roulette P_10", win, 0.2585334)
check("Ch11 roulette D_10", dur, 91.757303)

# Ch 11: B = mu t + W, mu = 0.5, exit (-1, 1): P(up first) = 1/(1+e^{-1})
def exit_drift(mu, A, B, n=40000, dt=1e-3):
    x = np.zeros(n); up = np.full(n, np.nan); alive = np.ones(n, bool)
    while alive.any():
        xn = x + mu * dt + rng.normal(0, np.sqrt(dt), n)
        pu = np.exp(-2 * np.maximum(A - x, 0) * np.maximum(A - xn, 0) / dt)   # bridge crosses A
        pd = np.exp(-2 * np.maximum(x + B, 0) * np.maximum(xn + B, 0) / dt)   # bridge crosses -B
        hu = alive & ((xn >= A) | (rng.random(n) < pu)); up[hu] = 1; alive &= ~hu
        hd = alive & ((xn <= -B) | (rng.random(n) < pd)); up[hd] = 0; alive &= ~hd
        x = xn
    return up
check("Ch11 P(up 1 before -1), mu=0.5", exit_drift(0.5, 1, 1), 1 / (1 + np.exp(-1)))

# Ch 14: P(M(1) >= 1) = 2(1 - Phi(1)) and P(W(1) <= 0, M(1) >= 1) = 1 - Phi(2), with bridge-corrected maxima
from math import erf
Phi = lambda x: 0.5 * (1 + erf(x / np.sqrt(2)))
n, steps = 200000, 500; dt = 1 / steps
w = np.zeros(n); hit = np.zeros(n, bool)
for _ in range(steps):
    wn = w + rng.normal(0, np.sqrt(dt), n)
    hit |= (wn >= 1) | (rng.random(n) < np.exp(-2 * np.maximum(1 - w, 0) * np.maximum(1 - wn, 0) / dt))
    w = wn
check("Ch14 P(M(1)>=1)", hit.astype(float), 2 * (1 - Phi(1)))
check("Ch14 P(W(1)<=0, M(1)>=1)", (hit & (w <= 0)).astype(float), 1 - Phi(2))

raise SystemExit(1 if fails else 0)
