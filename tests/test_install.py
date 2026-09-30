from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def test_install_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            first = subprocess.run(["bash", str(ROOT / "install.sh"), str(target)], text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((target / ".codex/config.toml").is_file())
            self.assertTrue((target / ".codex/agents/survey.toml").is_file())
            self.assertTrue((target / ".agents/skills/reasflow-survey/SKILL.md").is_file())
            second = subprocess.run(["bash", str(ROOT / "install.sh"), str(target)], text=True, capture_output=True)
            self.assertEqual(second.returncode, 1)
            self.assertIn("Nothing was installed", second.stderr)
            forced = subprocess.run(["bash", str(ROOT / "install.sh"), str(target), "--force"], text=True, capture_output=True)
            self.assertEqual(forced.returncode, 0, forced.stderr)


if __name__ == "__main__":
    unittest.main()
