#!/usr/bin/env python3
"""Check and optionally compile a full survey or embeddable related-work section.

The checker is deliberately mechanical. It does not judge whether a citation
supports a claim or whether a mathematical statement is correct.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


ENTRY_START = re.compile(r"(?m)^\s*@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")
CITATION = re.compile(
    r"\\(?:cite[A-Za-z]*|autocite|parencite|textcite)\*?"
    r"(?:\s*\[[^\]]*\]){0,2}\s*\{([^}]*)\}"
)
INPUT = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")


def normalized_text(value: str) -> str:
    value = re.sub(r"\\[A-Za-z]+\*?(?:\[[^]]*\])?", " ", value)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.casefold()).split())


def normalize_doi(value: str) -> str:
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)", "", value.strip().casefold()).rstrip(". ")


def normalize_arxiv(value: str) -> str:
    value = value.strip().casefold()
    value = re.sub(r"^(?:https?://arxiv\.org/(?:abs|pdf)/|arxiv:)", "", value)
    return re.sub(r"v\d+(?:\.pdf)?$", "", value).removesuffix(".pdf")


def field_value(body: str, name: str) -> str:
    """Read a common BibTeX field without pretending to parse all BibTeX syntax."""
    pattern = re.compile(rf"(?i)\b{re.escape(name)}\s*=\s*(\{{|\")")
    match = pattern.search(body)
    if not match:
        return ""
    opening = match.group(1)
    start = match.end()
    if opening == '"':
        end = start
        while end < len(body):
            if body[end] == '"' and body[end - 1] != "\\":
                return body[start:end].strip()
            end += 1
        return body[start:].strip()
    depth = 1
    for end in range(start, len(body)):
        if body[end] == "{":
            depth += 1
        elif body[end] == "}":
            depth -= 1
            if depth == 0:
                return body[start:end].strip()
    return body[start:].strip()


def parse_bibliography(text: str) -> list[dict[str, str]]:
    starts = list(ENTRY_START.finditer(text))
    entries: list[dict[str, str]] = []
    for index, match in enumerate(starts):
        body_end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        body = text[match.end() : body_end]
        record = {"type": match.group(1).lower(), "key": match.group(2).strip()}
        for name in ("title", "author", "year", "doi", "eprint", "archiveprefix", "url"):
            record[name] = field_value(body, name)
        entries.append(record)
    return entries


def identity_duplicates(entries: list[dict[str, str]]) -> list[dict[str, object]]:
    by_identity: dict[str, set[str]] = {}
    for entry in entries:
        identities = []
        doi = normalize_doi(entry["doi"])
        if doi:
            identities.append("doi:" + doi)
        eprint = ""
        if entry["archiveprefix"].casefold() == "arxiv" or re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", entry["eprint"].strip()):
            eprint = normalize_arxiv(entry["eprint"])
        if not eprint:
            arxiv_url = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9.]+(?:v\d+)?)", entry["url"], re.I)
            eprint = normalize_arxiv(arxiv_url.group(1)) if arxiv_url else ""
        if eprint:
            identities.append("arxiv:" + eprint)
        title = normalized_text(entry["title"])
        author = normalized_text(entry["author"])
        if title and author:
            identities.append("title-author:" + title + "|" + author)
        for identity in identities:
            by_identity.setdefault(identity, set()).add(entry["key"])
    return [
        {"identity": identity, "keys": sorted(keys)}
        for identity, keys in sorted(by_identity.items())
        if len(keys) > 1
    ]


def read_tex_tree(path: Path, root: Path, seen: set[Path] | None = None) -> str:
    path = path.resolve()
    root = root.resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"TeX input is missing or outside workspace: {path}")
    seen = set() if seen is None else seen
    if path in seen:
        return ""
    seen.add(path)
    text = without_tex_comments(path.read_text(encoding="utf-8"))

    def expand(match: re.Match[str]) -> str:
        relative = Path(match.group(1).strip())
        if not relative.suffix:
            relative = relative.with_suffix(".tex")
        return read_tex_tree(path.parent / relative, root, seen)

    return INPUT.sub(expand, text)


def without_tex_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        for index, char in enumerate(line):
            if char == "%":
                preceding_slashes = len(line[:index]) - len(line[:index].rstrip("\\"))
                if preceding_slashes % 2 == 0:
                    line = line[:index]
                    break
        lines.append(line)
    return "\n".join(lines)


def cited_keys(tex: str) -> set[str]:
    return {
        key.strip()
        for match in CITATION.finditer(without_tex_comments(tex))
        for key in match.group(1).split(",")
        if key.strip()
    }


def inspect_manuscript(kind: str, root: Path, bib_keys: set[str], min_citations: int) -> dict[str, object]:
    source = root / ("survey/survey.tex" if kind == "survey" else "related_works/related_works.tex")
    errors: list[str] = []
    if not source.is_file():
        return {"kind": kind, "source": str(source), "ok": False, "errors": ["missing manuscript"]}
    raw = source.read_text(encoding="utf-8")
    active_raw = without_tex_comments(raw)
    try:
        expanded = read_tex_tree(source, root)
    except ValueError as exc:
        expanded = raw
        errors.append(str(exc))
    citations = cited_keys(expanded)
    missing = sorted(citations - bib_keys)
    if missing:
        errors.append("undefined citation keys: " + ", ".join(missing))
    if len(citations) < min_citations:
        errors.append(f"{len(citations)} distinct citations, below requested floor {min_citations}")
    if kind == "survey":
        if "\\documentclass" not in active_raw:
            errors.append("full survey must be a standalone LaTeX document")
        if "\\begin{document}" not in active_raw or "\\end{document}" not in active_raw:
            errors.append("full survey has incomplete document boundaries")
    elif "\\documentclass" in active_raw and (
        "\\begin{document}" not in active_raw or "\\end{document}" not in active_raw
    ):
        errors.append("standalone Related Works has incomplete document boundaries")
    if not expanded.strip():
        errors.append("empty manuscript")
    return {
        "kind": kind,
        "source": str(source),
        "standalone": "\\documentclass" in active_raw,
        "citation_count": len(citations),
        "citation_keys": sorted(citations),
        "errors": errors,
        "ok": not errors,
    }


def find_tectonic(requested: str) -> str | None:
    candidate = requested or os.getenv("TECTONIC_BIN", "") or "tectonic"
    if Path(candidate).is_file():
        return str(Path(candidate).resolve())
    return shutil.which(candidate)


def run_tectonic(tectonic: str, source: Path, outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    command = [tectonic, "-X", "compile", str(source.resolve()), "--outdir", str(outdir.resolve()), "--keep-logs"]
    result = subprocess.run(command, cwd=source.parent, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    log = outdir / (source.stem + ".build.log")
    log.write_text(result.stdout, encoding="utf-8")
    pdf = outdir / (source.stem + ".pdf")
    valid_pdf = False
    if pdf.is_file() and pdf.stat().st_size > 8:
        with pdf.open("rb") as handle:
            valid_pdf = handle.read(4) == b"%PDF"
    return {
        "ok": result.returncode == 0 and valid_pdf,
        "returncode": result.returncode,
        "pdf": str(pdf) if valid_pdf else None,
        "log": str(log),
        "warnings": len(re.findall(r"Overfull \\[hv]box", result.stdout)),
    }


def compile_manuscript(kind: str, root: Path, tectonic: str, bib_path: Path) -> dict[str, object]:
    source_dir = root / ("survey" if kind == "survey" else "related_works")
    source = source_dir / ("survey.tex" if kind == "survey" else "related_works.tex")
    outdir = root / "build" / kind
    raw = source.read_text(encoding="utf-8")
    if kind == "related" and "\\documentclass" not in raw:
        wrapper = source_dir / "__reasflow_preview.tex"
        preview_bib = source_dir / "__reasflow_preview.bib"
        if wrapper.exists() or preview_bib.exists():
            raise FileExistsError("preview temporary path already exists")
        wrapper.write_text(
            "\\documentclass[11pt]{article}\n"
            "\\usepackage{natbib}\n"
            "\\begin{document}\n"
            "\\input{related_works.tex}\n"
            "\\bibliographystyle{plainnat}\n"
            "\\bibliography{__reasflow_preview}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        shutil.copyfile(bib_path, preview_bib)
        try:
            result = run_tectonic(tectonic, wrapper, outdir)
        finally:
            wrapper.unlink(missing_ok=True)
            preview_bib.unlink(missing_ok=True)
    else:
        result = run_tectonic(tectonic, source, outdir)
    if result["ok"]:
        shutil.copyfile(result["pdf"], source_dir / ("survey.pdf" if kind == "survey" else "related_works.pdf"))
    return result


def build_report(
    root: Path,
    mode: str,
    check_only: bool,
    tectonic_requested: str,
    min_citations: int,
    bibliography: Path = Path("references.bib"),
) -> dict[str, object]:
    root = root.resolve()
    bib_path = (root / bibliography).resolve()
    if not bib_path.is_file():
        return {"ok": False, "errors": [f"missing bibliography: {bib_path}"], "manuscripts": {}, "compilation": {}}
    entries = parse_bibliography(bib_path.read_text(encoding="utf-8"))
    keys = [entry["key"] for entry in entries]
    repeated_keys = sorted(key for key, count in Counter(keys).items() if count > 1)
    duplicates = identity_duplicates(entries)
    errors = []
    if repeated_keys:
        errors.append("duplicate BibTeX keys: " + ", ".join(repeated_keys))
    if duplicates:
        errors.append("multiple BibTeX entries resolve to the same paper identity")
    if not entries:
        errors.append("bibliography has no parsed entries")
    selected = ["survey", "related"] if mode == "both" else [mode]
    manuscripts = {kind: inspect_manuscript(kind, root, set(keys), min_citations) for kind in selected}
    valid = not errors and all(item["ok"] for item in manuscripts.values())
    compilation: dict[str, object] = {}
    if valid and not check_only:
        tectonic = find_tectonic(tectonic_requested)
        if not tectonic:
            errors.append("Tectonic not found; pass --tectonic or use --check-only")
        else:
            for kind in selected:
                compilation[kind] = compile_manuscript(kind, root, tectonic, bib_path)
                if not compilation[kind]["ok"]:
                    errors.append(f"{kind} compilation failed")
    return {
        "ok": valid and not errors,
        "mode": mode,
        "check_only": check_only,
        "bibliography": {"path": str(bib_path), "entry_count": len(entries), "duplicate_keys": repeated_keys, "canonical_duplicates": duplicates},
        "manuscripts": manuscripts,
        "compilation": compilation,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("survey", "related", "both"), required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--tectonic", default="")
    parser.add_argument("--min-citations", type=int, default=0)
    parser.add_argument("--bib", type=Path, default=Path("references.bib"), help="BibTeX file, relative to --workspace by default")
    args = parser.parse_args(argv)
    if args.min_citations < 0:
        parser.error("--min-citations must be nonnegative")
    try:
        report = build_report(args.workspace, args.mode, args.check_only, args.tectonic, args.min_citations, args.bib)
    except (OSError, ValueError) as exc:
        report = {"ok": False, "errors": [str(exc)], "manuscripts": {}, "compilation": {}}
    report_path = args.workspace / "build" / "publication_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
