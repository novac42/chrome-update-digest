#!/usr/bin/env python3
"""
Test script for area-specific digest generation.
"""

import sys
import asyncio
from pathlib import Path
from unittest.mock import Mock

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool


async def test_area_specific_digest():
    """Test generating digest for a specific area."""
    
    tool = EnhancedWebplatformDigestTool()
    
    # Create a mock context
    ctx = Mock()
    ctx.sample = None  # Will use fallback digest
    
    print("Testing area-specific digest generation...")
    print("="*50)
    
    # First, generate YAML files split by area
    print("\n1. Generating area-split YAML files for Chrome 138...")
    result = await tool.run(
        ctx=ctx,
        version="138",
        channel="stable",
        split_by_area=True,
        use_cache=False,
        debug=True
    )
    
    print("\n" + "="*50)
    print("2. Testing area-specific digest for CSS area...")
    print("="*50)
    
    # Generate digest for CSS area
    css_digest = await tool.run(
        ctx=ctx,
        version="138", 
        channel="stable",
        target_area="css",  # Specify CSS area
        language="en",
        use_cache=True,
        debug=True
    )
    
    print("\n--- CSS Area Digest Preview ---")
    print(css_digest[:1000] if len(css_digest) > 1000 else css_digest)
    
    print("\n" + "="*50)
    print("3. Testing area-specific digest for WebAPI area...")
    print("="*50)
    
    # Generate digest for WebAPI area
    webapi_digest = await tool.run(
        ctx=ctx,
        version="138",
        channel="stable", 
        target_area="webapi",  # Specify WebAPI area
        language="en",
        use_cache=True,
        debug=True
    )
    
    print("\n--- WebAPI Area Digest Preview ---")
    print(webapi_digest[:1000] if len(webapi_digest) > 1000 else webapi_digest)
    
    print("\n" + "="*50)
    print("4. Testing bilingual area-specific digest for Security area...")
    print("="*50)
    
    # Generate bilingual digest for Security area
    security_digest = await tool.run(
        ctx=ctx,
        version="138",
        channel="stable",
        target_area="security",  # Specify Security area
        language="bilingual",
        use_cache=True,
        debug=True
    )
    
    print("\n--- Security Area Digest Preview (Bilingual) ---")
    print(security_digest[:1000] if len(security_digest) > 1000 else security_digest)
    
    # List all available area files
    print("\n" + "="*50)
    print("Available area-specific YAML files:")
    print("="*50)
    
    yaml_dir = Path('upstream_docs/processed_releasenotes/tagged_features')
    area_files = sorted(yaml_dir.glob('chrome-138-stable-*.yml'))
    
    for file in area_files:
        area_name = file.stem.split('-')[-1]
        if area_name != 'tagged':  # Skip the general tagged file
            size = file.stat().st_size
            print(f"  - {area_name}: {file.name} ({size:,} bytes)")


async def test_prompt_replacement():
    """Test that [AREA] placeholder is correctly replaced in prompts."""
    
    tool = EnhancedWebplatformDigestTool()
    ctx = Mock()
    
    print("\nTesting prompt placeholder replacement...")
    print("="*50)
    
    # Test loading area-specific prompt
    for area in ['css', 'webapi', 'security']:
        for lang in ['en', 'zh', 'bilingual']:
            prompt = await tool._load_prompt(ctx, lang, area, debug=False)
            
            # Check that [AREA] is replaced
            if '[AREA]' in prompt:
                print(f"  ❌ {lang}-{area}: [AREA] placeholder not replaced!")
            else:
                # Count occurrences of the area name
                count = prompt.lower().count(area.lower())
                print(f"  ✅ {lang}-{area}: Area mentioned {count} times in prompt")


if __name__ == '__main__':
    print("Area-Specific Digest Generation Test")
    print("="*50)
    
    # Run async tests
    asyncio.run(test_area_specific_digest())
    
    print("\n\n")
    
    # Test prompt replacement
    asyncio.run(test_prompt_replacement())