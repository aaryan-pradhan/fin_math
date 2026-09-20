"""Check the G-function branches (§14), binomial pricing (§M4) and Ito calculus (§I).

Run: python test_joint_wm.py
"""
import math, random
from statistics import NormalDist

Phi = NormalDist().cdf


def G(b, c, t):
    """P(W(t) <= b, M(t) >= c) -- formula sheet 14.1."""
    s = math.sqrt(t)
    if c <= 0:
        return Phi(b / s)
    if b <= c:
        return 1 - Phi((2 * c - b) / s)
    return 1 + Phi(b / s) - 2 * Phi(c / s)


def rect(a, b, c, d, t):
    """P(a < W(t) <= b, c < M(t) <= d) -- formula sheet 14.3."""
    return (G(b, c, t) - G(a, c, t)) - (G(b, d, t) - G(a, d, t))


def mc(a, b, c, d, t, n=400_000, steps=2000, seed=0):
    """Monte Carlo on a fine random walk."""
    rng = random.Random(seed)
    dt = t / steps
    sd = math.sqrt(dt)
    hits = 0
    for _ in range(n):
        w = m = 0.0
        for _ in range(steps):
            w += rng.gauss(0, sd)
            if w > m:
                m = w
        if a < w <= b and c < m <= d:
            hits += 1
    return hits / n


def replicate(S0, u, d, r, payoff):
    """Delta, B, price -- formula sheet M4.3."""
    Vu, Vd = payoff(u * S0), payoff(d * S0)
    delta = (Vu - Vd) / ((u - d) * S0)
    B = (u * Vd - d * Vu) / ((1 + r) * (u - d))
    return delta, B, delta * S0 + B


def risk_neutral(S0, u, d, r, payoff):
    """Price via p* -- formula sheet M4.2/M4.4."""
    p = (1 + r - d) / (u - d)
    return (p * payoff(u * S0) + (1 - p) * payoff(d * S0)) / (1 + r)


def fair_c(S0, Su, Sd, K):
    """No-sure-win option cost -- formula sheet M4.5 (present values, no discounting)."""
    p = (S0 - Sd) / (Su - Sd)
    return p * max(Su - K, 0) + (1 - p) * max(Sd - K, 0)


def check_binomial():
    put = lambda S: max(225 - S, 0)

    # CT-2 2025 Q1/Q2: (Delta, B) = (-0.875, 190.22), price 15.22
    delta, B, price = replicate(200, 1.25, 0.25, 0.15, put)
    assert abs(delta - (-0.875)) < 1e-12, delta
    assert abs(B - 190.22) < 5e-3, B
    assert abs(price - 15.22) < 5e-3, price

    # replication and risk-neutral must agree, here and on random trees
    assert abs(price - risk_neutral(200, 1.25, 0.25, 0.15, put)) < 1e-9
    for S0, u, d, r, K in [(100, 1.2, 0.8, 0.05, 90), (60, 5 / 3, 1 / 3, 0.0, 80),
                           (400, 1.35, 0.6, 0.15, 500), (5, 6 / 5, 8 / 9, 1 / 9, 5)]:
        for f in (lambda S: max(S - K, 0), lambda S: max(K - S, 0)):
            assert abs(replicate(S0, u, d, r, f)[2] - risk_neutral(S0, u, d, r, f)) < 1e-9

    # put-call parity falls out of the same tree (M4.6)
    S0, u, d, r, K = 100, 1.2, 0.8, 0.05, 90
    C = risk_neutral(S0, u, d, r, lambda S: max(S - K, 0))
    P = risk_neutral(S0, u, d, r, lambda S: max(K - S, 0))
    assert abs((C - P) - (S0 - K / (1 + r))) < 1e-9

    # M4.5, the three papers that asked it
    assert abs(fair_c(50, 100, 25, 85) - 5) < 1e-12      # Midsem 2025 Q1(c)
    assert abs(fair_c(40, 100, 25, 75) - 5) < 1e-12      # CT-2 2025 Q5
    assert abs(fair_c(75, 200, 50, 120) - 80 / 6) < 1e-12  # Midsem 2024 Q1(a)

    print(f"binomial: (delta,B) = ({delta}, {B:.2f}), put = {price:.2f}; "
          f"replication == risk-neutral on all trees")


