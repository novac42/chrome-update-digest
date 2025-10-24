# TODO 1024: Add MCP Tool for Clean Data Pipeline

## Context
- `webplatform_digest` currently assumes area markdown/YAML already exist in `upstream_docs/processed_releasenotes/processed_forwebplatform/`.
- When the cache misses (e.g., Chrome 134 stable), the tool only suggests running `clean_data_pipeline` but does not ensure processed files are materialised.
- Manual runs are easy to forget, leaving digests without the corresponding “by area” processed notes.

## Goal
Automatically materialise processed release notes whenever the digest pipeline needs them, without forcing manual CLI calls.

## Proposed Approach
1. Introduce a dedicated MCP tool (e.g., `clean_data_pipeline.run`) that wraps `CleanDataPipeline.process_version_with_yaml`.
2. Extend `DigestYAMLCache.get_yaml_data` (and/or an orchestrator layer) to:
   - Detect missing processed markdown/YAML for the requested version/channel.
   - Invoke the new tool (or call the underlying pipeline directly) before retrying the read.
3. Ensure the new tool respects existing configuration (focus areas, WebGPU merge) and logs telemetry similar to other tools.

## Implementation Steps
1. **Tool scaffolding**  
   - Add new module under `src/chrome_update_digest/mcp/tools/` exposing an async entry point for the clean pipeline.  
   - Accept `version`, `channel`, `with_yaml` (default true), `output_dir` overrides.
2. **Pipeline integration**  
   - Import `CleanDataPipeline` and call `process_version_with_yaml` (fall back to markdown-only if YAML disabled).  
   - Surface warnings/errors in the MCP response.
3. **Digest workflow hook**  
   - Update `DigestYAMLCache.get_yaml_data` (or caller) to check for missing `areas/<area>/chrome-{version}-{channel}.{md,yml}`.  
   - When missing and `split_by_area=True`, invoke the new MCP tool before continuing.
4. **Telemetry / progress**  
   - Emit structured telemetry for the auto-triggered regeneration (duration, version, channel, status).  
   - Append audit entry to `.monitoring/webplatform-progress.json` if applicable.
5. **Documentation**  
   - Update `config/output_configuration.md` or relevant README sections to describe the new auto-regeneration behaviour.

## Testing
- Unit test: simulate missing processed files via temp dir, assert the tool produces markdown/YAML and `DigestYAMLCache` loads them.  
- Integration test: run `webplatform_digest` for a version with deleted processed files and confirm digests + processed files are regenerated.  
- CLI smoke test: direct MCP call to `clean_data_pipeline.run` with `--debug` logging.

## Open Questions / Follow-ups
- Should the auto-regeneration be opt-in via env flag for large runs?  
- Do we need rate limiting or concurrency control if multiple versions trigger regeneration simultaneously?  
- Is there any historical reason split files weren’t auto-generated that we need to preserve (e.g., performance limits)?
