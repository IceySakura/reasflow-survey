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

Write a self-contained paper with a useful organizing question, scope and cutoff, grounded field history, method families, common comparison axes, paper-specific mechanisms and limitations, and a conclusion that distinguishes established results from conjectures. Cover the works needed for a complete argument, including counterexamples and partial resolutions. For a broad task comparable to the older long-survey benchmark, a 10,000+ word paper and 100+ relevant cited papers are reasonable targets. Adjust to the user's scope and avoid citation padding.

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

Keep task-specific targets out of the generic checker unless agreed in advance; use `--min-citations N` only for an explicit coverage floor. Deliver the manuscript, bibliography, compiled PDF if requested, and a concise note of the source and publication checks actually performed.
