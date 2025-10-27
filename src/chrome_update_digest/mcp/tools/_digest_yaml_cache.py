from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from fastmcp import Context

from chrome_update_digest.mcp.tools._digest_yaml_pipeline import DigestYAMLPipeline
from chrome_update_digest.utils.yaml_pipeline import YAMLPipeline

LOGGER = logging.getLogger(__name__)


class DigestYAMLCache:
    """Facade responsible for loading, caching, and aggregating digest YAML data."""

    def __init__(self, base_path: Path, cache_dir: Path, yaml_pipeline: YAMLPipeline):
        self.base_path = base_path
        self.cache_dir = cache_dir
        self.yaml_pipeline = yaml_pipeline
        self.yaml_facade = DigestYAMLPipeline(base_path)
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._auto_regeneration_enabled: bool = True  # Enable auto-regeneration by default

    @property
    def cache_hits(self) -> int:
        return self._cache_hits

    @property
    def cache_misses(self) -> int:
        return self._cache_misses

    async def get_yaml_data(
        self,
        ctx: Context,
        version: str,
        channel: str,
        use_cache: bool,
        split_by_area: bool,
        target_area: Optional[str],
        debug: bool,
    ) -> Optional[Dict[str, Any]]:
        """Load YAML data for the requested scope, generating it when cache misses occur."""
        normalized_area: Optional[str] = None
        if target_area and target_area != "all":
            normalized_area = 'graphics-webgpu' if target_area in ['webgpu', 'graphics-webgpu'] else target_area

        # Check if processed files exist and auto-regenerate if needed
        if self._auto_regeneration_enabled and split_by_area and use_cache:
            missing_files = await self._check_and_regenerate_if_missing(
                version, channel, normalized_area, debug
            )
            if missing_files and debug:
                LOGGER.info(
                    f"Auto-regenerated missing processed files for Chrome {version} ({channel})"
                )

        if normalized_area is None:
            if use_cache:
                aggregated = await self._aggregate_area_files(version, channel, debug)
                if aggregated:
                    return aggregated

            release_notes = await self._load_release_notes(
                ctx,
                version,
                channel,
                debug,
                None if target_area in (None, "all") else target_area,
            )
            if not release_notes:
                return None

            if debug:
                print("Processing release notes through YAML pipeline...")
                if split_by_area:
                    print("Splitting features by area into separate YAML files")

            yaml_data = self.yaml_pipeline.process_release_notes(
                markdown_content=release_notes,
                version=version,
                channel=channel,
                save_yaml=True,
                split_by_area=split_by_area,
            )

            if split_by_area and use_cache:
                for area in yaml_data.get('areas', []):
                    area_yaml_path = self._area_yaml_path(area, version, channel)
                    if area_yaml_path.exists():
                        self._cache_misses += 1
                        self._memory_cache[str(area_yaml_path)] = self.yaml_pipeline.load_from_yaml(area_yaml_path)

            if debug:
                stats = yaml_data.get('statistics', {})
                print(f"Extracted {stats.get('total_features', 0)} features with {stats.get('total_links', 0)} links")

            return yaml_data

        yaml_path = self._area_yaml_path(normalized_area, version, channel)
        cache_key = str(yaml_path)

        if use_cache:
            cached = self._memory_cache.get(cache_key)
            if cached is not None:
                self._cache_hits += 1
                if debug:
                    print(f"YAML cache hit: {cache_key} (hits={self._cache_hits})")
                return cached

        if use_cache and yaml_path.exists():
            if debug:
                print(f"Using cached YAML file: {yaml_path}")
            loaded = self.yaml_pipeline.load_from_yaml(yaml_path)
            self._memory_cache[cache_key] = loaded
            self._cache_misses += 1
            return loaded

        release_notes = await self._load_release_notes(ctx, version, channel, debug, normalized_area)
        if not release_notes:
            return None

        if debug:
            print("Processing release notes through YAML pipeline...")
            if split_by_area:
                print("Splitting features by area into separate YAML files")

        yaml_data = self.yaml_pipeline.process_release_notes(
            markdown_content=release_notes,
            version=version,
            channel=channel,
            save_yaml=True,
            split_by_area=split_by_area,
        )

        if yaml_path.exists():
            cached_area = self.yaml_pipeline.load_from_yaml(yaml_path)
            self._memory_cache[cache_key] = cached_area
            self._cache_misses += 1
            if debug:
                print(f"YAML cached in memory: {yaml_path}")
            return cached_area

        if debug:
            stats = yaml_data.get('statistics', {})
            print(f"Extracted {stats.get('total_features', 0)} features with {stats.get('total_links', 0)} links")

        area_yaml = await self.load_area_yaml(ctx, version, channel, normalized_area, yaml_data, debug)
        if area_yaml is not None:
            self._memory_cache[cache_key] = area_yaml
        return area_yaml

    async def load_area_yaml(
        self,
        ctx: Context,
        version: str,
        channel: str,
        area: str,
        full_yaml: Optional[Dict[str, Any]],
        debug: bool,
    ) -> Optional[Dict[str, Any]]:
        """Load or derive YAML for a specific area."""
        area_yaml_path = self._area_yaml_path(area, version, channel)
        if area_yaml_path.exists():
            if debug:
                print(f"Loading cached area YAML: {area_yaml_path}")
            return self.yaml_pipeline.load_from_yaml(area_yaml_path)

        aggregated_yaml = full_yaml or {}
        area_features = []
        for feature in aggregated_yaml.get('features', []):
            tags = feature.get('primary_tags', [])
            tag_names = []
            for tag in tags:
                if isinstance(tag, dict):
                    tag_names.append(tag.get('name', ''))
                else:
                    tag_names.append(str(tag))

            if area in tag_names:
                area_features.append(feature)
            elif area == 'graphics-webgpu' and 'webgpu' in tag_names:
                area_features.append(feature)
            elif area == 'security-privacy' and ('security' in tag_names or 'privacy' in tag_names):
                area_features.append(feature)
            elif area == 'pwa-service-worker' and ('pwa' in tag_names or 'service-worker' in tag_names or 'serviceworker' in tag_names):
                area_features.append(feature)
            elif area == 'navigation-loading' and ('loading' in tag_names or 'navigation' in tag_names):
                area_features.append(feature)
            elif area == 'origin-trials' and 'trials' in tag_names:
                area_features.append(feature)

        if not area_features and area == 'others':
            for feature in aggregated_yaml.get('features', []):
                if not feature.get('primary_tags', []):
                    area_features.append(feature)

        if not area_features:
            return None

        return {
            'version': aggregated_yaml.get('version'),
            'channel': aggregated_yaml.get('channel'),
            'area': area,
            'features': area_features,
            'statistics': {
                'total_features': len(area_features),
                'total_links': sum(len(f.get('links', [])) for f in area_features),
            },
        }

    async def _aggregate_area_files(
        self,
        version: str,
        channel: str,
        debug: bool,
    ) -> Optional[Dict[str, Any]]:
        aggregated_features = []
        all_areas = []
        total_stats = {'total_features': 0, 'total_links': 0, 'primary_tags': {}, 'cross_cutting': {}}

        areas_dir = self.cache_dir / 'areas'
        if not areas_dir.exists():
            if debug:
                print(f"Areas directory not found: {areas_dir}")
            return None

        for area_dir in areas_dir.iterdir():
            if not area_dir.is_dir():
                continue

            area_name = area_dir.name
            yaml_path = area_dir / f"chrome-{version}-{channel}.yml"

            if yaml_path.exists():
                try:
                    area_data = self.yaml_pipeline.load_from_yaml(yaml_path)
                except Exception as exc:
                    if debug:
                        print(f"Failed to load {yaml_path}: {exc}")
                    continue

                if area_data and 'features' in area_data:
                    aggregated_features.extend(area_data['features'])
                    all_areas.append(area_name)

                    area_stats = area_data.get('statistics', {})
                    total_stats['total_features'] += area_stats.get('total_features', 0)
                    total_stats['total_links'] += area_stats.get('total_links', 0)

                    for tag, count in area_stats.get('primary_tags', {}).items():
                        total_stats['primary_tags'][tag] = total_stats['primary_tags'].get(tag, 0) + count

                    for concern, count in area_stats.get('cross_cutting', {}).items():
                        total_stats['cross_cutting'][concern] = total_stats['cross_cutting'].get(concern, 0) + count

                    if debug:
                        print(f"Aggregated {len(area_data['features'])} features from {area_name}")

        if not aggregated_features:
            if debug:
                print(f"No area files found for Chrome {version} {channel}")
            return None

        return {
            'version': version,
            'channel': channel,
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'aggregated',
            'statistics': total_stats,
            'features': aggregated_features,
            'areas': all_areas,
        }

    async def _load_release_notes(
        self,
        ctx: Context,
        version: str,
        channel: str,
        debug: bool,
        target_area: Optional[str] = None,
    ) -> Optional[str]:
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

    def _area_yaml_path(self, area: str, version: str, channel: str) -> Path:
        return self.cache_dir / 'areas' / area / f"chrome-{version}-{channel}.yml"

    async def _check_and_regenerate_if_missing(
        self,
        version: str,
        channel: str,
        target_area: Optional[str],
        debug: bool,
    ) -> bool:
        """
        Check if processed files are missing and auto-regenerate them.

        Args:
            version: Chrome version number
            channel: Release channel
            target_area: Specific area to check (None for all areas)
            debug: Enable debug logging

        Returns:
            True if files were regenerated, False otherwise
        """
        from chrome_update_digest.mcp.tools.clean_data_pipeline_tool import (
            CleanDataPipelineTool,
        )

        # Determine which areas to check
        areas_to_check = []
        if target_area:
            areas_to_check = [target_area]
        else:
            # Check all expected areas
            from chrome_update_digest.processors.clean_data_pipeline import (
                CleanDataPipeline,
            )

            pipeline = CleanDataPipeline()
            areas_to_check = list(
                pipeline.focus_areas_config.get("focus_areas", {}).keys()
            )

        # Check for missing files
        missing_areas = []
        for area in areas_to_check:
            yaml_path = self._area_yaml_path(area, version, channel)
            markdown_path = (
                self.base_path
                / "upstream_docs"
                / "processed_releasenotes"
                / "processed_forwebplatform"
                / "areas"
                / area
                / f"chrome-{version}-{channel}.md"
            )

            # If either markdown or YAML is missing, we need to regenerate
            if not yaml_path.exists() or not markdown_path.exists():
                missing_areas.append(area)

        # If no files are missing, return early
        if not missing_areas:
            return False

        if debug:
            LOGGER.info(
                f"Detected missing processed files for Chrome {version} ({channel}) "
                f"in areas: {', '.join(missing_areas)}"
            )
            LOGGER.info("Auto-regenerating processed files...")

        # Run the clean data pipeline
        try:
            pipeline_tool = CleanDataPipelineTool(self.base_path)
            result = await pipeline_tool.run_pipeline(
                version=version,
                channel=channel,
                with_yaml=True,
                debug=debug,
            )

            if result.get("success"):
                if debug:
                    LOGGER.info(
                        f"Successfully regenerated processed files for Chrome {version} ({channel})"
                    )
                return True
            else:
                LOGGER.warning(
                    f"Failed to regenerate processed files: {result.get('message')}"
                )
                return False

        except Exception as e:
            LOGGER.exception(
                f"Error during auto-regeneration for Chrome {version} ({channel}): {e}"
            )
            return False
