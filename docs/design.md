# Design and evidence boundary

The default is one writer with native Web research, source reading, a dynamic plan, and direct manuscript editing. This preserves the model's demonstrated strengths in taxonomy, chronology, comparison, and prose. The full-survey delivery contract is now long-form: roughly 10,000–15,000 main-text words and about 100 relevant papers cited in the argument, unless the user specifies a shorter scope. The repository adds mechanical checks for canonical bibliography identity, citation resolution, a default 90-citation floor in survey mode, and TeX/PDF delivery, plus source-first review of consequential claims. A citation count is necessary coverage evidence, not proof of quality.

## Decisions inherited from the earlier work

| Observation | Design consequence |
|---|---|
| GPT-5.6-Sol `ReaScholar+S2` vs `S2-only` gave a small positive long-survey macro in one later three-task test, but all three related-works results were negative; an earlier three-task test was broadly negative. | Neither S2 nor ReaScholar is a mandatory stage. Do not compress a generated long survey into related works by a fixed handoff. Write the requested output directly. |
| The Codex-first canary improved after removing staged writing, frozen outlines, worker handoff, and large upfront paper-card pools. It used GPT-5.6-Terra, not Sol. | One model owns research and writing. Tools supply evidence on demand, never a prescribed taxonomy or section plan. |
| The original canary's `s2-only` profile did not establish that S2 calls caused the gain. In a small later probe, Web found the tested original papers, while anonymous S2 returned irrelevant items or HTTP 429. | Native Web is default discovery. S2 stays an optional escape hatch for a concrete graph or metadata need. |
| Mathematical errors can survive syntax and bibliography gates; figures can introduce their own scientific errors. | Verify central equations, conditions, and comparison units against primary sources. Use figure tooling only when a figure serves the paper and audit its individual claims. |

The underlying comparison reports remain with the original research workspaces and are not runtime dependencies or part of this distribution. The public-facing conclusions above are deliberately narrower than a matched superiority claim.

## Minimal execution contract

1. Establish the actual deliverable: full survey or embeddable related works; respect user-specified scope and cutoff.
2. Search iteratively. Find original works, direct successors, and contradictory or partially resolving work. Open primary papers for consequential claims. Keep bibliographic identities distinct from search-result rank.
3. Write directly in the requested format. An unqualified full survey needs enough breadth and depth to meet the long-form contract: a clear organizing question, defensible scope, meaningful families, common comparison axes, evidence-rich sections, and bounded open questions. Related works needs the closest alternatives and a precise connection to the user's paper; it need not reproduce a full survey's taxonomy or future-work agenda.
4. Before delivery, inspect a handful of claims whose failure would materially change the paper: theorem conditions, rates and counted units, method priority, or field-wide absence. Record the source location or bounded search behind each. Do not manufacture a fixed number of claims or internal records.
5. Check actual main-text length and that cited works contribute to the argument, then run publication checks, compile if TeX/PDF is requested, inspect the final PDF, and repair observed defects locally. Report unresolved coverage, source, or metadata uncertainty. Do not label a partial overview as a complete full survey.

## Out of the default path

No mandatory S2 search budget, precomputed paper-card pool, Domain-to-outline conversion, frozen outline, multiple writing workers, separate related-works compressor, exhaustive claim ledger, figure quota, or mandatory long-form output when the user asked for a section. The near-100-paper full-survey target requires iterative discovery and substantive synthesis; it does not require a precomputed card pool. Optional source and design tools may be used for a concrete need.

The repository targets GPT-5.6-Sol and later strong models by using a short outcome contract rather than detailed step-by-step prompt control. It does not claim a new matched end-to-end superiority result. Before claiming that a future release beats the original Survey agent, compare full survey and related-works tasks under matched model, source access, output requirements, evaluation, and budget, including failed deliveries and costs.
