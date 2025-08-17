# Release Notes Resources

The upstream-digest server provides access to processed Chrome release notes through both MCP resources and tools.

## Resource Access

### Dynamic Resource Template
The server provides a dynamic resource template that allows direct access to release notes:

**URI Pattern:** `upstream://processed_releasenotes/{resource_path}`

Where:
- `{resource_path}` is the full path to the resource, including category and any subdirectories
- The path starts with one of: `features`, `processed_forenterprise`, `processed_forwebplatform`, `processed_given_feature`

**Note:** The `features` and `processed_given_feature` folders have been moved to `feature_details/` directory, but the URIs remain the same for backward compatibility.

**Example URIs:**
- `upstream://processed_releasenotes/features/profile-137/bookmarks-and-reading-list-improvements-on-chrome-desktop.md`
- `upstream://processed_releasenotes/processed_forenterprise/137-organized_chromechanges-enterprise.md`

## Available Tools

### list_release_notes
Lists all available release note resources with their metadata.

**Usage:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "list_release_notes",
    "arguments": {}
  }
}
```

**Returns:** JSON array of resources with:
- `uri`: Resource identifier (e.g., `upstream://processed_releasenotes/features/profile-137/feature.md`)
- `name`: File name
- `description`: Human-readable description with version and category info
- `mimeType`: Always "text/markdown"


## Resource Structure

Release notes are organized in the following categories:

1. **Individual Features** (`features/profile-{version}/`)
   - Physical location: `feature_details/features/profile-{version}/`
   - Example: `upstream://processed_releasenotes/features/profile-137/bookmarks-and-reading-list-improvements-on-chrome-desktop.md`
   - Contains individual feature documentation

2. **Enterprise Digests** (`processed_forenterprise/`)
   - Physical location: `upstream_docs/processed_releasenotes/processed_forenterprise/`
   - Example: `upstream://processed_releasenotes/processed_forenterprise/137-organized_chromechanges-enterprise.md`
   - Chrome updates organized for enterprise users

3. **Web Platform Digests** (`processed_forwebplatform/`)
   - Physical location: `upstream_docs/processed_releasenotes/processed_forwebplatform/`
   - Example: `upstream://processed_releasenotes/processed_forwebplatform/137-webplatform-with-webgpu.md`
   - Web platform and developer-focused updates

4. **Feature Collections** (`processed_given_feature/profile/`)
   - Physical location: `feature_details/processed_given_feature/profile/`
   - Example: `upstream://processed_releasenotes/processed_given_feature/profile/chrome-137-profile-features.md`
   - Collections of features by Chrome version

## Example Usage in Code

```python
# List all resources
resources = await list_release_notes()
print(f"Found {len(resources)} release notes")

# Read a specific release note
uri = "upstream://processed_releasenotes/features/profile-137/2sv-enforcement-for-admins.md"
content = await read_release_note(uri)
print(content)
```