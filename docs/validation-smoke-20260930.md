# Small end-to-end delivery tests (2026-09-30)

These are two preserved, single-attempt development smokes for the new survey-only agent. The frozen protocol and prompts remain in local development workspaces under `workspaces/smoke_20260930/`; those workspaces are intentionally excluded from this Git repository. Both used GPT-5.6-Sol at high reasoning effort, the installed `reasflow-survey` skill, and native Web search. Neither used Semantic Scholar or ReaScholar. They test two output modes on the same mathematical area; they are not a matched comparison with `reasflow-dev` or a test of a production-length survey.

| Mode | Workspace | Result | Host postflight |
| --- | --- | --- | --- |
| Full Survey: extragradient-family monotone VIs | `workspaces/smoke_20260930/full_survey/` | 5-page PDF; 2,051 extracted body words; 15 cited primary-paper records; mechanical check and compilation passed. The process reached the 900-second limit after files were written, while reconnecting after a network/TLS interruption, so the agent did not finish a final response. | `build/host_postflight.json` |
| Related Works: hypothetical adaptive projected extragradient paper | `workspaces/smoke_20260930/related_works/` | Embeddable TeX section, 4-page standalone preview including references; 848 extracted body words; 12 cited primary-paper records; mechanical check and compilation passed; process completed in 870 seconds. | `build/host_postflight.json` |

The body-word figures come from `pdftotext` before the References heading, so they are approximate and include any section headings. Both are within the frozen requested ranges. The Related Works section carefully states what the hypothetical paper would need to establish, without inventing a theorem or outcome. In a targeted reading of the Survey, the method families are compared by assumptions, operator/prox cost, output, and convergence criterion; the source audit records URLs and claim locators. The Survey PDF's first and last pages and the Related Works preview's first page were visually checked. These checks do not certify every mathematical statement or citation; the preserved source notes and PDFs support manual review.

In the preserved local development workspaces, manual inspection starts with:

- `full_survey/survey/survey.pdf`, `full_survey/survey/survey.tex`, `full_survey/references.bib`, and `full_survey/research/source_audit.md`.
- `related_works/related_works/related_works.tex`, `related_works/related_works/related_works.pdf`, `related_works/references.bib`, and `related_works/research_notes.md` (plus `research/source_pdfs/`).
- Each workspace's `build/agent_publication_report.json` (original agent check), `build/publication_report.json` (independent check-only rerun), `build/host_postflight.json`, and `logs/EXECUTION.json`, `logs/events.jsonl`, `logs/stderr.log`. The Survey lacks `logs/final.txt` because its process timed out after the deliverables existed.

The complete workspaces are deliberately ignored by Git but remain on disk. No quality-based retries were made. The repository's seven unit tests passed after these runs.
