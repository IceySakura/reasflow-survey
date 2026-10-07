from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills/reasflow-survey/scripts/publication.py"


class PublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "survey").mkdir()
        (self.root / "related_works").mkdir()
        (self.root / "references.bib").write_text(
            "@article{sourceA,\n"
            "  title={A Result {With} Conditions},\n"
            "  author={Smith, Alice and Jones, Bob},\n"
            "  year={2022},\n"
            "  doi={10.1000/example.a}\n"
            "}\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_checker(self, mode: str, *extra: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--workspace", str(self.root), "--mode", mode, "--check-only", *extra],
            text=True,
            capture_output=True,
            check=False,
        )
        report = json.loads((self.root / "build/publication_report.json").read_text(encoding="utf-8"))
        return result, report

    def test_full_survey_and_related_fragment_are_independent(self) -> None:
        (self.root / "survey/survey.tex").write_text(
            r"\documentclass{article}\begin{document}Evidence \citep{sourceA}.\bibliographystyle{plainnat}\bibliography{../references}\end{document}",
            encoding="utf-8",
        )
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}The closest result is \citet{sourceA}.", encoding="utf-8"
        )
        result, report = self.run_checker("both", "--min-citations", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(report["ok"])
        self.assertEqual(report["manuscripts"]["survey"]["citation_count"], 1)
        self.assertEqual(report["manuscripts"]["related"]["citation_count"], 1)

    def test_missing_citation_is_rejected(self) -> None:
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}Wrong key \cite{missing}.", encoding="utf-8"
        )
        result, report = self.run_checker("related")
        self.assertEqual(result.returncode, 1)
        self.assertIn("undefined citation keys", report["manuscripts"]["related"]["errors"][0])

    def test_same_paper_under_two_keys_is_rejected(self) -> None:
        with (self.root / "references.bib").open("a", encoding="utf-8") as handle:
            handle.write(
                "@misc{preprintA,\n"
                "  title={A Result With Conditions},\n"
                "  author={Smith, Alice and Jones, Bob},\n"
                "  year={2021},\n"
                "  eprint={2201.12345}\n"
                "}\n"
            )
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}Result \cite{sourceA}.", encoding="utf-8"
        )
        result, report = self.run_checker("related")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(report["bibliography"]["canonical_duplicates"])

    def test_citation_floor_is_explicit_not_default(self) -> None:
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}Evidence \cite{sourceA}.", encoding="utf-8"
        )
        self.assertEqual(self.run_checker("related")[0].returncode, 0)
        self.assertEqual(self.run_checker("related", "--min-citations", "2")[0].returncode, 1)

    def test_full_survey_default_rejects_short_overview_but_allows_explicit_short_scope(self) -> None:
        (self.root / "survey/survey.tex").write_text(
            r"\documentclass{article}\begin{document}Evidence \cite{sourceA}.\bibliography{../references}\end{document}",
            encoding="utf-8",
        )
        result, report = self.run_checker("survey")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["manuscripts"]["survey"]["citation_floor"], 90)
        self.assertTrue(any("below requested floor 90" in error for error in report["manuscripts"]["survey"]["errors"]))

        result, report = self.run_checker("survey", "--min-citations", "1")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["manuscripts"]["survey"]["citation_floor"], 1)

    def test_combined_mode_keeps_related_works_floor_separate(self) -> None:
        (self.root / "survey/survey.tex").write_text(
            r"\documentclass{article}\begin{document}Evidence \cite{sourceA}.\bibliography{../references}\end{document}",
            encoding="utf-8",
        )
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}Evidence \cite{sourceA}.", encoding="utf-8"
        )
        result, report = self.run_checker("both")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["manuscripts"]["survey"]["citation_floor"], 90)
        self.assertFalse(report["manuscripts"]["survey"]["ok"])
        self.assertEqual(report["manuscripts"]["related"]["citation_floor"], 0)
        self.assertTrue(report["manuscripts"]["related"]["ok"])

    def test_inline_bib_fields_and_commented_citations(self) -> None:
        (self.root / "references.bib").write_text(
            "@article{sourceA, title={A Result {With} Conditions}, author={Smith, Alice and Jones, Bob}, year={2022}, doi={10.1000/example.a}}\n"
            "@article{sourceB, title={Another Paper}, author={Doe, Carol}, year={2023}, doi={10.1000/example.b}}\n",
            encoding="utf-8",
        )
        (self.root / "related_works/related_works.tex").write_text(
            "\\section{Related Work}One result \\cite{sourceA}.\n"
            "% \\cite{missing}\n"
            "\\nocite{sourceB}\n",
            encoding="utf-8",
        )
        result, report = self.run_checker("related")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["manuscripts"]["related"]["citation_count"], 1)

    def test_existing_bibliography_path(self) -> None:
        (self.root / "paper").mkdir()
        (self.root / "references.bib").rename(self.root / "paper/refs.bib")
        (self.root / "related_works/related_works.tex").write_text(
            r"\section{Related Work}One result \cite{sourceA}.", encoding="utf-8"
        )
        result, report = self.run_checker("related", "--bib", "paper/refs.bib")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["bibliography"]["path"].endswith("paper/refs.bib"))


if __name__ == "__main__":
    unittest.main()
