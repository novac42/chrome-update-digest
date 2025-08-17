"""
Convert Markdown to HTML for Chrome Digest
"""

import markdown
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from typing import Dict, List


class ChromeDigestConverter:
    """Chrome Digest converter with robust template handling"""
    
    def __init__(self, template_path=None):
        """Initialize converter with automatic template path discovery"""
        # Set up markdown processor
        self.md = markdown.Markdown(
            extensions=['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                },
                'toc': {
                    'permalink': False
                }
            }
        )
        
        # Set up template environment with automatic path discovery
        if template_path is None:
            template_path = self._find_template_path()
        
        self.template_env = Environment(
            loader=FileSystemLoader(str(template_path)),
            autoescape=True
        )
        
        # Verify key templates exist
        self._verify_templates()
    
    def _find_template_path(self) -> Path:
        """Find template directory automatically"""
        possible_paths = [
            Path(__file__).parent / 'templates',
            Path(__file__).parent.parent / 'templates',
            Path.cwd() / 'templates',
            Path(__file__).parent.parent.parent / 'templates'
        ]
        
        for path in possible_paths:
            if path.exists() and (path / 'digest.html').exists():
                print(f"[DIR] Found template path: {path}")
                return path
        
        # If not found, use the first path and let FileSystemLoader handle the error
        print(f"⚠️ Template path not found, using default: {possible_paths[0]}")
        return possible_paths[0]
    
    def _verify_templates(self):
        """Verify that essential templates can be loaded"""
        templates_to_check = ['digest.html', 'digest_combined.html']
        
        for template_name in templates_to_check:
            try:
                self.template_env.get_template(template_name)
                print(f"✅ Template {template_name} loaded successfully")
            except TemplateNotFound:
                print(f"⚠️ Warning: Template {template_name} not found")
    
    def parse_chapters(self, content: str) -> Dict[str, str]:
        """Parse markdown content into chapters based on H2 headers"""
        lines = content.split('\n')
        chapters = {}
        current_chapter = None
        current_content = []
        
        for line in lines:
            if line.startswith('## '):
                # Save previous chapter
                if current_chapter and current_content:
                    chapters[current_chapter] = '\n'.join(current_content)
                
                # Start new chapter
                current_chapter = line[3:].strip()
                current_content = []
            else:
                if current_chapter:
                    current_content.append(line)
        
        # Save last chapter
        if current_chapter and current_content:
            chapters[current_chapter] = '\n'.join(current_content)
        
        return chapters
    
    def process_content(self, content: str) -> str:
        """Convert markdown content to HTML"""
        if not content or not content.strip():
            return ""
        
        # Convert markdown to HTML
        html_content = self.md.convert(content)
        
        # Reset markdown processor for next use
        self.md.reset()
        
        return html_content
    
    def generate_digest_html(self, versions_data: List[Dict], output_file: Path):
        """Generate digest HTML file from versions data"""
        try:
            template = self.template_env.get_template('digest.html')
            
            html_content = template.render(
                versions=versions_data,
                total_versions=len(versions_data)
            )
            
            # Validate generated content
            if not html_content or len(html_content.strip()) < 100:
                raise ValueError(f"Generated HTML is too short: {len(html_content)} chars")
            
            # Write to file
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to generate HTML: {str(e)}")
            return False