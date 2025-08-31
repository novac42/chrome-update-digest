## Payments

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError

Correct the error type thrown during WebAuthn credential creation for payment credentials. Due to a historic specification mismatch, creating a payment credential in a cross-origin iframe without a user activation would throw a `SecurityError` instead of a `NotAllowedError`, which is what is thrown for non-payment credentials. This is a breaking change, albeit a niche one. Code that previously detected the type of error thrown (for example, `e instanceof SecurityError`) is affected. Code that just generally handles errors during credential creation (for example, `catch (e)`) will continue to function correctly.

**References:** [Tracking bug #41484826](https://bugs.chromium.org/p/chromium/issues/detail?id=41484826) | [ChromeStatus.com entry](https://chromestatus.com/feature/5096945194598400) | [Spec](https://w3c.github.io/webauthn/#sctn-creating-a-credential)
