"""Assemble the published site without adding its hosted materials to Git."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        self.paths.extend(value for name, value in attrs
                          if name in ("href", "src") and value)


def copy(source, destination):
    if not source.exists() or source.is_symlink():
        raise ValueError(f"Missing or unsupported site input: {source.name}")
    if source.is_dir():
        if any(path.is_symlink() for path in source.rglob("*")):
            raise ValueError(f"Symlinks are not supported in {source.name}")
        shutil.copytree(source, destination)
    else:
        shutil.copyfile(source, destination)


def assemble(public_root, private_root, output):
    public_root = public_root.resolve()
    private_root = private_root.resolve()
    output = output.resolve()
    if output == public_root or output == private_root or output.exists():
        raise ValueError("Deployment output must be a new, separate directory")
    output.mkdir(parents=True)

    # Only website files enter the deployment; Git, workflows, and source files stay out.
    public_names = ["assets", "pic", "site_libs", "zh", "CNAME", "search.json", ".nojekyll"]
    public_names.extend(path.name for path in public_root.glob("*.html"))
    for name in public_names:
        copy(public_root / name, output / name)
    for name in ("cc-guide", "slides", "stata-to-r"):
        copy(private_root / "docs" / name, output / name)

    missing = []
    pages = list(output.rglob("*.html"))
    references = 0
    for page in pages:
        links = Links()
        links.feed(page.read_text(encoding="utf-8"))
        for value in links.paths:
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (output / unquote(url.path).lstrip("/")) if url.path.startswith("/") else page.parent / unquote(url.path)
            target = target.resolve()
            if not target.is_relative_to(output):
                raise ValueError("A site reference points outside the deployment")
            if target.is_dir():
                target = target / "index.html"
            references += 1
            if not target.is_file():
                missing.append(f"{page.relative_to(output)}: {value}")
    if missing:
        raise ValueError("Broken site references:\n" + "\n".join(sorted(set(missing))))
    print(f"Validated {len(pages)} HTML pages and {references} local references.")
    print("Deployment assembled successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-root", type=Path, default=Path("."))
    parser.add_argument("--private-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assemble(args.public_root, args.private_root, args.output)
