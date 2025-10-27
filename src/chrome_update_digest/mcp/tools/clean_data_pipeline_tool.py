#!/usr/bin/env python3
"""
MCP tool for triggering the clean data pipeline to process release notes.

This tool wraps CleanDataPipeline.process_version_with_yaml and allows
automatic materialization of processed markdown and YAML files when needed
by the digest pipeline.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from chrome_update_digest.processors.clean_data_pipeline import CleanDataPipeline
from chrome_update_digest.utils.telemetry import DigestTelemetry

LOGGER = logging.getLogger(__name__)


class CleanDataPipelineTool:
    """Tool for running the clean data pipeline via MCP."""

    def __init__(self, base_path: Path):
        """
        Initialize the clean data pipeline tool.

        Args:
            base_path: Workspace root directory
        """
        self.base_path = base_path
        self.telemetry = DigestTelemetry(base_path)
        self.pipeline = CleanDataPipeline()

    async def run_pipeline(
        self,
        version: str,
        channel: str = "stable",
        with_yaml: bool = True,
        markdown_output_dir: Optional[Path] = None,
        yaml_output_dir: Optional[Path] = None,
        debug: bool = False,
    ) -> Dict[str, Any]:
        """
        Run the clean data pipeline for a specific Chrome version.

        Args:
            version: Chrome version number (e.g., "138")
            channel: Release channel ("stable" or "beta")
            with_yaml: Generate YAML output in addition to markdown (default: True)
            markdown_output_dir: Override for markdown output directory
            yaml_output_dir: Override for YAML output directory
            debug: Enable debug logging

        Returns:
            Dictionary with processing results including:
            - success: bool
            - version: str
            - channel: str
            - markdown_files: dict mapping area names to file paths
            - yaml_files: dict mapping area names to file paths (if with_yaml=True)
            - duration_seconds: float
            - timestamp: str (ISO format)
            - message: str
        """
        start_time = datetime.now()
        
        if debug:
            LOGGER.setLevel(logging.DEBUG)
            print(f"\n{'='*60}")
            print(f"Running clean data pipeline for Chrome {version} ({channel})")
            print(f"with_yaml={with_yaml}")
            print(f"{'='*60}\n")

        try:
            # Set default directories if not provided
            if not markdown_output_dir:
                markdown_output_dir = (
                    self.base_path
                    / "upstream_docs"
                    / "processed_releasenotes"
                    / "processed_forwebplatform"
                    / "areas"
                )
            
            if not yaml_output_dir:
                yaml_output_dir = (
                    self.base_path
                    / "upstream_docs"
                    / "processed_releasenotes"
                    / "processed_forwebplatform"
                    / "processed_yaml"
                )

            # Run the pipeline
            if with_yaml:
                result = self.pipeline.process_version_with_yaml(
                    version=version,
                    markdown_output_dir=markdown_output_dir,
                    yaml_output_dir=yaml_output_dir,
                    channel=channel,
                )
                markdown_files = result.get("markdown", {})
                yaml_files = result.get("yaml", {})
            else:
                markdown_files = self.pipeline.process_version(
                    version=version,
                    output_dir=markdown_output_dir,
                    channel=channel,
                )
                yaml_files = {}

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Record telemetry
            self.telemetry.record_event(
                event_type="clean_data_pipeline_run",
                data={
                    "version": version,
                    "channel": channel,
                    "with_yaml": with_yaml,
                    "markdown_files_count": len(markdown_files),
                    "yaml_files_count": len(yaml_files),
                    "duration_seconds": duration,
                    "success": True,
                    "triggered_by": "mcp_tool",
                },
            )

            # Convert Path objects to strings for JSON serialization
            markdown_files_str = {
                area: str(path) for area, path in markdown_files.items()
            }
            yaml_files_str = {area: str(path) for area, path in yaml_files.items()}

            result_data = {
                "success": True,
                "version": version,
                "channel": channel,
                "markdown_files": markdown_files_str,
                "markdown_files_count": len(markdown_files),
                "duration_seconds": duration,
                "timestamp": end_time.isoformat(),
                "message": (
                    f"Successfully processed Chrome {version} ({channel}). "
                    f"Generated {len(markdown_files)} markdown files"
                ),
            }

            if with_yaml:
                result_data["yaml_files"] = yaml_files_str
                result_data["yaml_files_count"] = len(yaml_files)
                result_data["message"] += f" and {len(yaml_files)} YAML files"

            if debug:
                print(f"\n{'='*60}")
                print(f"✅ Pipeline completed in {duration:.2f}s")
                print(f"{'='*60}\n")

            return result_data

        except FileNotFoundError as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Record failure telemetry
            self.telemetry.record_event(
                event_type="clean_data_pipeline_run",
                data={
                    "version": version,
                    "channel": channel,
                    "with_yaml": with_yaml,
                    "duration_seconds": duration,
                    "success": False,
                    "error": str(e),
                    "triggered_by": "mcp_tool",
                },
            )
            
            error_msg = f"Release notes not found for Chrome {version} ({channel}): {e}"
            LOGGER.error(error_msg)
            
            return {
                "success": False,
                "version": version,
                "channel": channel,
                "error": str(e),
                "error_type": "FileNotFoundError",
                "duration_seconds": duration,
                "timestamp": end_time.isoformat(),
                "message": error_msg,
            }

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Record failure telemetry
            self.telemetry.record_event(
                event_type="clean_data_pipeline_run",
                data={
                    "version": version,
                    "channel": channel,
                    "with_yaml": with_yaml,
                    "duration_seconds": duration,
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "triggered_by": "mcp_tool",
                },
            )
            
            error_msg = f"Error processing Chrome {version} ({channel}): {e}"
            LOGGER.exception(error_msg)
            
            return {
                "success": False,
                "version": version,
                "channel": channel,
                "error": str(e),
                "error_type": type(e).__name__,
                "duration_seconds": duration,
                "timestamp": end_time.isoformat(),
                "message": error_msg,
            }

    def check_processed_files_exist(
        self, version: str, channel: str, split_by_area: bool = True
    ) -> Dict[str, bool]:
        """
        Check if processed files already exist for a version/channel.

        Args:
            version: Chrome version number
            channel: Release channel
            split_by_area: Check for split area files (vs single file)

        Returns:
            Dictionary with:
            - markdown_exists: bool
            - yaml_exists: bool
            - missing_areas: list of area names with missing files
        """
        if not split_by_area:
            # Check for single aggregated file
            single_file = (
                self.base_path
                / "upstream_docs"
                / "processed_releasenotes"
                / "processed_forwebplatform"
                / f"{version}-webplatform-with-webgpu.md"
            )
            return {
                "markdown_exists": single_file.exists(),
                "yaml_exists": False,  # Single file mode doesn't use YAML
                "missing_areas": [],
            }

        # Check for split area files
        areas_dir = (
            self.base_path
            / "upstream_docs"
            / "processed_releasenotes"
            / "processed_forwebplatform"
            / "areas"
        )

        if not areas_dir.exists():
            return {
                "markdown_exists": False,
                "yaml_exists": False,
                "missing_areas": ["all"],
            }

        # Expected areas from focus_areas.yaml
        from chrome_update_digest.processors.clean_data_pipeline import CleanDataPipeline
        pipeline = CleanDataPipeline()
        expected_areas = list(pipeline.focus_areas_config.get("focus_areas", {}).keys())

        missing_markdown = []
        missing_yaml = []

        for area in expected_areas:
            area_dir = areas_dir / area
            markdown_file = area_dir / f"chrome-{version}-{channel}.md"
            yaml_file = (
                self.base_path
                / "upstream_docs"
                / "processed_releasenotes"
                / "processed_forwebplatform"
                / "processed_yaml"
                / "areas"
                / area
                / f"chrome-{version}-{channel}.yml"
            )

            if not markdown_file.exists():
                missing_markdown.append(area)
            if not yaml_file.exists():
                missing_yaml.append(area)

        return {
            "markdown_exists": len(missing_markdown) == 0,
            "yaml_exists": len(missing_yaml) == 0,
            "missing_areas": list(set(missing_markdown + missing_yaml)),
            "missing_markdown_areas": missing_markdown,
            "missing_yaml_areas": missing_yaml,
        }
