# FinMath Notes

Self-study notes on probability, measure theory and stochastic processes, written one Note at a time via the math-buddy routine.

## Language

**Note**:
One HTML page covering one concept, named in descriptive snake_case with no number prefix.
_Avoid_: Lecture, file

**Module**:
A named, ordered group of Notes (e.g. Foundations, Martingales).
_Avoid_: Chapter, section, folder

**TOC**:
The single source of truth for which Notes exist, which Module each belongs to, and their order (`toc.json`).
_Avoid_: index (that is the generated page), ordering

**Formula Sheet**:
A dense reference page of results across Notes, with no Socratic build-up; listed under the Reference Module.
Every entry is a **Card**, and a Card is only complete with all three parts (see **Card**).
Organised in Parts, each covering a set of Modules, in TOC order: Part I is Foundations, Expectation and Martingales (sections F, E, M); Part II is Random walks and Brownian motion (sections 1-14); Part III is Stochastic calculus (sections I); Part IV is Option pricing (sections A). A Part is added whole, never piecemeal.
Section numbering is frozen once published, so cross-references never rot; a new Part gets a new prefix rather than renumbering the old one.
_Avoid_: cheat sheet, summary note

**Card**:
One entry on the Formula Sheet. Three mandatory parts, in order:
1. the formula,
2. **Use when** — the cases and guards that decide whether this formula applies at all,
3. **Paper / Trick** — a past-paper instance with its answer, or the one-line shortcut.
A formula with no guard and no instance is not a Card; it is a fact the reader cannot route to.
_Avoid_: entry, item, block (a Block is the Note vocabulary, not the Sheet's)

**Guard**:
The condition under which a formula is valid. A Guard names what to do when it fails, never merely that it fails.
Example: $P(W_t \le b, M_t \ge c)$ has the guard $b \le c$; when it fails the answer is a *different formula*, not zero.

## Relationships

- A **Module** contains one or more **Notes**, in order
- A **Note** belongs to at most one **Module**; a Note absent from the **TOC** is shown as Unsorted
- The **TOC** is an ordered list of **Modules**

## Example dialogue

> **Dev:** "To move `stopping_times` before `martingales`, do we rename the file?"
> **Domain expert:** "No — filenames never carry order. Edit its position in the **TOC**."

## Scope

Optimal control (MDPs, Bellman, American derivatives) is out of scope.

## Flagged ambiguities

- "lecture" was used for Notes — resolved: the unit is a **Note**; order lives only in the **TOC**, never in filenames.
