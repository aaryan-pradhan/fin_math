# Financial Mathematics: a Euclid book

## Context
One LaTeX book, one PDF (`build/main.pdf`), that replaces everything else in `fin_math/`: the handwritten lecture PDF, the 31 notes in `notes/*.html`, the 44 video transcripts, the formula sheet, the CT-2 memorize list, the problem notes and the past-paper solutions. It is the final source for this course. Read top to bottom, it is the whole course. Read only the formula sheets, it is the whole revision.

## Decisions (grill log, 2026-11-12)
1. **Source.** Backbone: `../lectures_all_1-26.pdf` (146 pages, handwritten scans, no text layer, so pages are read as images). It decides content, order and notation. Slides (p.77–85, 94–104, 115–124, 134–141) fold into their chapter. Extra explanation comes from `notes/*.html` (his own; keep their way of explaining, esp. Part 0 and filtrations) and `post-midsem/*.md`. Web explanations are allowed for clarity; they never override the PDF's notation.
2. **Purpose.** Revision reference and complete resource. Extremely undergraduate-level maths, simple words, nothing over-complicated.
3. **Assumed knowledge.** Calculus (derivatives, integrals, Taylor series, sums of series), sets, matrices. Part 0 (probability review, p.1–13) is in the book but marked "skip if revised"; later chapters list what they use from it by name.
4. **Scope and order.** PDF order, with moves only where Euclid order forces. A topic with problems is followed by its own Problems chapter (sources: p.55–58, p.68–76, problem notes, CT-1, midsem 2024/25, endsem 2025, assignments). Proofs are optional reading: statement first, Step-n proof below, nothing later needs a proof to have been read. A proof beyond undergraduate maths is omitted with one line (e.g. Doob–Dynkin, separation theorem, existence results).
5. **Numbers.** python3 recomputes every number; `VERIFY` = `verify.py` (Monte Carlo checks of stochastic claims, 95% interval).
6. **Chapter shape.** question box → whatfor box (ends with the skip line: "Skipping? Read the formula sheet on p.N.") → prereq box → body → **Formula sheet** (CT-2 cards: Formula → Use when → How to plug → Caveats → Example; each card names its symbols so it reads alone). The formula sheet replaces the recall sheet.
7. **Figures.** As many as help: any idea a picture can carry gets one (trees, paths, reflection, partitions, densities, payoffs). TikZ/pgfplots; random paths from seeded data in `figs/` written by `figs.py`.

## Notation lock
| Item | Lock |
|---|---|
| Probability space | $(\Omega,\mathcal F,P)$; events $A,B$; $\mathcal B(\R)$ Borel sets |
| Random variables | Part 0: $\xi,\eta$ (as the PDF), also $X,Y$ |
| Expectation | `\E_P` under the real-world $P$; `\E_{P^*}` under the risk-neutral $P^*$ |
| Filtration | $\mathbb F=(\mathcal F_t)$; filtered space $(\Omega,\mathcal F,\mathbb F,P)$ |
| Processes | discrete $X_n$/$X_t$; SBM $W(t)$ or $W_t$; BM with drift/variance $B(t)$; GBM $X(t)=e^{Y(t)}$ |
| Stopping | $\tau$ stopping time; $T_a$ hitting time of $a$; $M(t)=\max_{0\le s\le t}W(s)$ |
| Normal | $\Phi$ standard normal cdf; $N(\mu,\sigma^2)$ |
| Itô | $dX_t=a_t\,dt+b_t\,dW_t$; $(dW_t)^2=dt$ |
| Market | stock $S_t$, bond $B_t=(1+r)^t$ or $e^{rt}$, $u,d$, $p^*$, portfolio $(\Delta,b)$, strategy $\Phi_n$, claim $X$, fair price $X^*$/$V_0$, strike $K$ |

