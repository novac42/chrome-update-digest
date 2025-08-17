#!/usr/bin/env python3
"""
Unit tests for convert.py
"""

import unittest
from pathlib import Path
import sys
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from convert_md2html import ChromeDigestConverter


class TestChromeDigestConverter(unittest.TestCase):
    """Test cases for ChromeDigestConverter"""
    
    def setUp(self):
        """Set up test environment"""
        self.converter = ChromeDigestConverter()
        # Create temporary directories for testing
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = os.path.join(self.temp_dir, 'templates')
        os.makedirs(self.templates_dir)
        
        # Create a simple template
        template_content = """
<html>
<body>
{% for version in versions %}
<div class="version-content" id="version-{{ version.version }}">
{{ version.html_content }}
</div>
{% endfor %}
</body>
</html>
"""
        with open(os.path.join(self.templates_dir, 'digest.html'), 'w') as f:
            f.write(template_content)
        
        # Mock template environment to use test directory
        self.converter.template_env.loader.searchpath = [self.templates_dir]
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_extract_version_info(self):
        """Test version extraction from filename"""
        # Valid filename
        version, channel = self.converter.extract_version_info("digest-chrome-138-stable.md")
        self.assertEqual(version, "138")
        self.assertEqual(channel, "stable")
        
        # Another valid filename
        version, channel = self.converter.extract_version_info("digest-chrome-137-beta.md")
        self.assertEqual(version, "137")
        self.assertEqual(channel, "beta")
        
        # Invalid filename
        version, channel = self.converter.extract_version_info("invalid-filename.md")
        self.assertIsNone(version)
        self.assertIsNone(channel)
    
    def test_parse_chapters(self):
        """Test chapter parsing"""
        content = """
## Chapter One

Content for chapter one.
More content.

## Chapter Two

Content for chapter two.

### Subsection

Subsection content.

## Chapter Three

Final chapter content.
"""
        chapters = self.converter.parse_chapters(content)
        
        self.assertEqual(len(chapters), 3)
        self.assertIn("Chapter One", chapters)
        self.assertIn("Chapter Two", chapters)
        self.assertIn("Chapter Three", chapters)
        
        self.assertIn("Content for chapter one", chapters["Chapter One"])
        self.assertIn("More content", chapters["Chapter One"])
        self.assertIn("Subsection content", chapters["Chapter Two"])
    
    def test_wrap_h3_in_cards(self):
        """Test h3 wrapping functionality"""
        html = """
<h3>Feature Title</h3>
<p>Feature description paragraph.</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<h3>Another Feature</h3>
<p>Another description.</p>
"""
        result = self.converter.wrap_h3_in_cards(html)
        
        self.assertIn('<div class="h3-card">', result)
        self.assertIn('<h3>Feature Title</h3>', result)
        self.assertIn('<p>Feature description paragraph.</p>', result)
        
        # Count h3-card divs
        card_count = result.count('<div class="h3-card">')
        self.assertEqual(card_count, 2)
    
    def test_process_links(self):
        """Test link processing"""
        html = """
<a href="https://w3c.github.io/spec">W3C Spec</a>
<a href="https://developer.mozilla.org/docs">MDN Docs</a>
<a href="#section">Internal Link</a>
<a href="https://example.com">External Link</a>
"""
        result = self.converter.process_links(html)
        
        # Check external links
        self.assertIn('target="_blank"', result)
        self.assertIn('rel="noopener noreferrer"', result)
        self.assertIn('class="external-link', result)
        
        # Check spec links
        self.assertIn('link-spec', result)
        
        # Check docs links
        self.assertIn('link-docs', result)
        
        # Internal links should not have target="_blank"
        self.assertEqual(result.count('href="#section"'), 1)
        self.assertNotIn('#section" target="_blank"', result)
    
    def test_process_content(self):
        """Test content processing pipeline"""
        markdown_content = """
### Test Feature

This is a [link to spec](https://w3c.github.io/test).

- Item 1
- Item 2
"""
        html = self.converter.process_content(markdown_content)
        
        # Check markdown conversion - h3 is wrapped in div
        self.assertIn('<h3', html)  # Changed to partial match since it may have attributes
        self.assertIn('<ul>', html)
        self.assertIn('<li>Item 1</li>', html)
        
        # Check h3 wrapping
        self.assertIn('h3-card', html)
        
        # Check link processing
        self.assertIn('link-spec', html)
        self.assertIn('target="_blank"', html)
    
    def test_render_version_sections(self):
        """Test version section rendering"""
        chapters = {
            "Chapter 1": "<p>Content 1</p>",
            "Chapter 2": "<p>Content 2</p>"
        }
        
        result = self.converter._render_version_sections(chapters)
        
        self.assertIn('<div class="section">', result)
        self.assertIn('<h2>Chapter 1</h2>', result)
        self.assertIn('<p>Content 1</p>', result)
        self.assertIn('<h2>Chapter 2</h2>', result)
        self.assertIn('<p>Content 2</p>', result)
    
    def test_get_markdown_versions(self):
        """Test markdown version detection"""
        # Create test markdown directory
        md_dir = os.path.join(self.temp_dir, 'digest_markdown')
        os.makedirs(md_dir)
        
        # Create test files
        test_files = [
            'digest-chrome-138-stable.md',
            'digest-chrome-137-stable.md',
            'digest-chrome-136-stable.md',
            'other-file.md'
        ]
        
        for filename in test_files:
            Path(os.path.join(md_dir, filename)).touch()
        
        versions = self.converter.get_markdown_versions(md_dir)
        
        self.assertEqual(len(versions), 3)
        self.assertEqual(versions, [138, 137, 136])  # Should be sorted in descending order
    
    def test_parse_existing_html_versions(self):
        """Test parsing versions from existing HTML"""
        html_content = """
<html>
<body>
<select id="version-select">
<option value="138">Chrome 138</option>
<option value="137">Chrome 137</option>
</select>
<div class="version-content" id="version-138"></div>
<div class="version-content" id="version-137"></div>
</body>
</html>
"""
        # Create test HTML file
        html_file = os.path.join(self.temp_dir, 'test.html')
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        versions = self.converter.parse_existing_html_versions(html_file)
        
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions, [138, 137])
    
    def test_convert_file_success(self):
        """Test successful file conversion"""
        # Create test markdown file
        md_content = """
## Features

### New Feature

This is a test feature.
"""
        md_file = os.path.join(self.temp_dir, 'digest-chrome-138-stable.md')
        with open(md_file, 'w') as f:
            f.write(md_content)
        
        # Create output directory
        output_dir = os.path.join(self.temp_dir, 'output')
        os.makedirs(output_dir)
        output_file = os.path.join(output_dir, 'test.html')
        
        # Convert file
        self.converter.convert_file(md_file, output_file)
        
        # Check output exists
        self.assertTrue(os.path.exists(output_file))
        
        # Check content
        with open(output_file, 'r') as f:
            html_content = f.read()
            self.assertIn('version-138', html_content)
            self.assertIn('New Feature', html_content)
    
    def test_convert_file_invalid_filename(self):
        """Test conversion with invalid filename"""
        # Create test file with invalid name
        md_file = os.path.join(self.temp_dir, 'invalid-name.md')
        Path(md_file).touch()
        
        output_file = os.path.join(self.temp_dir, 'output.html')
        
        # Should exit with error
        with self.assertRaises(SystemExit):
            self.converter.convert_file(md_file, output_file)
    
    def test_process_version_file(self):
        """Test processing a single version file"""
        # Create test markdown file
        md_content = """
## Test Chapter

### Test Feature

Feature content here.
"""
        md_file = os.path.join(self.temp_dir, 'digest-chrome-138-stable.md')
        with open(md_file, 'w') as f:
            f.write(md_content)
        
        result = self.converter.process_version_file(Path(md_file))
        
        self.assertIsNotNone(result)
        self.assertEqual(result['version'], '138')
        self.assertEqual(result['channel'], 'stable')
        self.assertIn('Test Chapter', result['html_content'])
        self.assertIn('Test Feature', result['html_content'])
    
    def test_convert_incremental_no_existing(self):
        """Test incremental conversion with no existing HTML"""
        # Create test markdown directory and files
        md_dir = os.path.join(self.temp_dir, 'digest_markdown')
        os.makedirs(md_dir)
        
        md_content = """
## Features

Content here.
"""
        
        for version in [137, 138]:
            md_file = os.path.join(md_dir, f'digest-chrome-{version}-stable.md')
            with open(md_file, 'w') as f:
                f.write(md_content)
        
        output_file = os.path.join(self.temp_dir, 'output.html')
        
        # Run incremental conversion
        self.converter.convert_incremental(md_dir, output_file)
        
        # Check output exists
        self.assertTrue(os.path.exists(output_file))
        
        # Check both versions are present
        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn('version-137', content)
            self.assertIn('version-138', content)
    
    @patch('convert.ChromeDigestConverter.parse_existing_html_versions')
    def test_convert_incremental_with_existing(self, mock_parse):
        """Test incremental conversion with existing versions"""
        # Mock existing versions
        mock_parse.return_value = [137]
        
        # Create test markdown directory and files
        md_dir = os.path.join(self.temp_dir, 'digest_markdown')
        os.makedirs(md_dir)
        
        md_content = """
## Features

Content here.
"""
        
        # Create files for versions 137 and 138
        for version in [137, 138]:
            md_file = os.path.join(md_dir, f'digest-chrome-{version}-stable.md')
            with open(md_file, 'w') as f:
                f.write(md_content)
        
        output_file = os.path.join(self.temp_dir, 'output.html')
        
        # Run incremental conversion
        self.converter.convert_incremental(md_dir, output_file)
        
        # Should process only version 138 (the new one)
        self.assertTrue(os.path.exists(output_file))


if __name__ == '__main__':
    unittest.main()