#!/usr/bin/env python3
"""
Test enhanced resource system with FastMCP
Tests metadata, tags, and dynamic resource listing
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from chrome_update_digest.mcp.resources.processed_releasenotes import ProcessedReleaseNotesResource


def test_resource_metadata():
    """Test that resources have proper metadata with tags"""
    print("Testing resource metadata...")
    
    base_path = Path(__file__).parent.parent
    resource_handler = ProcessedReleaseNotesResource(base_path)
    
    # List all resources
    resources = resource_handler.list_resources()
    
    if not resources:
        print("No resources found - this might be expected if no processed release notes exist")
        return
    
    # Check first few resources
    for i, resource in enumerate(resources[:5]):
        print(f"\nResource {i+1}:")
        print(f"  URI: {resource['uri']}")
        print(f"  Name: {resource['name']}")
        print(f"  Description: {resource['description']}")
        
        # Check metadata
        if "_meta" in resource and "_fastmcp" in resource["_meta"]:
            meta = resource["_meta"]["_fastmcp"]
            print(f"  Tags: {', '.join(meta.get('tags', []))}")
            print(f"  Category: {meta.get('category', 'N/A')}")
            print(f"  Version: {meta.get('version', 'N/A')}")
            print(f"  Size: {meta.get('size', 0)} bytes")
        else:
            print("  ERROR: Missing metadata!")
    
    print(f"\nTotal resources found: {len(resources)}")


def test_tag_filtering():
    """Test filtering resources by tags"""
    print("\nTesting tag-based filtering...")
    
    base_path = Path(__file__).parent.parent
    resource_handler = ProcessedReleaseNotesResource(base_path)
    
    resources = resource_handler.list_resources()
    
    # Count resources by tag
    tag_counts = {}
    for resource in resources:
        if "_meta" in resource and "_fastmcp" in resource["_meta"]:
            tags = resource["_meta"]["_fastmcp"].get("tags", [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print("\nResource counts by tag:")
    for tag, count in sorted(tag_counts.items()):
        print(f"  {tag}: {count} resources")
    
    # Example: Filter resources with 'enterprise' tag
    enterprise_resources = [
        r for r in resources
        if "_meta" in r and "_fastmcp" in r["_meta"]
        and "enterprise" in r["_meta"]["_fastmcp"].get("tags", [])
    ]
    
    print(f"\nResources with 'enterprise' tag: {len(enterprise_resources)}")
    if enterprise_resources:
        print("First enterprise resource:", enterprise_resources[0]["name"])


def test_resource_reading():
    """Test reading a specific resource"""
    print("\nTesting resource reading...")
    
    base_path = Path(__file__).parent.parent
    resource_handler = ProcessedReleaseNotesResource(base_path)
    
    resources = resource_handler.list_resources()
    
    if resources:
        # Try to read the first resource
        first_resource = resources[0]
        uri = first_resource["uri"]
        
        print(f"Reading resource: {uri}")
        try:
            content = resource_handler.read_resource(uri)
            print(f"Successfully read {len(content)} characters")
            print(f"First 100 chars: {content[:100]}...")
        except Exception as e:
            print(f"ERROR reading resource: {e}")


def main():
    """Run all tests"""
    print("=== Enhanced Resource System Tests ===\n")
    
    test_resource_metadata()
    test_tag_filtering()
    test_resource_reading()
    
    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    main()