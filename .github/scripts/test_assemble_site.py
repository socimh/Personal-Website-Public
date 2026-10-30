"""Check that published Teaching links retain both hosted workshop editions."""
from pathlib import Path
import tempfile
import unittest
from assemble_site import assemble


class HostedWorkshops(unittest.TestCase):
    def fixture(self, root):
        public, private = root / "public", root / "private"
        public.mkdir()
        for name in ("assets", "pic", "site_libs", "zh"):
            (public / name).mkdir()
        for name in ("CNAME", "search.json", ".nojekyll"):
            (public / name).write_text("", encoding="utf-8")
        (public / "index.html").write_text("<p>Home</p>", encoding="utf-8")
        for name in ("cc-guide", "slides", "stata-to-r"):
            (private / "docs" / name).mkdir(parents=True)
            (private / "docs" / name / "index.html").write_text("<p>Material</p>", encoding="utf-8")
        return public, private

    def test_workshop_editions_are_included(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            public, private = self.fixture(root)
            for lang, other in (("en", "zh"), ("zh", "en")):
                edition = private / "docs/workshops" / lang
                edition.mkdir(parents=True)
                (edition / "index.html").write_text(f'<a href="../{other}/index.html">Language</a>', encoding="utf-8")
            output = root / "site"
            assemble(public, private, output)
            self.assertTrue((output / "workshops/en/index.html").is_file())
            self.assertTrue((output / "workshops/zh/index.html").is_file())

    def test_missing_workshops_fails_before_publication(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            public, private = self.fixture(root)
            with self.assertRaises(ValueError):
                assemble(public, private, root / "site")


if __name__ == "__main__":
    unittest.main()
