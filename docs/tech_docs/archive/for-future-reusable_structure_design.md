# Reusable Pipeline Structure Design

1. **Normalize the inputs**  
   - Raw release-note files live under `/release-notes/YYYY-MM-DD/`.  
   - Language-independent metadata (version, date, feature tags) sits in front-matter or a sidecar JSON/YAML file for reuse across stages.

2. **Pipeline templates (one per output type)**  
   - `english-html.pipeline.yaml` → Digest prompt-EN → HTML template-EN → `/dist/en/index.html`  
   - `chinese-html.pipeline.yaml` → Digest prompt-ZH → HTML template-ZH → `/dist/zh/index.html`  
   - `feature-md.pipeline.yaml` → Feature-breakdown prompt → MD template → `/dist/features/*.md`

3. **Parameterize the pipelines**  
   - Shared variables: `language`, `templatePath`, `outputPath`.  
   - Pass the raw note’s path into every job so only one trigger is needed.

4. **Reusable “digest” step**  
   - CLI wrapper (e.g., `node bin/digest.js`) with flags:  
     `-f <input>` `-p <prompt>` `-o <output>`  
   - Each pipeline merely swaps prompts.

5. **Reusable “render” step**  
   - Render via Remark / Handlebars.  
   - Accepts the digest JSON plus `templatePath`.

6. **CI/CD integration**  
   - GitHub Actions: single workflow matrix over `*.pipeline.yaml`.  
   - Or Azure DevOps multi-stage with one stage per pipeline file.

7. **Version the output**  
   - Push artifacts to `/dist` under the commit SHA.  
   - Optionally publish on GitHub Pages (EN HTML) and an NPM package (feature-MD).

8. **Recommended MCP servers / tools**  
   - **mcp-ingest** – Watches `/release-notes/**` (FS or webhook) and triggers the matrix pipeline.  
   - **mcp-digest** – Wraps the digest CLI as a stateless REST service (`POST /digest`) for reuse.  
   - **mcp-render** – Generic renderer exposing `POST /render` that accepts `templatePath` + data.  
   - **mcp-artifact** – Serves the `/dist` directory with versioned artifacts; simple Nginx or S3-style.  

   _Deployment model_  
   • **Micro-service**: run the four components as independent containers for maximum isolation and scalability.  
   • **Mono-service**: bundle them into a single server process exposing `/ingest`, `/digest`, `/render`, `/artifact` endpoints (or CLI sub-commands) to simplify ops for small teams.  
   Choose the model that best fits your infrastructure and traffic profile.

> Each MCP service is containerized, can be composed via docker-compose / k8s, and follows the single-responsibility principle—making the whole system easy to scale or replace.

> Add new output types by dropping another `*.pipeline.yaml` with its own prompt + template—no core code changes required.

## MCP Protocol Spec (​Mono-service)

The mono-service exposes four endpoints that map 1-to-1 with the former micro-services.  
Below is an MCP-style YAML spec that can be imported by tooling (e.g. auto-generated SDK / CLI).

```yaml
# mcp-protocol.yaml
version: 1
service: mcp
endpoints:
  - name: ingest
    method: POST
    path: /ingest
    description: Trigger pipeline based on an uploaded or referenced release note.
    request:
      contentType: application/json
      body:
        notePath: string   # path or URL to raw release-note file
        force: boolean?    # optional – bypass cache
    response:
      202:
        description: Accepted – returns pipeline run id
        body:
          runId: string

  - name: digest
    method: POST
    path: /digest
    description: Generate a digest from a release note using a specified prompt.
    request:
      contentType: application/json
      body:
        inputPath: string     # raw note location
        promptId:  string     # which prompt to use (en, zh, feature-breakdown…)
    response:
      200:
        body:
          digestPath: string  # where the digest JSON was written

  - name: render
    method: POST
    path: /render
    description: Render HTML/MD from a digest using a template.
    request:
      contentType: application/json
      body:
        digestPath:   string
        templatePath: string
    response:
      200:
        body:
          artifactPath: string  # produced HTML/MD file

  - name: artifact
    method: GET
    path: /artifact/{artifactPath}
    description: Download a rendered artifact by path.
    response:
      200:
        contentType: application/octet-stream
```

> Tools such as `mcp-cli` or client SDKs can be generated directly from the YAML to ensure contract consistency.

## MCP Server.py Refactoring Plan

To align `mcp_server.py` with the mono-service design, the following changes are needed:

### 1. **Replace current tools with the 4 mono-service tools**
   - Remove `enterprise-digest` and `webplatform-digest` tools
   - Add `ingest`, `digest`, `render`, and `artifact` tools matching the YAML spec

### 2. **Update tool schemas**
   - `ingest`: accepts `notePath` and optional `force` flag
   - `digest`: accepts `inputPath` and `promptId` (en, zh, feature-breakdown, etc.)
   - `render`: accepts `digestPath` and `templatePath`
   - `artifact`: accepts `artifactPath` for retrieval

### 3. **Implement pipeline orchestration**
   - `ingest` tool should trigger the appropriate pipeline based on available `*.pipeline.yaml` files
   - Track pipeline runs with unique `runId`s
   - Support async execution with status tracking

### 4. **Add prompt and template management**
   - Load prompts from `/prompts/{promptId}.txt` 
   - Load templates from `/templates/{templateId}.hbs` or similar
   - Make these configurable via environment or config files

### 5. **Resource handling updates**
   - Keep listing processed release notes as resources
   - Add ability to list available prompts and templates as resources
   - Add ability to list generated artifacts as resources

### 6. **State management**
   - Simple in-memory store for tracking pipeline runs
   - Or use a lightweight DB like SQLite for persistence
   - Track: runId → status, input, outputs, timestamps

### 7. **Error handling**
   - Consistent error responses matching the YAML spec
   - 202 for async operations, 200 for sync operations
   - Proper validation of promptId and templatePath

This refactoring transforms the server from a 2-tool system (enterprise/webplatform) into a flexible N-pipeline system where new outputs are added declaratively.
