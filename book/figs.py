"""Writes the seeded data behind the book's random-path figures (run once: uv run --with numpy python figs.py).
The data files in figs/ are committed, so the book builds without running this."""
import numpy as np
rng = np.random.default_rng(7)

def write(name, cols, header):
    np.savetxt(f'figs/{name}.dat', np.column_stack(cols), header=header, comments='', fmt='%.4f')

# three standard Brownian paths on [0,1]
n = 400; t = np.linspace(0, 1, n + 1)
many = np.hstack([np.zeros((500, 1)), np.cumsum(rng.normal(0, np.sqrt(1 / n), (500, n)), axis=1)])
ok = np.abs(many).max(axis=1) < 1.6          # pick three typical-looking paths: one ends high, one low, one near 0
pick = [np.where(ok & (abs(many[:, -1] - target) < 0.15))[0][0] for target in (0.9, -0.8, 0.1)]
W = many[pick]
write('bm3', [t, *W], 't w1 w2 w3')

# a fair +-1 random walk, 40 steps
k = np.arange(41); S = np.concatenate([[0], np.cumsum(rng.choice([-1, 1], 40))])
write('walk', [k, S], 'k s')

# random walk rescaled: dt = 1/n, dx = sqrt(dt), n = 10, 100, 1000 on [0,1]
cols, names = [], []
for m in (10, 100, 1000):
    steps = rng.choice([-1, 1], m) * np.sqrt(1 / m)
    path = np.concatenate([[0], np.cumsum(steps)])
    tt = np.linspace(0, 1, m + 1)
    np.savetxt(f'figs/scaled{m}.dat', np.column_stack([tt, path]), header='t x', comments='', fmt='%.4f')

# integrated Brownian motion Z(t) = int_0^t W(s) ds for the three paths above
Z = np.cumsum(W * (1 / n), axis=1) - W * (1 / n) / 2
write('ibm', [t, *W, *Z], 't w1 w2 w3 z1 z2 z3')
