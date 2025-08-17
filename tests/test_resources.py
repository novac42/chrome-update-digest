#!/usr/bin/env python3
"""Test script for ProcessedReleaseNotesResource"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mcp_resources.processed_releasenotes import ProcessedReleaseNotesResource


async def test_resources():
    """Test the ProcessedReleaseNotesResource functionality"""
    
    base_path = Path(__file__).parent.parent
    resource_handler = ProcessedReleaseNotesResource(base_path)
    
    print("Testing ProcessedReleaseNotesResource...\n")
    
    # Test listing resources
    print("1. Listing all resources:")
    print("-" * 50)
    
    try:
        resources = await resource_handler.list_resources()
        print(f"Found {len(resources)} resources\n")
        
        # Show first 5 resources
        for i, resource in enumerate(resources[:5]):
            print(f"Resource {i+1}:")
            print(f"  URI: {resource['uri']}")
            print(f"  Name: {resource['name']}")
            print(f"  Description: {resource['description']}")
            print(f"  MIME Type: {resource['mimeType']}")
            print()
        
        if len(resources) > 5:
            print(f"... and {len(resources) - 5} more resources\n")
        
    except Exception as e:
        print(f"Error listing resources: {e}")
        return
    
    # Test reading a resource
    print("\n2. Testing resource reading:")
    print("-" * 50)
    
    if resources:
        # Try to read the first resource
        test_uri = resources[0]['uri']
        print(f"Reading resource: {test_uri}")
        
        try:
            content = await resource_handler.read_resource(test_uri)
            print(f"Content preview (first 200 chars):")
            print(content[:200] + "..." if len(content) > 200 else content)
        except Exception as e:
            print(f"Error reading resource: {e}")
    
    # Test metadata extraction
    print("\n\n3. Testing metadata extraction:")
    print("-" * 50)
    
    # Show metadata for different types of resources
    categories = {}
    for resource in resources:
        # Extract category from URI
        parts = resource['uri'].replace("upstream://processed_releasenotes/", "").split("/")
        if parts:
            category = parts[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(resource)
    
    for category, items in categories.items():
        print(f"\nCategory: {category}")
        print(f"  Count: {len(items)}")
        if items:
            print(f"  Example: {items[0]['description']}")
    
    print("\n\nTest completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_resources())