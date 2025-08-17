# TODO: YAML Resources and Remote Hosting Implementation Plan

## Overview
This document outlines the implementation plan for adding YAML file support as MCP resources and enabling public hosting of processed release notes via CDN/remote URLs.

## Current State
- **Resources Supported**: Only Markdown files (`.md`)
- **MIME Type**: `text/markdown`
- **Hosting**: Local files only (`file://` scheme)
- **YAML Files**: Generated but not exposed as MCP resources

## Target State
- **Resources Supported**: Markdown (`.md`) and YAML (`.yml`, `.yaml`)
- **MIME Types**: Proper content types for each format
- **Hosting**: Support for local, remote (CDN), and hybrid modes
- **Deployment**: Automated resource publishing to public URLs

## Implementation Phases

### Phase 1: YAML File Support

#### TODO: yaml-resources-1 - Modify ProcessedReleaseNotesResource
**File**: `src/mcp_resources/processed_releasenotes.py`
- [ ] Update file scanning logic to include `.yml` and `.yaml` extensions
- [ ] Modify `list_resources()` method to discover YAML files
- [ ] Add YAML-specific metadata extraction

#### TODO: yaml-resources-2 - Configure MIME Types
**File**: `src/mcp_resources/processed_releasenotes.py`
```python
def get_mime_type(file_path: str) -> str:
    if file_path.endswith('.md'):
        return 'text/markdown'
    elif file_path.endswith(('.yml', '.yaml')):
        return 'application/yaml'
    elif file_path.endswith('.json'):
        return 'application/json'
    return 'text/plain'
```

#### TODO: yaml-resources-3 - Update Resource Discovery
**Directories to scan**:
- `processed_forwebplatform/*.yml` - Main WebPlatform YAML files
- `processed_forwebplatform/{area}/*.yml` - Area-specific YAML files
- `processed_forenterprise/*.yaml` - Enterprise YAML files
- `feature_details/**/*.yml` - Feature detail YAML files

### Phase 2: Remote Hosting Configuration

#### TODO: remote-hosting-1 - Base URL Configuration
**File**: `src/utils/resource_hosting_config.py` (new)
```python
class ResourceHostingConfig:
    def __init__(self):
        self.mode = 'local'  # local | remote | hybrid
        self.cdn_base = None
        self.version_prefix = 'v1'
        
    def get_resource_url(self, relative_path: str) -> str:
        if self.mode == 'local':
            return f"file://{relative_path}"
        elif self.mode == 'remote':
            return f"{self.cdn_base}/{self.version_prefix}/{relative_path}"
        else:  # hybrid
            # Logic for determining local vs remote
            pass
```

#### TODO: remote-hosting-2 - Environment Variable Support
**Environment Variables**:
```bash
# Hosting mode: local, remote, or hybrid
export MCP_RESOURCE_MODE=remote

# CDN base URL (no trailing slash)
export MCP_CDN_BASE=https://cdn.example.com/chrome-digests

# Optional: Version prefix for API versioning
export MCP_RESOURCE_VERSION=v1

# Optional: Fallback to local if remote fails
export MCP_FALLBACK_LOCAL=true
```

#### TODO: remote-hosting-3 - Hybrid Mode Implementation
**Logic**:
1. Check environment/configuration for mode
2. In hybrid mode:
   - Use remote for production versions (stable releases)
   - Use local for development versions (beta, canary)
   - Fallback to local if remote fetch fails

### Phase 3: Resource URL Mapping

#### TODO: resource-mapping-1 - URL Structure Design
**URL Patterns**:
```
# Local files:
file://chrome-138-enterprise.yaml
file://webplatform/chrome-138-stable.yml

# Remote URLs (CDN):
https://cdn.example.com/v1/enterprise/chrome-138.yaml
https://cdn.example.com/v1/webplatform/chrome-138-stable.yml
https://cdn.example.com/v1/webplatform/css/chrome-138-stable.yml

# With versioning:
https://cdn.example.com/v1/2024-01/enterprise/chrome-138.yaml
```

#### TODO: resource-mapping-2 - Version Management
**Versioning Strategy**:
- Include generation timestamp in metadata
- Support multiple versions via URL path
- Enable version pinning for stability

### Phase 4: Deployment Infrastructure