## Source inventory (every fin_math file → where it goes)
| File(s) | Goes to |
|---|---|
| lectures_all_1-26.pdf p.1–58 | Ch 1–19 (backbone) |
| lectures_all_1-26.pdf p.59–145 | Ch 20–27 (backbone); slide pages fold in |
| notes: starting_pieces, almost_surely | Ch 1 |
| notes: random_variables, doob_dynkin_lemma, distribution_functions, densities_and_joint_distributions | Ch 2 |
| notes: expectation_and_integration, change_of_variables_expectation | Ch 3 |
| notes: conditional_probability_and_independence, conditional_expectation_and_sigma_fields | Ch 4 |
| notes: filtrations_and_martingales, binomial_model_and_martingale_properties | Ch 5 |
| notes: brownian_motion_and_canonical_martingales, additive_and_geometric_random_walks | Ch 6 |
| notes: stopping_times, stopped_process_martingale, optimal_stopping_theorem, gambling_strategies | Ch 7 |
| notes: martingale_sheet_problems; class_test_1 (MG parts); PDF p.55–58, 73–76 | Ch 8 (Problems) |
| notes: brownian_motion_density_and_diffusion, wiener_process_axioms_levy_and_random_walk | Ch 9 |
| notes: brownian_bridge_and_conditional_distributions (conditional part) | Ch 10 |
| notes: brownian_motion_with_drift_and_exit_probabilities, gamblers_ruin_problem_derivation | Ch 11 |
| notes: geometric_brownian_motion | Ch 12 |
| notes: multivariate_distribution, gaussian_processes_and_mvn_conditioning, brownian_bridge (bridge part) | Ch 13 |
| notes: brownian_motion_hitting_times_and_maximum, joint_distribution_of_bm_and_maximum | Ch 14 |
| notes: brownian_motion_short_problems, brownian_motion_additional_problems; assignments bm*, CT-1, midsem 2024/25 (BM parts) | Ch 15 (Problems) |
| notes: ito_integral | Ch 16 |
| notes: ito_formula; PDF p.68–70 | Ch 17 |
| notes: stochastic_differential_equations; PDF p.70–72 | Ch 18 |
| notes: martingale_bm_ito_problems; assignment mg_bm_stocal_sde; endsem (Itô parts) | Ch 19 (Problems) |
| notes: arbitrage_and_risk_neutral_pricing; post-midsem p059-063 | Ch 20 |
| post-midsem p064-065, p065-067 | Ch 21 |
| post-midsem p086-087, p087-092, p092-093 | Ch 22 |
| post-midsem p105-109, p109-111, p111-114 | Ch 23 |
| post-midsem p125-129 | Ch 24 |
| post-midsem p130-133 | Ch 25 |
| post-midsem p142-143, p143-145 | Ch 26 |
| notes: binomial_and_black_scholes_problems; assignments intro_finance*; endsem 2025 (finance parts) | Ch 27 (Problems) |
| FinMath Formula Sheet.pdf / notes/formula_sheet.html, notes/ct2_memorize | every chapter's formula sheet |
| pre-midsem/*.md | dropped: verbatim copies of notes/*.html |
| videos/ | dropped: renders of the transcripts |
| assignments/individual_project | dropped: a project report, not course content |
| past_papers/*.pdf | via their solution notes (Ch 8, 15, 19, 27) |

## Topic plan
Needs must appear in an earlier row's Introduces, or in "Before you start".
| # | Title | PDF pages | Needs | Introduces | Status |
|---|---|---|---|---|---|
| 1 | Probability spaces | 1–4 | sets, series | σ-field, Borel sets, probability measure, continuity of P, almost surely, Borel–Cantelli, filtration (first look) | written |
| 2 | Random variables and distributions | 4–7 | 1 | random variable, σ(ξ), Borel function, Doob–Dynkin, distribution, d.f., density, discrete, joint density, normal | written |
| 3 | Expectation | 7–9, 55 | 2 | integrable, E as integral, indicator, step function, E h(ξ), normal mgf, Markov/Chebyshev | written |
| 4 | Independence and conditional expectation | 9–13 | 3 | conditional prob, total prob, independence (events, r.v.s, σ-fields), E(X∣𝒢), CE1–CE4, tower | written |
| 5 | Filtrations and martingales | 13–16 | 4 | discrete process, filtration, adapted, filtered space, binomial tree, martingale, sub/super, constant mean | written |
| 6 | Random walks and the Wiener process | 16–20 | 5 | stochastic process, sample path, Wiener process (axioms), W, W²−t, exponential MG, random walk, geometric random walk | written |
| 7 | Stopping times and optional stopping | 21–24 | 6 | stopping time, entry/hitting time, stopped process, optional stopping thm, no beating a fair game | written |
| 8 | Problems: martingales and stopping | 55–58, 73–76 | 7 | — | written |
| 9 | Brownian motion from random walks | 25–26 | 6 | scaling limit, density of W(t), heat equation, BM with variance σ² | written |
| 10 | Joint and conditional laws of Brownian motion | 26–27 | 9 | joint density, conditional law W(s)∣W(t) | written |
| 11 | Drift and gambler's ruin | 27–32 | 7, 9 | BM with drift, gambler's ruin, exit probabilities | written |
| 12 | Geometric Brownian motion | 32–34 | 11 | GBM, its mean, log-normal | written |
| 13 | Gaussian processes and the Brownian bridge | 34–39 | 10 | MVN, joint mgf, Gaussian process, cov min(s,t), Brownian bridge, integrated BM | todo |
| 14 | Hitting times and the maximum | 40–43 | 13, 7 | T_a law, reflection principle, M(t), joint law of W and M | todo |
| 15 | Problems: Brownian motion | — | 14 | — | todo |
| 16 | The Itô integral | 44–46 | 14 | Itô integral, isometry, ∫W dW, quadratic variation | todo |
| 17 | Itô processes and Itô's formula | 46–49, 68–70 | 16 | Itô process, multiplication table, Itô formula, product/quotient rule | todo |
| 18 | Stochastic differential equations | 50–54, 70–72 | 17 | SDE, OU, Vasicek, CIR, GBM as SDE | todo |
| 19 | Problems: Itô calculus and SDEs | — | 18 | — | todo |
| 20 | Arbitrage and risk-neutral pricing | 59–63, 77–85 | 4 | discounting, option, arbitrage, risk-neutral probability, arbitrage theorem | todo |
| 21 | Derivatives and replication | 64–67 | 20 | forward, call, put, American, contingent claim, replicating portfolio | todo |
| 22 | The single-period binomial market | 86–93, 94–104 | 21 | portfolio, trading strategy, self-financing, NA principle, perfect hedge, p*, put–call parity | todo |
| 23 | The fundamental theorems (finite market) | 105–114, 115–124 | 22 | convex hull, hyperplane, EMM, Thm 2 (NA⇔EMM), Thm 3 (pricing), complete market, Thm 4 | todo |
| 24 | The multiperiod binomial market | 125–129, 134–138 | 23 | backward induction, V_t formula, discounted price MG | todo |
| 25 | From binomial to Black–Scholes | 130–133, 139–141 | 24, 12 | binomial call formula, continuous limit, Black–Scholes formula | todo |
| 26 | Martingale pricing in continuous time | 142–145 | 25, 18 | P_t(X), Black–Scholes market, EMM condition | todo |
| 27 | Problems: option pricing | — | 26 | — | todo |
