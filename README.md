# reasflow-survey

A survey-only Codex project for GPT-5.6-Sol and stronger models. It keeps the useful delivery checks from `reasflow-dev` while letting one capable model research, organize, and write the paper.

The agent has two outputs:

- **Full survey:** a substantial, self-contained review paper with a coherent field map, source-grounded comparisons, references, and a compiled PDF.
- **Related works:** a section that can be inserted into an existing paper, with its own citations and an optional preview PDF.

The requested topic, audience, cutoff, venue, length, must-cover works, and output format take precedence. For an unqualified **full survey**, the default is a detailed 10,000–15,000-word paper with roughly 100 distinct, relevant papers cited in the argument (normally 90–110). A narrow topic should be placed in its directly relevant neighboring literature rather than silently reduced to a five-page overview; if the evidence still cannot support the target, the agent reports the shortfall. A Related Works section remains a separate, usually much shorter deliverable.

## Why this version is smaller

The older Sol comparisons found mixed value from adding ReaScholar to an S2-based writer: some gains in long-survey lineage and synthesis, losses in related-works compression. A later Terra canary improved after removing fixed stages, frozen outlines, worker handoffs, large evidence pools, and default multi-skill loading. A small 2026-09-30 retrieval probe found that ordinary Web search could locate the tested original papers and official versions, while the anonymous S2 route was unreliable. These results motivate a **Web-first default**, not a claim that S2 or ReaScholar can never help. See [the design notes](docs/design.md) for the evidence boundary.

## Install into a project

Clone this repository, then run its installer from your local checkout. The repository itself includes project-local `.codex/` and `.agents/` links, so it is also ready to open directly in Codex after a restart.

```bash
git clone "https://github.com/OWNER/reasflow-survey.git" reasflow-survey
cd reasflow-survey
bash install.sh /path/to/project
```

The installer adds `.codex/config.toml`, `.codex/agents/survey.toml`, and `.agents/skills/reasflow-survey/`. It refuses to replace existing targets unless `--force` is given. If the destination already has a Codex config, review it before using `--force`, which replaces that file. Restart Codex in the target project so it loads the new config and skill. Choose the model in your Codex invocation or user config; this project does not override provider credentials or model settings. The installer currently targets Bash environments.

Example requests inside an installed project:

```text
Write a full survey of decentralized optimization through July 2026. Compare assumptions, convergence criteria, and communication costs. Deliver the default long-form paper with about 100 substantively cited papers, LaTeX, bibliography, and PDF.
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

The checker writes `build/publication_report.json`. With a TeX engine available, it also builds preview PDFs. `--check-only` runs offline structural, citation, and duplicate-identity checks without requiring a compiler. Its default distinct-citation floor is 90 for a full survey and zero for Related Works; `--min-citations N` overrides it for an explicitly different scope. The count cannot establish relevance or depth, so the agent must also inspect the argument and sources. For full surveys, the skill asks the author to plan useful figures and inspect their final rendering; the mechanical checker does not certify visual or scientific quality.
Use `--bib path/to/existing.bib` when integrating a Related Works section into a paper with an existing bibliography.

## Optional evidence tools

Native Web search and primary sources are the default. Use Semantic Scholar only for a specific unresolved identity, metadata, or citation-neighbor question when its service is available; use ReaScholar only when structured mathematical evidence is part of the task. Neither is loaded or queried automatically. A search result is a lead, not proof of a theorem, historical priority, or an absence claim.

This repository does not copy the original multi-agent paper pipeline, cached corpora, experimental runners, hidden evaluators, or provider credentials.

The [2026-09-30 smoke tests](docs/validation-smoke-20260930.md) deliberately requested a short 1,800–2,400-word Survey with an eight-citation floor. Their five-page result shows that the basic pipeline can deliver a PDF; it does not meet the current default full-survey contract. The [2026-10-07 long-survey validation](docs/validation-long-survey-20261007.md) reached the current length and citation targets, but its mathematical corrections and two figures were added after an independent review. Neither run proves that the current default reliably produces publication-quality figures without review. The raw workspaces are local development artifacts and are not included in the Git repository.

## Development

```bash
python3 -m unittest discover -s tests -v
```

The checker uses the Python standard library. Compilation uses a user-provided Tectonic binary or one on `PATH`; creating code-native figures may require additional plotting packages selected for the task. Release preparation and the upload handoff are recorded in [docs/release.md](docs/release.md).
