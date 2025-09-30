"""
Tests for the ChromeDigestConverter utility.
"""

import pytest
from pathlib import Path

from src.convert_md2html import ChromeDigestConverter


@pytest.fixture
def template_dir(tmp_path: Path) -> Path:
    """Create a temporary template directory for the converter."""
    templates = tmp_path / "templates"
    templates.mkdir()

    digest_template = """
<html>
  <body>
  {% for version in versions %}
    <section id="version-{{ version.version }}" data-channel="{{ version.channel }}">
      {{ version.html_content | safe }}
    </section>
  {% endfor %}
  </body>
</html>
"""
    combined_template = """<html><body>{{ webplatform_total }} {{ enterprise_total }}</body></html>"""

    (templates / "digest.html").write_text(digest_template, encoding="utf-8")
    (templates / "digest_combined.html").write_text(combined_template, encoding="utf-8")
    return templates


@pytest.fixture
def converter(template_dir: Path) -> ChromeDigestConverter:
    """Provide a converter instance pointing at the temporary templates."""
    return ChromeDigestConverter(template_path=template_dir)


def test_parse_chapters_splits_by_heading(converter: ChromeDigestConverter) -> None:
    """parse_chapters should group content under H2 headings."""
    content = """
## Chapter One
Line one.

## Chapter Two
Line two.

## Chapter Three
Line three.
"""
    chapters = converter.parse_chapters(content)

    assert list(chapters.keys()) == ["Chapter One", "Chapter Two", "Chapter Three"]
    assert "Line one." in chapters["Chapter One"]
    assert "Line three." in chapters["Chapter Three"]


def test_process_content_renders_markdown(converter: ChromeDigestConverter) -> None:
    """process_content should convert markdown to HTML and reset the parser."""
    html = converter.process_content("## Heading\n\n* item")
    assert "<h2" in html and "Heading</h2>" in html
    assert "id=\"heading\"" in html
    assert "<li>item</li>" in html

    # Running again should not accumulate previous state
    html_again = converter.process_content("Plain text")
    assert "Plain text" in html_again


def test_generate_digest_html_writes_file(converter: ChromeDigestConverter, tmp_path: Path) -> None:
    """generate_digest_html should render the template to the requested path."""
    output_file = tmp_path / "digest.html"
    versions_data = [
        {
            "version": "138",
            "channel": "stable",
            "html_content": "<div>" + "Feature description " * 6 + "</div>",
        }
    ]

    result = converter.generate_digest_html(versions_data, output_file)

    assert result is True
    assert output_file.exists()

    generated = output_file.read_text(encoding="utf-8")
    assert "version-138" in generated
    assert "Feature description" in generated