def check_ito(seed=1, n=200_000, t=1.0):
    """Ito integral, isometry, and the expectations behind §I1, §I5, §I7."""
    rng = random.Random(seed)

    # --- §I1.7: the left-endpoint sum IS 1/2 W^2 - 1/2 sum(dW)^2, exactly.
    dt = t / n
    sd = math.sqrt(dt)
    w = 0.0
    left_sum = 0.0   # sum W_{i-1} (W_i - W_{i-1})
    qv = 0.0         # sum (dW)^2
    for _ in range(n):
        dw = rng.gauss(0, sd)
        left_sum += w * dw
        qv += dw * dw
        w += dw
    assert abs(left_sum - (0.5 * w * w - 0.5 * qv)) < 1e-6, "algebraic identity broken"

    # --- §I1.8: quadratic variation converges to t (this is the whole -t/2)
    assert abs(qv - t) < 0.02, qv

    # --- §I1.5 / §I1.4: Var(int_0^1 t^k dW) = 1/(2k+1), by quadrature
    def quad(f, a, b, m=200_000):
        h = (b - a) / m
        return h * sum(f(a + (i + 0.5) * h) for i in range(m))

    for k in (1, 2, 3, 4):
        assert abs(quad(lambda x, k=k: x ** (2 * k), 0, 1) - 1 / (2 * k + 1)) < 1e-9, k

    # --- §I7.3: OU variance = sigma^2 (1 - e^{-2rt}) / (2r), by quadrature
    for r, sig, T in [(1.0, 1.0, 1.0), (2.0, 0.5, 3.0), (0.3, 1.7, 5.0)]:
        num = sig ** 2 * quad(lambda u, r=r, T=T: math.exp(-2 * r * (T - u)), 0, T)
        closed = sig ** 2 * (1 - math.exp(-2 * r * T)) / (2 * r)
        assert abs(num - closed) < 1e-7, (r, sig, T)

    # --- §I5.4: E[cos W_t] = e^{-t/2}, by quadrature against the N(0,t) density
    for T in (0.5, 1.0, 4.0):
        sT = math.sqrt(T)
        dens = lambda x, sT=sT: math.exp(-x * x / (2 * sT * sT)) / (sT * math.sqrt(2 * math.pi))
        got = quad(lambda x, d=dens: math.cos(x) * d(x), -12 * sT, 12 * sT)
        assert abs(got - math.exp(-T / 2)) < 1e-7, (T, got)

    # --- §I4.1 / §I8.1: moment recursion E[W^n] = n(n-1)/2 * int E[W^{n-2}]
    #     n=2 -> t, n=4 -> 3t^2, n=6 -> 15t^3
    for T in (1.0, 2.5):
        m2 = quad(lambda s: 1.0, 0, T)
        m4 = 6 * quad(lambda s: s, 0, T)
        m6 = 15 * quad(lambda s: 3 * s * s, 0, T)
        assert abs(m2 - T) < 1e-7 and abs(m4 - 3 * T ** 2) < 1e-6 and abs(m6 - 15 * T ** 3) < 1e-5
        # Midsem 2025 Q4(a): Var(W_t^2) = E[W^4] - t^2 = 2t^2
        assert abs((m4 - T ** 2) - 2 * T ** 2) < 1e-6

    print(f"ito: int W dW = {left_sum:.4f} vs 1/2 W^2 - t/2 = {0.5 * w * w - 0.5 * t:.4f}; "
          f"QV = {qv:.4f} (t = {t}); isometry, OU variance, E[cos W_t] all exact")


def main():
    t = 4.0

    # branch continuity at b == c
    assert abs(G(2, 2, t) - (1 - Phi(1.0))) < 1e-12

    # b -> infinity recovers P(M >= c) = 2(1 - Phi(c/sqrt t))
    assert abs(G(1e9, 2, t) - 2 * (1 - Phi(1.0))) < 1e-9

    # c <= 0 collapses to the marginal of W
    assert abs(G(1.5, -1, t) - Phi(0.75)) < 1e-12

    # M >= W always: I strictly above J must vanish
    assert abs(rect(3, 4, 1, 2, t)) < 1e-12

    # marginal of M: let I be the whole line
    assert abs(rect(-1e9, 1e9, 2, 3, t) - 2 * (Phi(1.5) - Phi(1.0))) < 1e-9

    # Midsem 2025 Q5(b)
    ans = rect(1, 3, 2, 3, t)
    assert abs(ans - 0.1231) < 5e-5, ans

    # the wrong-branch answer the guard prevents
    bad = (1 - Phi((2 * 2 - 3) / 2)) - G(1, 2, t) - ((1 - Phi((2 * 3 - 3) / 2)) - G(1, 3, t))
    assert abs(bad - ans) > 0.05, "guard is not actually doing anything"

    print(f"P(1<W(4)<3, 2<M(4)<3) = {ans:.4f}   (naive reflection would give {bad:.4f})")
    check_binomial()
    check_ito()
    print("all asserts passed")

    if __import__("sys").argv[1:2] == ["--mc"]:
        est = mc(1, 3, 2, 3, t)
        print(f"monte carlo = {est:.4f}  (analytic {ans:.4f})")
        assert abs(est - ans) < 0.004, (est, ans)
        print("monte carlo agrees")


if __name__ == "__main__":
    main()
