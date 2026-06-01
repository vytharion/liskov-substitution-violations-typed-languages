# liskov-substitution-violations-typed-languages

Companion repository for the article at <https://oop.nicedx.com/liskov-substitution-violations-typed-languages/>.

A six-step catalogue of Liskov Substitution Principle violations that survive a strict type checker, with cross-language mirrors in Java, C#, and TypeScript, and a final refactor that makes the failures unrepresentable at the type level using composition, `@final` sealing, two-state `Union` sum types, and `Protocol`-bound contracts.

## What this project demonstrates

Each step builds one progressively deeper LSP violation, lets the type checker pass it, then exposes the runtime contract failure via tests:

1. **Square-Is-A-Rectangle** — the classic substitution lie. `Square` overrides `Rectangle`'s setters to keep `width == height`; any caller that resizes width and height independently gets a silently-wrong result.
2. **Postcondition weakening** — `RoundingRectangle` silently rounds caller-supplied dimensions, returning *less* than the base contract promised.
3. **Invariant + history-constraint violations** — `FlexibleCounter` breaks the parent's monotonic-value invariant; `RevisableDocument` breaks the publish-lock history constraint. Both pass `mypy`.
4. **Exception broadening + covariant return abuse** — across Java, C#, and TypeScript: an override widens the declared exception set, or narrows the return type in a way that fragments downstream callers.
5. **(Refactor preview)** — a partial refactor with composition + `Protocol`-typed return shapes + frozen invariants demonstrates the path the final step takes.
6. **Refactor with composition + sealed hierarchies + trait bounds** — every violation from steps 1-4 rebuilt so the substitution failure is statically rejected. 157 tests pass.

## Tech stack

- **Python 3.11+** with `mypy --strict` as the substitution lie detector.
- **pytest** for runtime verification of every violation + the refactored contract.
- **uv** for env / lockfile (see `pyproject.toml` + `uv.lock`).
- **Cross-language**: `cross_language/` mirrors selected steps in Java, C#, and TypeScript stubs to prove the same hole opens in every typed mainstream language.

## Prerequisites

- Python ≥ 3.11
- [`uv`](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `git` for stepping through commits

## Quick start

```bash
git clone https://github.com/vytharion/liskov-substitution-violations-typed-languages.git
cd liskov-substitution-violations-typed-languages
uv sync
uv run pytest -q
```

Expected: green at `HEAD` (157 tests, all refactored hierarchies substitution-safe). To feel each violation, check out an earlier step (see commit walkthrough below) and rerun the suite.

## Commit walkthrough

Step through the violations chronologically. Each commit leaves the tree in a runnable state — `uv run pytest -q` works at every commit.

| Step | Commit | Description |
|---|---|---|
| 1 | [`f5021fb`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/f5021fb) | Rectangle/Square hierarchy with passing tests that mask the LSP violation |
| 2 | [`1344964`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/1344964) | RoundingRectangle weakens the width/height setter postcondition by silently rounding caller-supplied dimensions |
| 3 | [`203b977`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/203b977) | FlexibleCounter weakens monotonic-value invariant; RevisableDocument breaks publish-lock history constraint |
| 4 | [`46ff779`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/46ff779) | Exception broadening and covariant return abuse across Java, C#, and TypeScript |
| 5 | [`db0dc85`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/db0dc85) | Refactor preview — composition, sealed hierarchies, Protocol-typed return shapes, frozen invariants for shapes / accounts / documents / counters / notifier / feed / inbox |
| 6 | [`6b98a8a`](https://github.com/vytharion/liskov-substitution-violations-typed-languages/commit/6b98a8a) | Final refactor — composition + sealed Protocol hierarchies + `@final` markers across every module from steps 1-4; 157 tests passing |

To replay a specific violation:

```bash
git checkout <step-sha>
uv sync
uv run pytest -q tests/<relevant_module>     # runs ONLY that step's affected tests
```

`git checkout main` returns to the fully-refactored state.

## Repo layout

```
src/
  accounts/        — step 3 history-constraint violation + step 6 sealed refactor
  contracts/       — Protocol bounds + sentinel @final marks (step 6)
  notifications/   — exception-broadening Notifier + step 6 sealed Notifier (step 4 + 6)
  refactored/      — step 5 refactor preview
  repository/      — step 6 composition-over-inheritance for repo pattern
  shapes/          — Rectangle/Square + RoundingRectangle (steps 1, 2)
  transports/      — step 6 sealed transport hierarchy
cross_language/    — Java, C#, TypeScript mirrors of selected violations
examples/          — short illustrative runs you can `python -m` to feel a violation
tests/             — pytest suite (157 cases at HEAD; earlier steps have fewer)
```

## Related reading

- **Liskov's original paper**: Barbara Liskov, _Data Abstraction and Hierarchy_, SIGPLAN Notices 23(5), 1988. The formal definition is sharper than the textbook square/rectangle illustration.
- **Strict mypy**: `mypy --strict` is the toolchain assumed throughout. Running with looser config will let some violations look like other bugs.
- **Companion article**: <https://oop.nicedx.com/liskov-substitution-violations-typed-languages/> — narrative + diagrams + tests-output for each step.

## License

MIT.
