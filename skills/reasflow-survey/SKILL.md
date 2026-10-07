---
name: reasflow-survey
description: Research and deliver either a full literature survey paper or a compact Related Works section with one strong Codex author, primary-source checks, and publication validation.
---

# ReasFlow Survey

Use this skill for a literature survey or Related Works request. The user chooses the deliverable. If unclear, infer from the requested context; ask only when the difference materially changes the work. A strong model owns the research and manuscript from start to finish. Make the plan and section structure flexible as evidence accumulates.

## Research and evidence

- Search the Web iteratively. Start with the problem and candidate original works; follow direct successors, important alternatives, and counterevidence. Prefer official proceedings, publishers, arXiv versions, and source PDFs for claims. Search results, abstracts, and citation graphs are leads.
- For each paper actually used, retain enough identity to avoid treating a preprint and its conference/journal version as separate contributions: title, authors, year, DOI or arXiv ID where available, and a source URL. Verify historical priority rather than assuming that the highest-ranked result is original.
- When comparing mathematical results, bind each stated rate or guarantee to its problem setting, assumptions, output criterion, counted resource, and source location. Split incompatible regimes instead of flattening them into one leaderboard.
- Before asserting that a problem remains open or a class of methods does not exist, search likely later work and synonyms through the task cutoff. State the bounded result of that search; do not turn non-retrieval into proof of absence.
- Revisit a small number of claims whose failure would change the paper's argument. Check the primary passage, formula, or derivation, and preserve a locator. Do not build a large mandatory claim ledger or invent entries to pass a tool.

Semantic Scholar and ReaScholar are **optional**. Use them only for a concrete missing metadata field, citation neighbor, paper detail, or structured mathematical-evidence need. A failed S2 call does not trigger a silent ReaScholar substitution. If an experiment specifies `s2-only`, use an explicit S2 source flag and report actual provenance.

## Full survey

Unless the user explicitly asks for a shorter or narrower deliverable, **full survey means a detailed long-form paper**: aim for 10,000–15,000 words of main text and roughly 100 distinct, relevant papers cited in the argument (normally 90–110, not merely listed in the bibliography). The 2026-09-30 five-page, 15-citation example was a deliberately shortened smoke test, not this default. If the topic as stated is too narrow to support that coverage honestly, broaden to its directly relevant neighboring methods and applications while keeping a clear boundary; disclose any remaining shortfall rather than padding citations or presenting an overview as complete.

Build a self-contained account with a useful organizing question, scope and cutoff, grounded field history, method families, common comparison axes, paper-specific mechanisms and limitations, counterexamples and partial resolutions, and a conclusion that distinguishes established results from conjectures. Give each major family enough space to explain representative algorithms, mathematical assumptions, guarantees, evaluation settings, and the changes introduced by later work. Synthesize across papers instead of writing one paragraph per citation. For a long-form survey, normally include a conceptual figure that makes the field's organizing logic visible and a second figure when it clarifies a distinct mechanism, comparison, or evidence pattern. Treat figures as part of the argument: explain them in the text, make captions self-contained, audit their mathematical claims and units, and inspect them in the rendered PDF. A table does not automatically replace a figure; omit figures only when none would improve understanding, and record that reason in the delivery note. There is no numerical figure quota.

Research and write iteratively: widen the source set as the argument exposes missing branches, then check that the final sections and references cover the claimed scope. Keep bibliographic identities and source locations for used works. Do not create a giant mandatory paper-card pool or freeze the outline before reading. Before calling the paper complete, inspect its actual main-text length, count distinct cited papers, check that the important branches have substantive discussion, and run the publication checker. A short draft or partial source map is progress, not final delivery. Explicit user length and scope instructions override these defaults.

Default files: `survey/survey.tex`, root `references.bib`, and, when TeX/PDF is requested, `survey/survey.pdf`. Write the TeX directly. Build a separate Related Works section only if requested.

## Related Works section

Write directly for the user's manuscript: its setting, terminology, and contribution. Group the closest prior work by meaningful distinctions, compare under the same axes, and state exactly where the user's problem or method differs. A section may be brief; do not force a survey-paper introduction, taxonomy, figures, gap agenda, or 45–55 citations. Honor an explicit word or citation target when supplied.

Default files: embeddable `related_works/related_works.tex` and root `references.bib`. Produce `related_works/related_works.pdf` as a preview when requested or when it helps inspect layout. Preserve the user's existing BibTeX keys and style if working inside an existing paper.

## Delivery

Use the bundled standard-library checker after writing:

```bash
python3 .agents/skills/reasflow-survey/scripts/publication.py --mode survey --check-only
python3 .agents/skills/reasflow-survey/scripts/publication.py --mode related --check-only
```

If a PDF is required, rerun without `--check-only` and provide `--tectonic /path/to/tectonic` if it is not on `PATH`. The tool checks citation keys, BibTeX keys, canonical duplicates, TeX structure, compiler status, and PDF existence. It cannot certify that a source supports a mathematical claim; perform the source checks above. Inspect the rendered references and pages. Repair errors locally and rerun the checker. A passing mechanical report is not a substitute for source-grounded judgment.

The checker defaults to a 90-distinct-citation floor for full-survey mode and no citation floor for Related Works. This is only a coverage signal; it cannot judge relevance, depth, or source support. For an explicitly shorter survey, pass an appropriate `--min-citations N` override and state the changed scope. Deliver the manuscript, bibliography, compiled PDF if requested, and a concise note of actual length, cited-paper count, source checks, and any unfinished coverage.
