#!/usr/bin/env python3
"""
Test FastMCP resource system from client perspective
Requires the FastMCP server to be running on localhost:4242
"""

import asyncio
from fastmcp import AsyncClient


async def test_resource_listing():
    """Test listing resources and their metadata"""
    async with AsyncClient("ws://localhost:4242") as client:
        print("=== Testing Resource Listing ===")
        
        # List all resources
        resources = await client.list_resources()
        
        print(f"\nTotal resources: {len(resources)}")
        
        # Check static resources
        static_resources = [r for r in resources if r.uri.startswith("file://")]
        print(f"Static resources: {len(static_resources)}")
        for r in static_resources:
            print(f"  - {r.uri}: {r.description}")
        
        # Check dynamic resources
        dynamic_resources = [r for r in resources if r.uri.startswith("upstream://")]
        print(f"\nDynamic release note resources: {len(dynamic_resources)}")
        
        # Show first few dynamic resources with metadata
        print("\nFirst 5 dynamic resources with metadata:")
        for i, r in enumerate(dynamic_resources[:5]):
            print(f"\n{i+1}. {r.name}")
            print(f"   URI: {r.uri}")
            print(f"   Description: {r.description}")
            
            # Check for FastMCP metadata
            if hasattr(r, '_meta') and '_fastmcp' in r._meta:
                meta = r._meta['_fastmcp']
                print(f"   Tags: {', '.join(meta.get('tags', []))}")
                print(f"   Version: {meta.get('version', 'N/A')}")
                print(f"   Category: {meta.get('category', 'N/A')}")


async def test_tag_filtering():
    """Test filtering resources by tags"""
    async with AsyncClient("ws://localhost:4242") as client:
        print("\n=== Testing Tag-Based Filtering ===")
        
        resources = await client.list_resources()
        
        # Filter by enterprise tag
        enterprise_resources = [
            r for r in resources 
            if hasattr(r, '_meta') and '_fastmcp' in r._meta 
            and 'enterprise' in r._meta['_fastmcp'].get('tags', [])
        ]
        
        print(f"\nResources with 'enterprise' tag: {len(enterprise_resources)}")
        if enterprise_resources:
            print("Examples:")
            for r in enterprise_resources[:3]:
                print(f"  - {r.name}")
        
        # Filter by Chrome version
        chrome_137_resources = [
            r for r in resources 
            if hasattr(r, '_meta') and '_fastmcp' in r._meta 
            and 'chrome-137' in r._meta['_fastmcp'].get('tags', [])
        ]
        
        print(f"\nResources for Chrome 137: {len(chrome_137_resources)}")


async def test_resource_reading():
    """Test reading specific resources"""
    async with AsyncClient("ws://localhost:4242") as client:
        print("\n=== Testing Resource Reading ===")
        
        # Read a static resource
        try:
            prompt = await client.read_resource("file://enterprise-prompt")
            print(f"\nEnterprise prompt loaded: {len(prompt[0].text)} characters")
            print(f"First 100 chars: {prompt[0].text[:100]}...")
        except Exception as e:
            print(f"Error reading enterprise prompt: {e}")
        
        # Read a dynamic resource
        resources = await client.list_resources()
        dynamic_resources = [r for r in resources if r.uri.startswith("upstream://")]
        
        if dynamic_resources:
            first_resource = dynamic_resources[0]
            print(f"\nReading dynamic resource: {first_resource.uri}")
            try:
                content = await client.read_resource(first_resource.uri)
                print(f"Successfully read: {len(content[0].text)} characters")
                print(f"First 100 chars: {content[0].text[:100]}...")
            except Exception as e:
                print(f"Error reading resource: {e}")


async def main():
    """Run all tests"""
    print("FastMCP Resource System Client Tests")
    print("====================================")
    print("Note: Requires FastMCP server running on localhost:4242\n")
    
    try:
        await test_resource_listing()
        await test_tag_filtering()
        await test_resource_reading()
        print("\n=== All Tests Complete ===")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure the FastMCP server is running: python fast_mcp_server.py")


if __name__ == "__main__":
    asyncio.run(main())