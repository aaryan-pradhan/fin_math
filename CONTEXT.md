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
_Avoid_: cheat sheet, summary note

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
