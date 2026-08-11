from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jobhunt.cli import _resolve_resume_path


def test_resume_path_accepts_exact_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    resume = tmp_path / "resume.pdf"
    resume.write_bytes(b"%PDF")

    path, err = _resolve_resume_path("resume.pdf")

    assert path == Path("resume.pdf")
    assert err is None


def test_resume_path_adds_pdf_suffix_when_unambiguous(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.pdf").write_bytes(b"%PDF")

    path, err = _resolve_resume_path("resume")

    assert path == Path("resume.pdf")
    assert err is None


def test_resume_path_reports_ambiguous_extensionless_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resume.pdf").write_bytes(b"%PDF")
    (tmp_path / "resume.md").write_text("# Resume", encoding="utf-8")

    path, err = _resolve_resume_path("resume")

    assert path is None
    assert "ambiguous" in err
    assert "resume.pdf" in err
    assert "resume.md" in err
