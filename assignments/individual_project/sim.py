"""Monte Carlo simulation of BM, GBM, OU, Vasicek and CIR.
Writes every figure (figures/) and every number (tables/) that main.tex uses.

    uv run --no-project --with numpy --with matplotlib python sim.py
"""
import os
from math import erf, sqrt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

HERE = os.path.dirname(os.path.abspath(__file__))
FIG, TAB = os.path.join(HERE, "figures"), os.path.join(HERE, "tables")
os.makedirs(FIG, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

BLUE, DARK, ORANGE, GREY, GREEN, RED = "#2A78D6", "#174A8A", "#EB6834", "#52514E", "#008300", "#E34948"
mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"], "axes.formatter.use_mathtext": True,
    "mathtext.fontset": "cm", "axes.unicode_minus": False, "pdf.fonttype": 42, "font.size": 9, "axes.titlesize": 9,
    "axes.titlelocation": "left", "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "legend.frameon": False, "legend.fontsize": 8,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})

rng = np.random.default_rng(2026)
M = 20_000                                   # Monte Carlo paths
Phi = np.vectorize(lambda x: 0.5 * (1 + erf(x / sqrt(2))))
npdf = lambda x, m, s: np.exp(-(x - m) ** 2 / (2 * s * s)) / (s * sqrt(2 * np.pi))
rows, num = [], {}


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"))
    plt.close(fig)


def check(group, name, f, theory):
    """Monte Carlo estimate of E[f] with standard error. Fails if it is more than 4 SE from theory."""
    est, se = f.mean(), f.std(ddof=1) / sqrt(len(f))
    z = (est - theory) / se
    assert abs(z) < 4, (name, est, theory, se)
    rows.append((group, name, theory, est, se, z))


def fan(ax, t, X, color, k=10):
    q = np.percentile(X, [5, 25, 50, 75, 95], axis=0)
    ax.fill_between(t, q[0], q[4], color=color, alpha=0.12, lw=0, label="90% band")
    ax.fill_between(t, q[1], q[3], color=color, alpha=0.25, lw=0, label="50% band")
    ax.plot(t, X[:k].T, color=color, lw=0.55, alpha=0.75)
    ax.plot(t, q[2], color=DARK, lw=1.3, label="median")


def paths(x0, step, Z):
    X = np.empty((Z.shape[0], Z.shape[1] + 1))
    X[:, 0] = x0
    for i in range(Z.shape[1]):
        X[:, i + 1] = step(X[:, i], Z[:, i])
    return X


def ou_step(th, m, s, dt):
    """Exact OU transition: X(t+dt) | X(t) is normal."""
    e, sd = np.exp(-th * dt), s * sqrt((1 - np.exp(-2 * th * dt)) / (2 * th))
    return lambda x, z: m + (x - m) * e + sd * z


# ---------------------------------------------------------------- 1. Brownian motion
T, n = 1.0, 252
dt = T / n
t = np.linspace(0, T, n + 1)
Z = rng.standard_normal((M, n))
W = np.concatenate([np.zeros((M, 1)), sqrt(dt) * Z.cumsum(1)], 1)
check("BM", r"$\mathbb{E}[W_1]$", W[:, -1], 0.0)
check("BM", r"$\mathrm{Var}[W_1]$", W[:, -1] ** 2, T)
check("BM", r"$\mathbb{E}[W_{1/2}W_1]=\min(s,t)$", W[:, n // 2] * W[:, -1], 0.5)

fig, ax = plt.subplots(figsize=(6.3, 2.7))
fan(ax, t, W, BLUE)
for c, ls in [(1, "--"), (2, ":")]:
    ax.plot(t, c * np.sqrt(t), color=ORANGE, ls=ls, lw=1, label=rf"$\pm{c}\sqrt{{t}}$" if c > 1 else r"$\pm\sqrt{t}$")
    ax.plot(t, -c * np.sqrt(t), color=ORANGE, ls=ls, lw=1)
ax.set(xlabel="time $t$ (years)", ylabel="$W_t$", xlim=(0, T))
ax.legend(ncol=5, loc="upper left")
save(fig, "bm_paths")

fine = 2 ** 16
dWf = rng.standard_normal(fine) * sqrt(T / fine)
Wf = np.concatenate([[0], dWf.cumsum()])
ks = np.arange(2, 17)
qv = [np.sum(np.diff(Wf[:: fine // 2 ** k]) ** 2) for k in ks]
tv = [np.sum(np.abs(np.diff(Wf[:: fine // 2 ** k]))) for k in ks]
num["QVFinest"] = f"{qv[-1]:.3f}"
num["TVFinest"] = f"{tv[-1]:.0f}"

fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.1))
x = np.linspace(-4, 4, 300)
axs[0].hist(W[:, -1], bins=70, density=True, color=BLUE, alpha=0.55, label="simulated")
axs[0].plot(x, npdf(x, 0, 1), color=DARK, lw=1.3, label="$N(0,1)$")
axs[0].set(title="(a) $W_1$", xlabel="$w$", ylabel="density", ylim=(0, 0.58))
axs[0].legend(loc="upper left", fontsize=6.5)
axs[1].plot(t, W.var(0), color=BLUE, lw=1.5, label="sample")
axs[1].plot(t, t, color=ORANGE, ls="--", lw=1, label="$t$")
axs[1].set(title=r"(b) $\mathrm{Var}[W_t]$", xlabel="$t$")
axs[1].legend()
axs[2].loglog(2.0 ** ks, qv, "o-", color=BLUE, ms=3, label=r"$\sum(\Delta W)^2$")
axs[2].loglog(2.0 ** ks, tv, "s-", color=ORANGE, ms=3, label=r"$\sum|\Delta W|$")
axs[2].axhline(T, color=GREY, lw=0.8, ls=":")
axs[2].set(title="(c) variation on one path", xlabel="number of steps")
axs[2].legend()
fig.tight_layout()
save(fig, "bm_checks")

# ---------------------------------------------------------------- 2. Geometric Brownian motion
S0, mu, sig = 100.0, 0.08, 0.25
S = S0 * np.exp((mu - sig ** 2 / 2) * t + sig * W)          # exact solution on the same W
mean_th, med_th = S0 * np.exp(mu * T), S0 * np.exp((mu - sig ** 2 / 2) * T)
check("GBM", r"$\mathbb{E}[S_1]$", S[:, -1], mean_th)
check("GBM", r"$\mathrm{Var}[S_1]$", (S[:, -1] - mean_th) ** 2, S0 ** 2 * np.exp(2 * mu * T) * (np.exp(sig ** 2 * T) - 1))
check("GBM", r"$\mathbb{P}(S_1\le \mathrm{median})$", (S[:, -1] <= med_th).astype(float), 0.5)
check("GBM", r"$\mathbb{E}[\ln S_1]$", np.log(S[:, -1]), np.log(S0) + (mu - sig ** 2 / 2) * T)
num["GBMMeanTh"], num["GBMMedTh"] = f"{mean_th:.2f}", f"{med_th:.2f}"
num["GBMMin"], num["GBMMax"] = f"{S[:, -1].min():.1f}", f"{S[:, -1].max():.1f}"

lnpdf = lambda s, m, v: np.exp(-(np.log(s) - m) ** 2 / (2 * v)) / (s * np.sqrt(2 * np.pi * v))
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.5), gridspec_kw={"width_ratios": [1.6, 1]})
fan(axs[0], t, S, BLUE)
axs[0].plot(t, S0 * np.exp(mu * t), color=ORANGE, ls="--", lw=1.2, label=r"$S_0e^{\mu t}$")
axs[0].set(title="(a) sample paths", xlabel="time $t$ (years)", ylabel="$S_t$", xlim=(0, T), ylim=(55, 185))
axs[0].legend(ncol=4, loc="upper left", fontsize=7)
s = np.linspace(30, 260, 400)
axs[1].hist(S[:, -1], bins=90, range=(30, 260), density=True, color=BLUE, alpha=0.55, label="simulated")
axs[1].plot(s, lnpdf(s, np.log(S0) + (mu - sig ** 2 / 2) * T, sig ** 2 * T), color=DARK, lw=1.3, label="lognormal")
axs[1].axvline(med_th, color=GREY, ls=":", lw=1, label="median")
axs[1].axvline(mean_th, color=ORANGE, ls="--", lw=1, label="mean")
axs[1].set(title="(b) $S_1$", xlabel="$s$", ylabel="density")
axs[1].legend()
fig.tight_layout()
save(fig, "gbm_paths")

fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.4))
for sg, c in zip([0.10, 0.25, 0.50], [GREEN, BLUE, RED]):
    axs[0].plot(t, S0 * np.exp((mu - sg ** 2 / 2) * t + sg * W[1]), color=c, lw=1, label=rf"$\sigma={sg:.2f}$")
    s = np.linspace(20, 300, 500)
    axs[1].plot(s, lnpdf(s, np.log(S0) + (mu - sg ** 2 / 2) * T, sg ** 2 * T), color=c, lw=1.3, label=rf"$\sigma={sg:.2f}$")
    axs[1].plot(S0 * np.exp((mu - sg ** 2 / 2) * T), 0, "v", color=c, ms=6, clip_on=False)
axs[1].axvline(mean_th, color=GREY, ls="--", lw=0.9)
axs[1].annotate("mean, the same\nfor every $\\sigma$", (mean_th, 0.03), (170, 0.028), color=GREY, fontsize=7,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=0.7))
axs[0].set(title="(a) same shocks, three volatilities", xlabel="$t$", ylabel="$S_t$", xlim=(0, T))
axs[1].set(title=r"(b) density of $S_1$ ($\blacktriangledown$ = median)", xlabel="$s$", ylim=(0, None))
axs[0].legend()
fig.tight_layout()
save(fig, "gbm_sigma")

# Strong error of Euler and Milstein against the exact GBM solution
Mf, kmax = 5000, 10
dWf = rng.standard_normal((Mf, 2 ** kmax)) * sqrt(T / 2 ** kmax)
exact = S0 * np.exp((mu - sig ** 2 / 2) * T + sig * dWf.sum(1))
hs, e_eu, e_mi = [], [], []
for k in range(2, kmax + 1):
    h = T / 2 ** k
    dWk = dWf.reshape(Mf, 2 ** k, -1).sum(2)
    se, sm = np.full(Mf, S0), np.full(Mf, S0)
    for i in range(2 ** k):
        d = dWk[:, i]
        se = se + mu * se * h + sig * se * d
        sm = sm + mu * sm * h + sig * sm * d + 0.5 * sig ** 2 * sm * (d * d - h)
    hs.append(h); e_eu.append(np.abs(se - exact).mean()); e_mi.append(np.abs(sm - exact).mean())
p_eu, p_mi = np.polyfit(np.log(hs), np.log(e_eu), 1)[0], np.polyfit(np.log(hs), np.log(e_mi), 1)[0]
assert 0.35 < p_eu < 0.65 and 0.8 < p_mi < 1.2, (p_eu, p_mi)
num["EulerOrder"], num["MilsteinOrder"] = f"{p_eu:.2f}", f"{p_mi:.2f}"

fig, ax = plt.subplots(figsize=(3.6, 2.6))
hs = np.array(hs)
ax.loglog(hs, e_eu, "o-", color=BLUE, ms=3.5, label=f"Euler--Maruyama (slope {p_eu:.2f})".replace("--", "-"))
ax.loglog(hs, e_mi, "s-", color=ORANGE, ms=3.5, label=f"Milstein (slope {p_mi:.2f})")
ax.loglog(hs, e_eu[-1] * (hs / hs[-1]) ** 0.5, color=GREY, ls=":", lw=0.9, label=r"$\propto\Delta t^{1/2}$")
ax.loglog(hs, e_mi[-1] * (hs / hs[-1]), color=GREY, ls="--", lw=0.9, label=r"$\propto\Delta t$")
ax.set(xlabel=r"step size $\Delta t$", ylabel=r"$\mathbb{E}|S_1^{\Delta t}-S_1|$")
ax.legend(fontsize=7)
save(fig, "gbm_error")

# ---------------------------------------------------------------- 3. Ornstein-Uhlenbeck
th, m, s_ou, To, no = 2.0, 0.0, 1.0, 3.0, 600
dto = To / no
to = np.linspace(0, To, no + 1)
sd_inf = s_ou / sqrt(2 * th)
step = ou_step(th, m, s_ou, dto)
X = paths(1.5, step, rng.standard_normal((M, no)))
i1 = int(round(1 / dto))
check("OU", r"$\mathbb{E}[X_1]$", X[:, i1], m + (1.5 - m) * np.exp(-th))
check("OU", r"$\mathrm{Var}[X_1]$", (X[:, i1] - m - 1.5 * np.exp(-th)) ** 2, s_ou ** 2 / (2 * th) * (1 - np.exp(-2 * th)))
check("OU", r"$\mathrm{Var}[X_3]$ (near $\sigma^2/2\theta$)", (X[:, -1] - 1.5 * np.exp(-th * To)) ** 2,
      s_ou ** 2 / (2 * th) * (1 - np.exp(-2 * th * To)))
num["OUHalfLife"] = f"{np.log(2) / th:.2f}"

fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.6))
for x0, c in zip([-1.5, 0.0, 1.5], [GREEN, GREY, BLUE]):
    Xs = X if x0 == 1.5 else paths(x0, step, rng.standard_normal((6, no)))
    axs[0].plot(to, Xs[:6].T, color=c, lw=0.55, alpha=0.8)
    mt = m + (x0 - m) * np.exp(-th * to)
    axs[0].plot(to, mt, color=c, lw=1.6, label=f"$X_0={x0:g}$")
sd_t = s_ou * np.sqrt((1 - np.exp(-2 * th * to)) / (2 * th))
axs[0].set(title="(a) three starting points", xlabel="$t$", ylabel="$X_t$", xlim=(0, To), ylim=(-2.1, 2.9))
axs[0].legend(loc="upper right", ncol=3, fontsize=7)
edges = np.linspace(-1.6, 2.4, 161)
H = np.stack([np.histogram(X[:, j], bins=edges, density=True)[0] for j in range(no + 1)], 1)
axs[1].imshow(H, origin="lower", aspect="auto", extent=(0, To, edges[0], edges[-1]), cmap="Blues", norm=PowerNorm(0.7, vmin=0, vmax=H[:, 30:].max()))
mt = m + (1.5 - m) * np.exp(-th * to)
axs[1].plot(to, mt, color=ORANGE, lw=1.3, label="mean")
axs[1].plot(to, mt + 2 * sd_t, color=ORANGE, ls="--", lw=0.9, label=r"mean $\pm 2$ sd")
axs[1].plot(to, mt - 2 * sd_t, color=ORANGE, ls="--", lw=0.9)
axs[1].set(title=r"(b) density of $X_t$ from $X_0=1.5$", xlabel="$t$")
axs[1].grid(False)
axs[1].legend(loc="upper right")
fig.tight_layout()
save(fig, "ou_paths")

fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.1))
x = np.linspace(-2, 2, 300)
axs[0].hist(X[:, -1], bins=70, density=True, color=BLUE, alpha=0.55, label="simulated")
axs[0].plot(x, npdf(x, m, sd_inf), color=DARK, lw=1.3, label=r"$N(\mu,\sigma^2/2\theta)$")
axs[0].set(title="(a) $X_3$ vs stationary law", xlabel="$x$", ylim=(0, 1.15))
axs[0].legend(loc="upper left", fontsize=6.5)
lag = 400
Xs = paths(rng.normal(m, sd_inf, M), step, rng.standard_normal((M, lag)))   # start in the stationary law
ac = [np.corrcoef(Xs[:, 0], Xs[:, j])[0, 1] for j in range(0, lag + 1, 10)]
tau = to[: lag + 1 : 10]
axs[1].plot(tau, ac, "o", color=BLUE, ms=3, label="simulated")
axs[1].plot(tau, np.exp(-th * tau), color=ORANGE, lw=1.2, label=r"$e^{-\theta\tau}$")
axs[1].set(title=r"(b) $\mathrm{corr}(X_0,X_\tau)$", xlabel=r"lag $\tau$")
axs[1].legend()
z1 = rng.standard_normal(no)[None]
for thv, c in zip([0.5, 2.0, 8.0], [GREEN, BLUE, RED]):
    axs[2].plot(to, paths(1.5, ou_step(thv, m, s_ou, dto), z1)[0], color=c, lw=0.8, label=rf"$\theta={thv:g}$")
axs[2].set(title=r"(c) same shocks, three $\theta$", xlabel="$t$", ylim=(None, axs[2].get_ylim()[1] + 1))
axs[2].legend(fontsize=6.5, ncol=3, loc="upper center", handlelength=1, columnspacing=0.6)
fig.tight_layout()
save(fig, "ou_stationary")

# ---------------------------------------------------------------- 4. Short-rate models (VIR): Vasicek and CIR
a, b, sv, r0, Tr, nr = 0.5, 0.05, 0.02, 0.02, 10.0, 520      # weekly steps, 10 years
sc = sv / sqrt(b)                       # CIR vol chosen so both models share the same long-run variance
dtr = Tr / nr
tr = np.linspace(0, Tr, nr + 1)
num.update(CIRSigma=f"{sc:.4f}", FellerLHS=f"{2 * a * b:.3f}", FellerRHS=f"{sc ** 2:.4f}")
assert 2 * a * b >= sc ** 2                                    # Feller condition: CIR never hits 0

Rv = paths(r0, ou_step(a, b, sv, dtr), rng.standard_normal((M, nr)))
e, c = np.exp(-a * dtr), sc ** 2 * (1 - np.exp(-a * dtr)) / (4 * a)
nu = 4 * a * b / sc ** 2
Rc = np.empty_like(Rv)
Rc[:, 0] = r0
for i in range(nr):                                           # exact CIR step: scaled noncentral chi-square
    Rc[:, i + 1] = c * rng.noncentral_chisquare(nu, Rc[:, i] * e / c)

vmean = lambda tt, x0=r0: b + (x0 - b) * np.exp(-a * tt)
vvar = lambda tt: sv ** 2 / (2 * a) * (1 - np.exp(-2 * a * tt))
cvar = lambda tt: r0 * sc ** 2 / a * (np.exp(-a * tt) - np.exp(-2 * a * tt)) + b * sc ** 2 / (2 * a) * (1 - np.exp(-a * tt)) ** 2


def bond_vasicek(tau, x0):
    B = (1 - np.exp(-a * tau)) / a
    return np.exp((b - sv ** 2 / (2 * a ** 2)) * (B - tau) - sv ** 2 * B ** 2 / (4 * a) - B * x0)


def bond_cir(tau, x0):
    h = sqrt(a * a + 2 * sc ** 2)
    den = (h + a) * (np.exp(h * tau) - 1) + 2 * h
    A = (2 * h * np.exp((a + h) * tau / 2) / den) ** (2 * a * b / sc ** 2)
    return A * np.exp(-2 * (np.exp(h * tau) - 1) / den * x0)


def integral(R):                                              # trapezoid rule for int_0^t r ds
    return np.concatenate([np.zeros((M, 1)), np.cumsum((R[:, 1:] + R[:, :-1]) / 2 * dtr, 1)], 1)


Iv, Ic = integral(Rv), integral(Rc)
j1, j5 = int(1 / dtr), int(5 / dtr)
check("Vasicek", r"$\mathbb{E}[r_1]$", Rv[:, j1], vmean(1))
check("Vasicek", r"$\mathrm{Var}[r_1]$", (Rv[:, j1] - vmean(1)) ** 2, vvar(1))
check("Vasicek", r"$P(0,5)$", np.exp(-Iv[:, j5]), bond_vasicek(5, r0))
check("Vasicek", r"$P(0,10)$", np.exp(-Iv[:, -1]), bond_vasicek(10, r0))
pneg = float(Phi(-vmean(Tr) / sqrt(vvar(Tr))))
check("Vasicek", r"$\mathbb{P}(r_{10}<0)$", (Rv[:, -1] < 0).astype(float), pneg)
check("CIR", r"$\mathbb{E}[r_1]$", Rc[:, j1], vmean(1))
check("CIR", r"$\mathrm{Var}[r_1]$", (Rc[:, j1] - vmean(1)) ** 2, cvar(1))
check("CIR", r"$P(0,5)$", np.exp(-Ic[:, j5]), bond_cir(5, r0))
check("CIR", r"$P(0,10)$", np.exp(-Ic[:, -1]), bond_cir(10, r0))
assert Rc.min() > 0
num.update(PNegTh=f"{100 * pneg:.2f}", PNegSim=f"{100 * (Rv[:, -1] < 0).mean():.2f}",
           PNegEver=f"{100 * (Rv.min(1) < 0).mean():.1f}", CIRMin=f"{100 * Rc.min():.3f}",
           VasMin=f"{100 * Rv.min():.2f}", YInf=f"{100 * (b - sv ** 2 / (2 * a ** 2)):.2f}")

fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.6), sharey=True)
for ax, R, name in [(axs[0], Rv, "(a) Vasicek"), (axs[1], Rc, "(b) CIR")]:
    fan(ax, tr, 100 * R, BLUE)
    ax.plot(tr, 100 * vmean(tr), color=ORANGE, ls="--", lw=1.2, label="theoretical mean")
    ax.axhline(0, color=RED, lw=0.8)
    ax.set(title=name, xlabel="$t$ (years)", xlim=(0, Tr))
