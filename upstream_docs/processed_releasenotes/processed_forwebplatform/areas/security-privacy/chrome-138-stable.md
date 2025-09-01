## Security

### Integrity Policy for scripts

Subresource-Integrity (SRI) enables developers to make sure the assets they intend to load are indeed the assets they are loading. But there's no current way for developers to be sure that all of their scripts are validated using SRI. The Integrity-Policy header gives developers the ability to assert that every resource of a given type needs to be integrity-checked. If a resource of that type is attempted to be loaded without integrity metadata, that attempt will fail and trigger a violation report.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5104518463627264) | [Spec](https://w3c.github.io/webappsec-csp/#integrityPolicy)
