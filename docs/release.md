# Release preparation and upload handoff

This is a standalone Git repository with one Codex custom agent (`agents/survey.toml`) and one mounted skill (`skills/reasflow-survey/`). The project-local `.codex/` and `.agents/` paths are relative links to those canonical files. The installer copies the same files into an existing project; it does not install any of the original `reasflow-dev` pipeline.

## Distribution boundary

- Tracked: agent, skill, publication checker, Bash installer, tests, license, README, design and validation summaries, and CI workflow.
- Local only: `workspaces/`, generated paper/PDF assets, source PDFs, logs, build outputs, model credentials, and provider configuration. They are not part of the Git archive.
- The package is usable without the local research workspaces. The validation summaries describe observations, not a guarantee of autonomous mathematical or visual correctness.
- Runtime: Codex with a sufficiently capable model and Web/source access. Python 3.10+ runs the standard-library publication checker and tests. Tectonic is needed only to compile PDFs. Plotting dependencies are task-specific and are not bundled.

## Checks before upload

1. Run `python3 -m unittest discover -s tests -v`, `bash -n install.sh`, and `git diff --check`.
2. Run `git archive` into a temporary directory and test installation from that export into a separate empty target. Check that the agent and skill resolve without links to the original `reasflow-dev` or local workspaces.
3. Review `git ls-files` for credentials, generated artifacts, and machine-specific paths. The local workspaces remain available for manual review but are ignored by Git.
4. Inspect the public README, license, installer behavior, and `docs/validation-*.md` claim boundaries. An end-to-end fresh run with the final figure guidance has **not** yet been measured; do not claim stable figure quality or superiority over `reasflow-dev`.
5. Once the user creates an empty remote repository, add its URL as `origin` and push `main`. Do not initialize the remote with a separate README/license, which would create an avoidable unrelated history. Follow the repository owner's visibility and release-tag choice.

The remote creation and push are intentionally pending the user's new repository. A GitHub Release is separate from pushing the repository: it can later attach a tag, release notes, and optional assets if wanted. No tag is required for the initial source upload.
