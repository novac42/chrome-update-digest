## Area Summary

Chrome 139 (stable) updates JavaScript-relevant MIME type handling to fully follow the WHATWG mimesniff specification for JSON. The browser now recognizes any MIME subtype that ends with "+json" in addition to "application/json" and "text/json", which affects APIs that detect JSON by Content-Type. This change improves interoperability and correctness for web APIs, service workers, fetch/XHR handlers, and developer-written MIME checks. Developers should verify server Content-Type headers and avoid brittle string checks that only match "application/json".

## Detailed Updates

Below are the specific changes that implement the summary above and what they mean for JavaScript developers.

### Specification-compliant JSON MIME type detection

#### What's New
Chrome now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification, including any MIME subtype ending in `+json`, plus `application/json` and `text/json`.

#### Technical Details
Detection logic in Chromium's networking/content-sniffing layer was aligned with the WHATWG mimesniff spec. Any Content-Type whose subtype ends with `+json` is treated as JSON for APIs that perform MIME-based heuristics.

#### Use Cases
- Server APIs can use vendor or custom types like `application/vnd.api+json` and still be treated as JSON by fetch(), XHR, and other browser APIs.
- Service workers and middleware that branch on Content-Type can reliably handle `+json` subtypes without custom lists.
- Libraries that previously performed manual matching of `application/json` should update to accept `+json` or rely on response.json() behavior.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528)
- [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

File to save this digest:
```text
digest_markdown/webplatform/JavaScript/chrome-139-stable-en.md
```