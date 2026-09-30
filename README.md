# reasflow-survey

A survey-only Codex project for GPT-5.6-Sol and stronger models. It keeps the useful delivery checks from `reasflow-dev` while letting one capable model research, organize, and write the paper.

The agent has two outputs:

- **Full survey:** a substantial, self-contained review paper with a coherent field map, source-grounded comparisons, references, and a compiled PDF.
- **Related works:** a section that can be inserted into an existing paper, with its own citations and an optional preview PDF.

The requested topic, audience, cutoff, venue, length, must-cover works, and output format take precedence. If the task leaves them open, the agent chooses sensible targets from the field's size and tells the user what it chose. The long-paper targets used by the original Survey workflow (roughly 10,000 words and 100 relevant papers) remain supported; they are targets for an appropriately broad assignment, not universal validity gates. A related-works section can be short or as substantial as the user's paper needs.

## Why this version is smaller

The older Sol comparisons found mixed value from adding ReaScholar to an S2-based writer: some gains in long-survey lineage and synthesis, losses in related-works compression. A later Terra canary improved after removing fixed stages, frozen outlines, worker handoffs, large evidence pools, and default multi-skill loading. A small 2026-09-30 retrieval probe found that ordinary Web search could locate the tested original papers and official versions, while the anonymous S2 route was unreliable. These results motivate a **Web-first default**, not a claim that S2 or ReaScholar can never help. See [DESIGN.md](DESIGN.md) for the exact evidence boundary.

## Install into a project

The repository itself includes project-local `.codex/` and `.agents/` links, so it is ready to open in Codex after a restart. To add the agent to another project, run from this repository:

```bash
bash install.sh /path/to/project
```

The installer adds `.codex/config.toml`, `.codex/agents/survey.toml`, and `.agents/skills/reasflow-survey/`. It refuses to replace existing targets unless `--force` is given. Restart Codex in the target project so it loads the new config and skill. Choose the model in your Codex invocation or user config; this project does not override provider credentials or model settings.

Example requests inside an installed project:

```text
Write a full survey of decentralized optimization through July 2026. Compare assumptions, convergence criteria, and communication costs. Deliver LaTeX, bibliography, and PDF.
```

```text
Write a 1,500-word Related Works section for this paper, using its terminology and existing bibliography. Cover the closest methods and explain the precise difference from our setting. Deliver an embeddable TeX section.
```

The agent writes to `survey/survey.tex` or `related_works/related_works.tex` by default, with `references.bib` at the project root. Its publication checker is also usable directly:

```bash
python3 .agents/skills/reasflow-survey/scripts/publication.py --mode survey --check-only
python3 .agents/skills/reasflow-survey/scripts/publication.py --mode related --check-only
python3 .agents/skills/reasflow-survey/scripts/publication.py --mode both --tectonic /path/to/tectonic
```

The checker writes `build/publication_report.json`. With a TeX engine available, it also builds preview PDFs. `--check-only` runs offline structural, citation, and duplicate-identity checks without requiring a compiler. For a particular assignment, `--min-citations` can enforce an agreed coverage floor; the default is zero so a citation count cannot substitute for relevance.
Use `--bib path/to/existing.bib` when integrating a Related Works section into a paper with an existing bibliography.

## Optional evidence tools

Native Web search and primary sources are the default. Use Semantic Scholar only for a specific unresolved identity, metadata, or citation-neighbor question when its service is available; use ReaScholar only when structured mathematical evidence is part of the task. Neither is loaded or queried automatically. A search result is a lead, not proof of a theorem, historical priority, or an absence claim.

This repository does not copy the original multi-agent paper pipeline, cached corpora, experimental runners, hidden evaluators, or provider credentials.

## Development

```bash
python3 -m unittest discover -s tests -v
```

The package uses the Python standard library. Compilation uses a user-provided Tectonic binary or one on `PATH`. The repository is local and has no remote configured by default.
