"""
Merged Digest HTML Tool
Generates combined enterprise and web platform Chrome digest as HTML
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import time

# Import sys and add parent directory for absolute imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from convert_md2html import ChromeDigestConverter
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class MergedDigestHtmlTool:
    """Tool for generating merged Chrome digests as HTML"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.output_base_dir = base_path / "digest_html"
        
        # Initialize the HTML converter with proper template path
        self._init_html_converter()
    
    def _init_html_converter(self):
        """Initialize HTML converter with proper template path"""
        # Search for template directory in possible locations
        possible_template_paths = [
            self.base_path / "templates",
            self.base_path.parent / "templates",
            Path(__file__).parent.parent / "templates",
            Path(__file__).parent.parent.parent / "templates",
            Path.cwd() / "templates"
        ]
        
        template_path = None
        for path in possible_template_paths:
            if path.exists() and (path / "digest_combined.html").exists():
                template_path = path
                break
        
        if not template_path:
            raise RuntimeError(
                f"Cannot find templates directory with digest_combined.html. "
                f"Searched in: {[str(p) for p in possible_template_paths]}"
            )
        
        print(f"[DIR] Using template path: {template_path}")
        
        # Create HTML converter and override its template environment
        self.html_converter = ChromeDigestConverter()
        self.html_converter.template_env = Environment(
            loader=FileSystemLoader(str(template_path)),
            autoescape=True
        )
        
        # Verify template can be loaded
        try:
            self.html_converter.template_env.get_template('digest_combined.html')
            print("✅ Template digest_combined.html loaded successfully")
        except TemplateNotFound:
            raise RuntimeError(f"Template digest_combined.html not found in {template_path}")
    
    def _read_digest_file(self, digest_type: str, version: int, channel: str) -> str:
        """Read existing digest markdown file with high fault tolerance"""
        base_dir = self.base_path / "digest_markdown" / digest_type
        
        # Define possible file name patterns in priority order
        if digest_type == "enterprise":
            possible_patterns = [
                f"digest-chrome-{version}-enterprise-{channel}.md",  # with channel suffix
                f"digest-chrome-{version}-enterprise.md",           # without channel suffix
                f"chrome-{version}-enterprise-{channel}.md",        # alternative format 1
                f"chrome-{version}-enterprise.md",                  # alternative format 2
                f"{version}-enterprise-{channel}.md",               # alternative format 3
                f"{version}-enterprise.md"                          # alternative format 4
            ]
        else:  # webplatform
            possible_patterns = [
                f"digest-chrome-{version}-webplatform-{channel}.md", # with channel suffix
                f"digest-chrome-{version}-webplatform.md",          # without channel suffix
                f"chrome-{version}-webplatform-{channel}.md",       # alternative format 1
                f"chrome-{version}-webplatform.md",                 # alternative format 2
                f"{version}-webplatform-{channel}.md",              # alternative format 3
                f"{version}-webplatform.md"                         # alternative format 4
            ]
        
        # Try to find existing file
        found_file = None
        for pattern in possible_patterns:
            candidate_file = base_dir / pattern
            if candidate_file.exists():
                found_file = candidate_file
                break
        
        # If no patterns match, try fuzzy matching
        if found_file is None:
            if base_dir.exists():
                # Look for any file containing version number and type
                for file in base_dir.glob("*.md"):
                    filename = file.name.lower()
                    if (str(version) in filename and 
                        digest_type in filename and
                        ("digest" in filename or "chrome" in filename)):
                        found_file = file
                        break
        
        if found_file is None:
            # List all files in directory for debugging
            available_files = []
            if base_dir.exists():
                available_files = [f.name for f in base_dir.glob("*.md")]
            
            raise FileNotFoundError(
                f"No {digest_type} digest file found for Chrome {version} ({channel}). "
                f"Searched patterns: {possible_patterns[:2]}. "
                f"Available files in {base_dir}: {available_files}. "
                f"Please ensure the {digest_type} digest has been generated first."
            )
        
        try:
            with open(found_file, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            
            if not raw_content.strip():
                raise ValueError(f"Digest file is empty: {found_file}")
            
            # Extract markdown content from structured format if needed
            content = self._extract_markdown_content(raw_content)
            
            if not content.strip():
                raise ValueError(f"No valid markdown content extracted from: {found_file}")
            
            # Log the actual file path used
            print(f"✅ Found {digest_type} digest: {found_file.name}")
            return content
            
        except Exception as e:
            raise Exception(f"Failed to read digest file {found_file}: {str(e)}")
    
    def _extract_markdown_content(self, raw_content: str) -> str:
        """Extract markdown content from structured format"""
        # Check if content is wrapped in structured format
        if raw_content.startswith("type='text' text='"):
            # Extract content between text=' and ' annotations=
            import re
            # Updated pattern to handle the actual format: ' annotations=None meta=None
            pattern = r"text='(.*?)' annotations=.*?meta=.*?$"
            match = re.search(pattern, raw_content, re.DOTALL)
            if match:
                extracted = match.group(1)
                # Unescape the content
                extracted = extracted.replace('\\n', '\n')
                extracted = extracted.replace("\\'", "'")
                extracted = extracted.replace('\\"', '"')
                return extracted
            else:
                # Fallback: try to extract everything after text=' and before ' annotations=
                if "text='" in raw_content:
                    start_idx = raw_content.find("text='") + 6
                    # Look for either pattern
                    end_patterns = ["' annotations=None meta=None", "' annotations="]
                    end_idx = -1
                    for pattern in end_patterns:
                        end_idx = raw_content.rfind(pattern)
                        if end_idx > start_idx:
                            break
                    
                    if end_idx > start_idx:
                        extracted = raw_content[start_idx:end_idx]
                        # Unescape the content
                        extracted = extracted.replace('\\n', '\n')
                        extracted = extracted.replace("\\'", "'")
                        extracted = extracted.replace('\\"', '"')
                        return extracted
        
        # If not in structured format, return as is
        return raw_content
    
    async def generate_html(self, arguments: dict) -> str:
        """Generate merged digest HTML based on arguments"""
        version = arguments.get("version")
        channel = arguments.get("channel", "stable")
        force_regenerate = arguments.get("force_regenerate", False)
        output_dir = arguments.get("output_dir", "digest_html")
        
        if not version:
            return json.dumps({
                "success": False,
                "error": "Version number is required",
                "message": "Please provide a Chrome version number (e.g., 138)"
            }, indent=2)
        
        # Set up output directory
        output_path = Path(output_dir) if output_dir != "digest_html" else self.output_base_dir
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename
        output_filename = f"chrome-{version}-merged-digest-{channel}.html"
        output_file = output_path / output_filename
        
        # Check if file exists and should not be regenerated
        if output_file.exists() and not force_regenerate:
            # Validate file is not empty and has reasonable size
            file_size = output_file.stat().st_size
            if file_size < 1000:  # HTML file should be at least 1KB
                print(f"⚠️ Existing file is too small ({file_size} bytes), forcing regeneration")
                force_regenerate = True
            else:
                file_size_str = self._format_file_size(file_size)
                file_mtime = datetime.fromtimestamp(output_file.stat().st_mtime)
                
                return json.dumps({
                    "success": True,
                    "file_path": str(output_file.absolute()),
                    "file_size": file_size_str,
                    "generated": False,
                    "timestamp": file_mtime.isoformat(),
                    "sections": ["enterprise", "webplatform"],
                    "preview_url": f"file://{output_file.absolute()}",
                    "message": f"HTML file already exists. Use force_regenerate=true to recreate it."
                }, indent=2)
        
        try:
            # Read existing digest files
            print(f"📖 Reading digest files for Chrome {version} {channel}...")
            enterprise_content = self._read_digest_file("enterprise", version, channel)
            webplatform_content = self._read_digest_file("webplatform", version, channel)
            
            # Validate content
            if not enterprise_content or len(enterprise_content.strip()) < 100:
                raise ValueError("Enterprise digest content is empty or too short")
            if not webplatform_content or len(webplatform_content.strip()) < 100:
                raise ValueError("WebPlatform digest content is empty or too short")
            
            print(f"  ✓ Enterprise content: {len(enterprise_content)} chars")
            print(f"  ✓ WebPlatform content: {len(webplatform_content)} chars")
            
            # Process and combine the content
            print("🔄 Processing digest content...")
            processed_data = self._process_digest_content(
                enterprise_content, 
                webplatform_content, 
                version, 
                channel
            )
            
            # Validate processed data
            ent_html = processed_data.get('enterprise', {}).get('html_content', '')
            web_html = processed_data.get('webplatform', {}).get('html_content', '')
            
            if not ent_html or len(ent_html) < 50:
                raise ValueError(f"Processed enterprise HTML is empty or too short ({len(ent_html)} chars)")
            if not web_html or len(web_html) < 50:
                raise ValueError(f"Processed webplatform HTML is empty or too short ({len(web_html)} chars)")
            
            print(f"  ✓ Processed Enterprise HTML: {len(ent_html)} chars")
            print(f"  ✓ Processed WebPlatform HTML: {len(web_html)} chars")
            
            # Generate HTML using template
            print("🎨 Generating HTML from template...")
            html_content = self._generate_combined_html(processed_data)
            
            # Validate final HTML
            if not html_content or len(html_content) < 1000:
                raise ValueError(f"Generated HTML is too short ({len(html_content)} chars)")
            
            print(f"  ✓ Generated HTML: {len(html_content)} chars")
            
            # Write to temporary file first
            temp_file = output_file.with_suffix('.tmp')
            print(f"✍️ Writing to temporary file...")
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                bytes_written = f.write(html_content)
                f.flush()
                os.fsync(f.fileno())
            
            print(f"  ✓ Wrote {bytes_written} chars")
            
            # Wait for file system sync
            time.sleep(0.1)
            
            # Verify temporary file
            if not temp_file.exists():
                raise IOError("Temporary file does not exist after writing")
            
            temp_size = temp_file.stat().st_size
            if temp_size < 1000:
                raise IOError(f"Temporary file is too small ({temp_size} bytes)")
            
            # Read back and verify content
            with open(temp_file, 'r', encoding='utf-8') as f:
                verify_content = f.read()
                if len(verify_content) != len(html_content):
                    raise IOError(f"Content verification failed: wrote {len(html_content)} chars but read {len(verify_content)} chars")
            
            # Move to final location
            temp_file.replace(output_file)
            print(f"✅ Moved to final location: {output_file}")
            
            # Final verification
            if not output_file.exists():
                raise IOError("Final file does not exist after move")
            
            final_size = output_file.stat().st_size
            if final_size < 1000:
                raise IOError(f"Final file is too small ({final_size} bytes)")
            
            # Calculate file size
            file_size = self._format_file_size(final_size)
            
            return json.dumps({
                "success": True,
                "file_path": str(output_file.absolute()),
                "file_size": file_size,
                "generated": True,
                "timestamp": datetime.now().isoformat(),
                "sections": ["enterprise", "webplatform"],
                "preview_url": f"file://{output_file.absolute()}",
                "message": f"Successfully generated merged digest HTML for Chrome {version} {channel}"
            }, indent=2)
            
        except Exception as e:
            # Clean up any temporary or empty files
            for file_to_clean in [output_file, output_file.with_suffix('.tmp')]:
                if file_to_clean.exists():
                    try:
                        file_to_clean.unlink()
                        print(f"🧹 Cleaned up: {file_to_clean.name}")
                    except:
                        pass
            
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return json.dumps({
                "success": False,
                "error": str(e),
                "message": f"Failed to generate merged digest HTML for Chrome {version}",
                "details": traceback.format_exc()
            }, indent=2)
    
    def _process_digest_content(self, enterprise_content: str, webplatform_content: str, 
                               version: int, channel: str) -> dict:
        """Process and structure the digest content for HTML generation"""
        
        # Parse enterprise content into chapters
        enterprise_chapters = self.html_converter.parse_chapters(enterprise_content)
        
        # Parse webplatform content into chapters  
        webplatform_chapters = self.html_converter.parse_chapters(webplatform_content)
        
        # Process each chapter into HTML
        enterprise_html_chapters = {}
        for chapter_title, chapter_content in enterprise_chapters.items():
            enterprise_html_chapters[chapter_title] = self.html_converter.process_content(chapter_content)
        
        webplatform_html_chapters = {}
        for chapter_title, chapter_content in webplatform_chapters.items():
            webplatform_html_chapters[chapter_title] = self.html_converter.process_content(chapter_content)
        
        return {
            "version": version,
            "channel": channel,
            "enterprise": {
                "chapters": enterprise_html_chapters,
                "html_content": self._render_sections(enterprise_html_chapters)
            },
            "webplatform": {
                "chapters": webplatform_html_chapters,
                "html_content": self._render_sections(webplatform_html_chapters)
            }
        }
    
    def _render_sections(self, chapters: Dict[str, str]) -> str:
        """Render chapters into HTML sections"""
        html_parts = []
        for chapter_title, chapter_content in chapters.items():
            html_parts.append(f'<div class="section">')
            html_parts.append(f'<h2>{chapter_title}</h2>')
            html_parts.append(chapter_content)
            html_parts.append('</div>')
        return '\n'.join(html_parts)
    
    def _generate_combined_html(self, processed_data: dict) -> str:
        """Generate combined HTML using the digest_combined.html template"""
        try:
            # Verify template environment is properly initialized
            if not hasattr(self.html_converter, 'template_env'):
                raise RuntimeError("Template environment not initialized")
            
            # Load template with explicit error handling
            try:
                template = self.html_converter.template_env.get_template('digest_combined.html')
            except TemplateNotFound as e:
                print(f"❌ Template not found: {e}")
                raise RuntimeError(f"Cannot load template digest_combined.html: {e}")
            
            # Prepare version data
            enterprise_version_data = [{
                'version': processed_data['version'],
                'channel': processed_data['channel'],
                'digest_type': 'enterprise',
                'html_content': processed_data['enterprise']['html_content']
            }]
            
            webplatform_version_data = [{
                'version': processed_data['version'],
                'channel': processed_data['channel'],
                'digest_type': 'webplatform',
                'html_content': processed_data['webplatform']['html_content']
            }]
            
            # Render template
            html_content = template.render(
                webplatform_versions=webplatform_version_data,
                enterprise_versions=enterprise_version_data,
                webplatform_total=1,
                enterprise_total=1,
                generated_at=datetime.now()
            )
            
            # Validate rendered content
            if not html_content or len(html_content.strip()) < 100:
                raise ValueError(f"Template rendered to empty or very short content ({len(html_content)} chars)")
            
            return html_content
            
        except Exception as e:
            print(f"❌ Template rendering failed: {str(e)}")
            print("🔄 Using fallback HTML generation")
            return self._generate_fallback_html(processed_data)
    
    def _generate_fallback_html(self, processed_data: dict) -> str:
        """Generate a simple fallback HTML if template rendering fails"""
        version = processed_data['version']
        channel = processed_data['channel']
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome {version} {channel.title()} - Merged Digest</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .tabs {{ display: flex; margin-bottom: 20px; }}
        .tab {{ padding: 10px 20px; cursor: pointer; background: #f0f0f0; margin-right: 10px; }}
        .tab.active {{ background: #007acc; color: white; }}
        .content {{ display: none; }}
        .content.active {{ display: block; }}
        .section {{ margin-bottom: 30px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #007acc; border-bottom: 2px solid #007acc; padding-bottom: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Chrome {version} {channel.title()} - Merged Digest</h1>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('enterprise')">🏢 Enterprise</div>
            <div class="tab" onclick="switchTab('webplatform')">🌐 Web Platform</div>
        </div>
        
        <div id="enterprise" class="content active">
            {processed_data['enterprise']['html_content']}
        </div>
        
        <div id="webplatform" class="content">
            {processed_data['webplatform']['html_content']}
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {{
            // Hide all content
            document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            
            // Show selected content
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>"""
        return html
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f}MB"
