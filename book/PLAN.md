# Financial Mathematics: a Euclid book

## Context
One LaTeX book, one PDF (`build/main.pdf`), that replaces everything else in `fin_math/`: the handwritten lecture PDF, the 31 notes in `notes/*.html`, the 44 video transcripts, the formula sheet, the CT-2 memorize list, the problem notes and the past-paper solutions. It is the final source for this course. Read top to bottom, it is the whole course. Read only the formula sheets, it is the whole revision.

## Decisions (grill log, 2026-11-12)
1. **Source.** Backbone: `../lectures_all_1-26.pdf` (146 pages, handwritten scans, no text layer, so pages are read as images). It decides content, order and notation. Slides (p.77–85, 94–104, 115–124, 134–141) fold into their chapter. Extra explanation comes from `notes/*.html` (his own; keep their way of explaining, esp. Part 0 and filtrations) and `post-midsem/*.md`. Web explanations are allowed for clarity; they never override the PDF's notation.
2. **Purpose.** Revision reference and complete resource. Extremely undergraduate-level maths, simple words, nothing over-complicated.
3. **Assumed knowledge.** Calculus (derivatives, integrals, Taylor series, sums of series), sets, matrices. Part 0 (probability review, p.1–13) is in the book but marked "skip if revised"; later chapters list what they use from it by name.
4. **Scope and order.** PDF order, with moves only where Euclid order forces. A topic with problems is followed by its own Problems chapter (sources: p.55–58, p.68–76, problem notes, CT-1, midsem 2024/25, endsem 2025, assignments). Proofs are optional reading: statement first, Step-n proof below, nothing later needs a proof to have been read. A proof beyond undergraduate maths is omitted with one line (e.g. Doob–Dynkin, separation theorem, existence results).
5. **Numbers.** python3 recomputes every number; `VERIFY` = `verify.py` (Monte Carlo checks of stochastic claims, 95% interval).
6. **Chapter shape.** question box → whatfor box (ends with the skip line) → prereq box → body → **Formula sheet** of general-formula cards (euclid-book §2a, 2026-11-12): each card is the single most general formula the course uses, boxed, followed by numbered plug-in rows (given → plug → result, valid when, numbers). Every smaller formula is a row of some card; nothing is repeated across sheets. A card sits beneath the chapter that unlocks it. He revises only from these sheets.
8. **Problems** move to one final Part at the end of the book; every solution is Card N row k → plug → answer.
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
| exam questions on Markov decision processes / optimal betting | dropped: optimal control is out of syllabus (CONTEXT.md) |

## Topic plan
Numbering after the 2026-11-12 restructure: problem chapters moved to the final Part "Problems" (files 90+), so body chapters renumbered.
| # | Title | PDF pages | Status |
|---|---|---|---|
| 1 | Probability spaces | 1–4 | written |
| 2 | Random variables and distributions | 4–7 | written |
| 3 | Expectation | 7–9, 55 | written |
| 4 | Independence and conditional expectation | 9–13 | written |
| 5 | Filtrations and martingales | 13–16 | written |
| 6 | Random walks and the Wiener process | 16–20 | written |
| 7 | Stopping times and optional stopping | 21–24 | written |
| 8 | Brownian motion from random walks | 25–26 | written |
| 9 | Joint and conditional laws of BM | 26–27 | written (no card: rows of Card 10.1) |
| 10 | Drift and gambler's ruin | 27–32 | written |
| 11 | Geometric Brownian motion | 32–34 | written |
| 12 | Gaussian processes and the Brownian bridge | 34–39 | written |
| 13 | Hitting times and the maximum | 40–43 | written |
| 14 | The Itô integral | 44–46 | written |
| 15 | Itô processes and Itô's formula | 46–49, 68–70 | written |
| 16 | Stochastic differential equations | 50–54, 70–72 | written |
| 17 | Arbitrage and risk-neutral pricing | 59–63, 77–85 | written |
| 18 | Derivatives and replication | 64–67 | written |
| 19 | The single-period binomial market | 86–93, 94–104 | written |
| 20 | The fundamental theorems (finite market) | 105–114, 115–124 | written |
| 21 | The multiperiod binomial market | 125–129, 134–138 | written |
| 22 | From binomial to Black–Scholes | 130–133, 139–141 | written |
| 23 | Martingale pricing in continuous time | 142–145 | written |
| P | Problems: probability and martingales (90) | 55–58, 73–76 + sheets | written (card → plug → answer) |
| P | Problems: Brownian motion (91) | sheets, papers | written |
| P | Problems: Itô calculus and SDEs (92) | sheets, papers | written |
| P | Problems: option pricing (93) | sheets, papers | todo |

## Card catalogue (euclid-book §2a), current numbering
1.1 atoms · 1.2 union · 1.3 limits · 2.1 measurability · 2.2 P(ξ∈B) · 2.3 normal probabilities · 3.1 E h(ξ) · 3.2 variance of combinations · 3.3 normal exponential moment · 3.4 tail bound · 4.1 Bayes · 4.2 independence · 4.3 freeze and average · 5.1 one-step test · 6.1 independent increments · 7.1 stopping-time test · 7.2 optional stopping (exits, ruin, drift, lines, Laplace) · 7.3 stakes · 8.1 scaled walk · 8.2 heat equation · 10.1 law of x0+μt+σW given known values · 11.1 GBM · 12.1 jointly normal / Gaussian processes · 13.1 G(b,c) · 14.1 Itô integral · 15.1 Itô's formula · 16.1 linear SDE · 17.1 one-period pricing.
