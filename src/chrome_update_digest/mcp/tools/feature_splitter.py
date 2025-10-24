"""
Feature Splitter Tool
Splits markdown files by H3 headings into separate feature files
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class FeatureSplitterTool:
    """Tool for splitting markdown files by H3 headings into separate feature files"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        
    async def split_features(self, arguments: dict) -> str:
        """Split markdown files by H3 headings based on arguments"""
        input_path = arguments.get("input_path", "")
        output_base_dir = arguments.get("output_base_dir")
        dry_run = arguments.get("dry_run", False)
        feature_name = arguments.get("feature_name")
        version = arguments.get("version")
        
        # Resolve input path relative to base_path if it's not absolute
        if not os.path.isabs(input_path):
            input_path = os.path.join(self.base_path, input_path)
        
        # Check if input path exists
        if not os.path.exists(input_path):
            return json.dumps({
                "success": False,
                "error": f"Input path '{input_path}' does not exist"
            }, indent=2)
        
        try:
            if os.path.isdir(input_path):
                result = await self._process_folder(
                    input_path, output_base_dir, dry_run, feature_name, version
                )
            else:
                result = await self._process_single_file(
                    input_path, output_base_dir, dry_run
                )
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Error processing files: {str(e)}"
            }, indent=2)
    
    async def _process_folder(self, input_folder: str, output_base_dir: Optional[str], 
                            dry_run: bool, feature_name: Optional[str], 
                            version: Optional[int]) -> Dict[str, Any]:
        """Process all markdown files in a folder"""
        
        # Find all .md files in the folder and subfolders
        md_files = []
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    
                    # Apply filters
                    if feature_name and feature_name not in file:
                        continue
                    if version and f"-{version}-" not in file and f"chrome-{version}" not in file:
                        continue
                        
                    md_files.append(file_path)
        
        if not md_files:
            return {
                "success": True,
                "message": "No markdown files found matching the criteria",
                "summary": {
                    "files_processed": 0,
                    "features_extracted": 0,
                    "output_directories": []
                },
                "details": {},
                "dry_run": dry_run
            }
        
        results = {}
        total_features = 0
        output_dirs = []
        
        for md_file in md_files:
            try:
                if dry_run:
                    file_result = await self._preview_file(md_file, output_base_dir)
                else:
                    file_result = await self._split_file(md_file, output_base_dir)
                
                results[os.path.basename(md_file)] = file_result
                total_features += file_result.get("features_created", 0)
                
                if file_result.get("output_dir"):
                    output_dirs.append(file_result["output_dir"])
                    
            except Exception as e:
                results[os.path.basename(md_file)] = {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": True,
            "message": f"Successfully processed {len(md_files)} files, {'would create' if dry_run else 'created'} {total_features} feature files",
            "summary": {
                "files_processed": len(md_files),
                "features_extracted": total_features,
                "output_directories": list(set(output_dirs))
            },
            "details": results,
            "dry_run": dry_run
        }
    
    async def _process_single_file(self, input_file: str, output_base_dir: Optional[str], 
                                 dry_run: bool) -> Dict[str, Any]:
        """Process a single markdown file"""
        
        try:
            if dry_run:
                file_result = await self._preview_file(input_file, output_base_dir)
            else:
                file_result = await self._split_file(input_file, output_base_dir)
            
            return {
                "success": True,
                "message": f"Successfully processed file, {'would create' if dry_run else 'created'} {file_result.get('features_created', 0)} feature files",
                "summary": {
                    "files_processed": 1,
                    "features_extracted": file_result.get("features_created", 0),
                    "output_directories": [file_result.get("output_dir", "")]
                },
                "details": {
                    os.path.basename(input_file): file_result
                },
                "dry_run": dry_run
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing file '{input_file}': {str(e)}"
            }
    
    async def _preview_file(self, input_file: str, output_base_dir: Optional[str]) -> Dict[str, Any]:
        """Preview what would be created from a file without actually creating files"""
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine output directory
        output_dir = self._get_output_directory(input_file, output_base_dir)
        
        # Find H3 sections
        sections = re.split(r'^### ', content, flags=re.MULTILINE)
        sections.pop(0)  # Remove content before first H3
        
        preview_files = []
        for i, section in enumerate(sections, 1):
            lines = section.split('\n', 1)
            if lines:
                heading = lines[0].strip()
                filename = self._create_filename(heading, i)
                preview_files.append(f"{filename}.md")
        
        return {
            "success": True,
            "features_created": len(preview_files),
            "output_dir": os.path.basename(output_dir),
            "files": preview_files,
            "preview": True
        }
    
    async def _split_file(self, input_file: str, output_base_dir: Optional[str]) -> Dict[str, Any]:
        """Actually split the file and create feature files"""
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine output directory
        output_dir = self._get_output_directory(input_file, output_base_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Split content by H3 headings
        sections = re.split(r'^### ', content, flags=re.MULTILINE)
        sections.pop(0)  # Remove content before first H3
        
        created_files = []
        
        for i, section in enumerate(sections, 1):
            lines = section.split('\n', 1)
            if len(lines) >= 2:
                heading = lines[0].strip()
                content_part = lines[1]
            elif len(lines) == 1:
                heading = lines[0].strip()
                content_part = ""
            else:
                continue
            
            # Create filename
            filename = self._create_filename(heading, i)
            output_file = os.path.join(output_dir, f"{filename}.md")
            
            # Prepare content for the new file
            file_content = f"# {heading.strip()}\n\n{content_part.strip()}\n"
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            created_files.append(f"{filename}.md")
        
        return {
            "success": True,
            "features_created": len(created_files),
            "output_dir": os.path.basename(output_dir),
            "files": created_files,
            "full_output_path": output_dir
        }
    
    def _get_output_directory(self, input_file: str, output_base_dir: Optional[str]) -> str:
        """Determine the output directory for split files"""
        
        input_path = Path(input_file)
        file_stem = input_path.stem
        
        # Parse filename to extract feature name and version
        # Expected format: chrome-{version}-{feature}-features.md
        version_match = re.search(r'chrome-(\d+)-(.+?)-features', file_stem)
        if version_match:
            version = version_match.group(1)
            feature_name = version_match.group(2)
            folder_name = f"{feature_name}-{version}"
        else:
            # Fallback if filename doesn't match expected pattern
            folder_name = f"{file_stem}_features"
        
        if output_base_dir:
            return os.path.join(output_base_dir, folder_name)
        else:
            # Place the feature folder at the same level as the input folder
            input_folder = input_path.parent
            return os.path.join(input_folder.parent, "features", folder_name)
    
    def _create_filename(self, heading: str, index: int) -> str:
        """Create a clean filename from heading"""
        
        # Clean up heading for filename
        filename = re.sub(r'[^\w\s-]', '', heading.strip())
        filename = re.sub(r'[-\s]+', '-', filename)
        filename = filename.strip('-').lower()
        
        # Ensure filename is not empty
        if not filename:
            filename = f"section-{index}"
        
        return filename


if __name__ == '__main__':
    import argparse
    import asyncio

    async def main():
        """Main function to handle command line arguments and execute the splitting."""
        parser = argparse.ArgumentParser(
            description="Split markdown files by H3 (###) headings into separate feature files."
        )
        parser.add_argument(
            "input_path",
            help="Path to a markdown file or folder containing markdown files"
        )
        parser.add_argument(
            "-o", "--output-dir",
            dest="output_base_dir",
            help="Output base directory for split files (optional)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating files"
        )
        parser.add_argument(
            "--feature",
            dest="feature_name",
            help="Feature name to process (e.g., 'profile')"
        )
        parser.add_argument(
            "--version",
            type=int,
            help="Chrome version to process (e.g., 137)"
        )
        
        args = parser.parse_args()
        
        # Convert args namespace to a dictionary, removing None values
        arguments = {k: v for k, v in vars(args).items() if v is not None}
        
        # The tool expects the base path to be the project root
        base_path = Path(__file__).resolve().parent.parent.parent
        
        splitter = FeatureSplitterTool(base_path)
        
        print(f"Running splitter with arguments: {arguments}")
        
        try:
            result_json = await splitter.split_features(arguments)
            result_dict = json.loads(result_json)
            
            print("\n--- Splitting Complete ---")
            print(f"Success: {result_dict.get('success')}")
            print(f"Message: {result_dict.get('message')}")
            if 'error' in result_dict:
                print(f"Error: {result_dict.get('error')}")
            
            print("\nSummary:")
            summary = result_dict.get('summary', {})
            for key, value in summary.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")

            print("\nDetails:")
            details = result_dict.get('details', {})
            for filename, file_details in details.items():
                if file_details.get('success'):
                    print(f"  - {filename}: OK, {file_details.get('features_created', 0)} features found.")
                else:
                    print(f"  - {filename}: FAILED, {file_details.get('error')}")

        except Exception as e:
            print(f"\n--- An unexpected error occurred ---")
            print(e)

    asyncio.run(main())
