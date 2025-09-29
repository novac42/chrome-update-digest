## Area Summary

Chrome 139 makes JSON MIME type detection specification-compliant by recognizing all valid JSON MIME types per the WHATWG mimesniff spec. The most impactful change for developers is broader, consistent detection of JSON payloads (including vendor and custom types ending with +json), which reduces interoperability surprises in APIs that branch on Content-Type. This alignment advances the web platform by enforcing a single, standards-based detection model across features that parse or treat JSON. For JavaScript developers, this improves reliability in fetch/XHR handling, service workers, and other runtime behaviors that depend on Content-Type classification.

## Detailed Updates

The concise change above affects how the browser classifies JSON payloads and therefore how JavaScript code and web APIs handle responses and request bodies.

### Specification-compliant JSON MIME type detection

#### What's New
Chrome now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification. This includes any MIME type whose subtype ends with `+json`, in addition to `application/json` and `text/json`.

#### Technical Details
Detection follows the WHATWG mimesniff rules for JSON MIME types (subtype ends with `+json` or is `application/json`/`text/json`), bringing Chrome behavior into alignment with the spec.

#### Use Cases
- Fetch/XHR response handling that branches on Content-Type for JSON parsing.
- Service workers and other request/response filters that rely on accurate JSON classification.
- Server and client integrations using vendor-specific or custom `+json` subtypes (e.g., `application/vnd.company+json`) will be correctly treated as JSON.

#### References
- https://chromestatus.com/feature/5470594816278528
- https://mimesniff.spec.whatwg.org/#json-mime-type