from pathlib import Path
from typing import Optional, Dict, Any
from fastmcp import Context

from src.utils.yaml_pipeline import YAMLPipeline


class DigestYAMLPipeline:
    """Thin facade over YAMLPipeline and existing file loading logic.

    This keeps signatures compatible with EnhancedWebplatformDigestTool methods
    so we can migrate incrementally without changing behavior.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.yaml_pipeline = YAMLPipeline()

    def load_from_yaml(self, path: Path) -> Dict[str, Any]:
        return self.yaml_pipeline.load_from_yaml(path)

    def process_release_notes(
        self,
        markdown_content: str,
        version: str,
        channel: str,
        save_yaml: bool,
        split_by_area: bool,
    ) -> Dict[str, Any]:
        return self.yaml_pipeline.process_release_notes(
            markdown_content=markdown_content,
            version=version,
            channel=channel,
            save_yaml=save_yaml,
            split_by_area=split_by_area,
        )

    async def load_release_notes(
        self,
        ctx: Context,
        version: str,
        channel: str,
        debug: bool,
        target_area: Optional[str] = None,
    ) -> Optional[str]:
        # Mirror current filesystem-based lookup used by the tool
        base_dir = self.base_path / 'upstream_docs' / 'release_notes' / 'WebPlatform'
        patterns = [
            f"Chrome {version} release note - WebPlatform.md",
            f"chrome-{version}-{channel}.md",
            f"chrome_{version}_{channel}.md",
        ]
        if channel == 'stable':
            patterns.insert(1, f"chrome-{version}.md")

        chrome_content = None
        for pattern in patterns:
            file_path = base_dir / pattern
            if file_path.exists():
                if debug:
                    print(f"Loading from file: {file_path}")
                chrome_content = file_path.read_text(encoding='utf-8')
                break

        if not chrome_content:
            if debug:
                print(f"No release notes found for Chrome {version} {channel}")
            return None

        if target_area in ('graphics-webgpu', 'webgpu'):
            webgpu_file = base_dir / f"webgpu-{version}.md"
            if webgpu_file.exists():
                if debug:
                    print(f"Merging WebGPU content from: {webgpu_file}")
                webgpu_content = webgpu_file.read_text(encoding='utf-8')
                return self._merge_webgpu_content(chrome_content, webgpu_content)
            elif debug:
                print(f"No WebGPU file found for version {version}")
        return chrome_content

    def _merge_webgpu_content(self, chrome_content: str, webgpu_content: str) -> str:
        if '## WebGPU' in chrome_content:
            lines = chrome_content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if line.startswith('## WebGPU'):
                    skip = True
                    new_lines.append('## WebGPU')
                    new_lines.append('')
                    webgpu_lines = webgpu_content.split('\n')
                    in_content = False
                    for w in webgpu_lines:
                        if in_content or (w and not w.startswith('#')):
                            in_content = True
                            new_lines.append(w)
                    continue
                elif skip and line.startswith('##'):
                    skip = False
                if not skip:
                    new_lines.append(line)
            return '\n'.join(new_lines)
        return chrome_content + '\n\n## WebGPU\n\n' + webgpu_content