axs[0].set_ylabel("short rate $r_t$ (%)")
fig.tight_layout()
fig.legend(*axs[0].get_legend_handles_labels(), ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.0))
save(fig, "rate_paths")

fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.2))
x = np.linspace(-0.03, 0.14, 400)
axs[0].hist(100 * Rv[:, -1], bins=80, density=True, color=BLUE, alpha=0.45, label="Vasicek")
axs[0].hist(100 * Rc[:, -1], bins=80, density=True, color=ORANGE, alpha=0.45, label="CIR")
axs[0].plot(100 * x, npdf(x, vmean(Tr), sqrt(vvar(Tr))) / 100, color=DARK, lw=1.1)
axs[0].axvspan(-3, 0, color=RED, alpha=0.08)
axs[0].set(title="(a) $r_{10}$ (%)", xlim=(-3, 14))
axs[0].legend(fontsize=7)
tt = tr[1:]
axs[1].plot(tt, 100 * Phi(-vmean(tt) / np.sqrt(vvar(tt))), color=DARK, lw=1.3, label="theory")
axs[1].plot(tt[::13], 100 * (Rv[:, 1::13] < 0).mean(0), "o", color=BLUE, ms=2.5, label="Vasicek sim.")
axs[1].plot(tt[::13], 100 * (Rc[:, 1::13] < 0).mean(0), "s", color=ORANGE, ms=2.5, label="CIR sim.")
axs[1].set(title=r"(b) $\mathbb{P}(r_t<0)$ (%)", xlabel="$t$")
axs[1].legend(fontsize=6.5)
taus = np.linspace(0.05, 10, 200)
for x0, ls in [(0.02, "-"), (0.05, "--"), (0.09, ":")]:
    axs[2].plot(taus, -100 * np.log(bond_vasicek(taus, x0)) / taus, color=BLUE, ls=ls, lw=1.1)
    axs[2].plot(taus, -100 * np.log(bond_cir(taus, x0)) / taus, color=ORANGE, ls=ls, lw=1.1)