#### TODO: deployment-1 - CDN Upload Script
**File**: `scripts/deploy_resources.py` (new)
```python
#!/usr/bin/env python3
"""
Deploy MCP resources to CDN/cloud storage
"""

class ResourceDeployer:
    def __init__(self, target: str, config: dict):
        self.target = target  # s3, gcs, azure, cloudflare
        self.config = config
        
    def deploy_s3(self, files: List[Path]):
        # AWS S3 deployment logic
        pass
        
    def deploy_gcs(self, files: List[Path]):
        # Google Cloud Storage deployment
        pass
        
    def deploy_azure(self, files: List[Path]):
        # Azure Blob Storage deployment
        pass

# Usage:
# python scripts/deploy_resources.py --target s3 --bucket chrome-digests --region us-east-1
# python scripts/deploy_resources.py --target gcs --bucket chrome-digests --project my-project
```

#### TODO: deployment-2 - Resource Manifest Generation
**File**: `resources-manifest.yaml`
```yaml
version: "1.0"
generated: "2025-08-15T10:00:00Z"
resources:
  - path: "enterprise/chrome-138.yaml"
    type: "yaml"
    mime_type: "application/yaml"
    hash: "sha256:abc123def456..."
    size: 12345
    updated: "2025-08-15T09:00:00Z"
    tags: ["enterprise", "chrome-138", "stable"]
    
  - path: "webplatform/chrome-138-stable.yml"
    type: "yaml"
    mime_type: "application/yaml"
    hash: "sha256:789ghi012jkl..."
    size: 23456
    updated: "2025-08-15T09:30:00Z"
    tags: ["webplatform", "chrome-138", "stable"]
```

### Phase 5: Testing

#### TODO: testing-1 - YAML Resource Loading Tests
**Test Cases**:
- [ ] Load YAML file via MCP protocol
- [ ] Verify correct MIME type is returned
- [ ] Test YAML parsing and content integrity
- [ ] Test large YAML file handling

#### TODO: testing-2 - Remote Resource Tests
**Test Cases**:
- [ ] Fetch resource from HTTP URL
- [ ] Fetch resource from HTTPS URL
- [ ] Handle 404 errors gracefully
- [ ] Test timeout and retry logic
- [ ] Verify fallback to local files
- [ ] Test CDN cache headers

### Phase 6: Documentation

#### TODO: documentation-1 - Configuration Guide
**Documentation Topics**:
- How to configure remote hosting
- Environment variable reference
- CDN setup guides (AWS, GCP, Azure)
- Deployment workflow
- Troubleshooting guide

## File Changes Summary

### Files to Modify:
1. `src/mcp_resources/processed_releasenotes.py` - Add YAML support
2. `fast_mcp_server.py` - Update resource registration logic
3. `.env.example` - Add new environment variables

### Files to Create:
1. `src/utils/resource_hosting_config.py` - Hosting configuration
2. `scripts/deploy_resources.py` - Deployment script
3. `config/hosting.yaml` - Default hosting configuration
4. `docs/hosting-setup.md` - Setup documentation

## Success Criteria

1. **YAML Support**: All YAML files are discoverable as MCP resources
2. **Remote Hosting**: Resources can be served from CDN
3. **Backward Compatibility**: Existing local file access continues to work
4. **Performance**: Remote resources load within acceptable latency
5. **Reliability**: Graceful fallback when remote resources unavailable
6. **Documentation**: Complete setup and deployment guides

## Timeline Estimate

- **Phase 1 (YAML Support)**: 2-3 hours
- **Phase 2 (Remote Config)**: 3-4 hours
- **Phase 3 (URL Mapping)**: 2-3 hours
- **Phase 4 (Deployment)**: 4-5 hours
- **Phase 5 (Testing)**: 3-4 hours
- **Phase 6 (Documentation)**: 2-3 hours

**Total Estimate**: 16-22 hours

## Risk Mitigation

1. **Risk**: CDN outages affecting resource availability
   - **Mitigation**: Implement local fallback mechanism

2. **Risk**: Large YAML files causing performance issues
   - **Mitigation**: Implement streaming/chunked loading

3. **Risk**: Breaking changes to existing integrations
   - **Mitigation**: Maintain backward compatibility, gradual rollout

## Next Steps

1. Review and approve this plan
2. Start with Phase 1 (YAML support) as it's foundational
3. Set up test CDN environment for Phase 2
4. Implement in feature branch for testing
5. Deploy to staging before production

## Notes

- Consider using CloudFlare R2 or Bunny CDN for cost-effective hosting
- Implement cache headers for optimal CDN performance
- Consider adding resource compression (gzip) for large files
- Future enhancement: GraphQL endpoint for querying resources