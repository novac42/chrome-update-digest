## Area Summary

Chrome 138 (stable) introduces a DOM-level change focused on error modeling in the HTML-DOM area: QuotaExceededError is being moved from a name-based DOMException entry toward a DOMException-derived interface. The most impactful change for developers is that quota errors can carry structured, additional information instead of relying solely on the `name` string. This advances the web platform by enabling richer, extensible error objects and clearer programmatic handling. These updates matter because they improve diagnostic detail and future-proof APIs that report quota-related failures.

## Detailed Updates

The single change below directly follows from the summary and explains the developer-facing implications.

### Update QuotaExceededError to a DOMException derived interface

#### What's New
Previously quota-exceeded conditions were reported using a generic `DOMException` with `name = "QuotaExceededError"`. The change proposes replacing that name-only approach with a DOMException-derived interface for `QuotaExceededError` so the error can carry additional information.

#### Technical Details
- The proposal removes "QuotaExceededError" from the list of built-in `DOMException` names and introduces a dedicated interface derived from `DOMException`.
- This shift enables attaching structured data or additional fields to the error object beyond the `name` string.

#### Use Cases
- Developers can get richer diagnostics from quota failures (e.g., implementation-provided details) that assist in error handling and telemetry.
- APIs that need to signal quota limits gain an extensible error type, enabling clearer and more maintainable error-handling code paths.

#### References
- https://chromestatus.com/feature/5647993867927552
- https://whatpr.org/dom/1245.html

File path to save this digest:
```text
digest_markdown/webplatform/HTML-DOM/chrome-138-stable-en.md
```