yrs = np.arange(1, 11)
axs[2].plot(yrs, -100 * np.log(np.exp(-Iv[:, yrs * 52]).mean(0)) / yrs, "o", color=BLUE, ms=3)
axs[2].plot(yrs, -100 * np.log(np.exp(-Ic[:, yrs * 52]).mean(0)) / yrs, "s", color=ORANGE, ms=3)
axs[2].set(title="(c) yield curve $y(0,\\tau)$ (%)", xlabel=r"maturity $\tau$")
axs[2].text(3.2, 1.0, "$r_0=2\\%$ solid, $5\\%$ dashed,\n$9\\%$ dotted; marks: Monte Carlo", fontsize=6.3, color=GREY)
axs[2].set_ylim(0.8, None)
fig.tight_layout()
save(fig, "rate_compare")

# ---------------------------------------------------------------- overview: one path of each process
fig, axs = plt.subplots(1, 4, figsize=(6.3, 1.7))
for ax, (y, tx, ttl) in zip(axs, [(W[0], t, "Brownian motion"), (S[0], t, "geometric BM"),
                                  (X[0], to, "Ornstein-Uhlenbeck"), (100 * Rv[0], tr, "Vasicek rate (%)")]):
    ax.plot(tx, y, color=BLUE, lw=0.7)
    ax.set_title(ttl, fontsize=8)
    ax.tick_params(labelsize=7)
fig.tight_layout()
save(fig, "overview")

# ---------------------------------------------------------------- tables
with open(os.path.join(TAB, "moments.tex"), "w") as f:
    last = None
    for g, name, th_, est, se, z in rows:
        if last and g != last:
            f.write("\\midrule\n")
        sci = lambda v, p: "$" + f"{v:.{p}g}".replace("e-0", r"\times10^{-").replace("e-", r"\times10^{-") + ("}" if "e" in f"{v:.{p}g}" else "") + "$"
        f.write(f"{g if g != last else ''} & {name} & {sci(th_, 5)} & {sci(est, 5)} & {sci(se, 2)} & ${z:+.2f}$ \\\\\n")
        last = g
    f.write("\\bottomrule\n")   # inside the file: \input followed by \bottomrule breaks \noalign
num["MaxZ"] = f"{max(abs(r[-1]) for r in rows):.2f}"
num["NChecks"] = str(len(rows))
with open(os.path.join(TAB, "numbers.tex"), "w") as f:
    for k, v in num.items():
        f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
print(f"{len(rows)} checks passed, max |z| = {num['MaxZ']}")
print(num)
