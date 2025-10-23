## Area Summary

Chrome 137 fixes a specification mismatch in the Payment area by aligning the error type thrown during WebAuthn credential creation for payment credentials. The most impactful change is that attempts to create a payment credential in a cross-origin iframe without user activation now throw NotAllowedError instead of SecurityError. This brings Chromium behavior into conformity with the WebAuthn spec, improving interoperability and simplifying error handling for developers. The change matters for payment integrations that rely on predictable WebAuthn error semantics, testing, and secure user-activation flows.

## Detailed Updates

The item below expands on the summary and describes developer-facing implications.

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError

#### What's New
Attempts to create a payment WebAuthn credential in a cross-origin iframe without a user activation now raise NotAllowedError (per the WebAuthn spec) rather than SecurityError.

#### Technical Details
A historic specification mismatch caused Chromium to emit SecurityError for this scenario. Chromium 137 corrects that behavior so the create-credential path follows the WebAuthn normative text: lack of required user activation in certain cross-origin contexts results in NotAllowedError. Developers relying on the previous SecurityError must update error handling and tests accordingly.

#### Use Cases
- Payment integrations using WebAuthn for credential creation in embedded frames should catch NotAllowedError when user activation is absent.
- Automated tests and error reporting for payment flows should be updated from SecurityError to NotAllowedError expectations.
- Security-sensitive flows that gate credential creation on user gestures will now see consistent, spec-aligned exceptions across browsers, aiding cross-browser interoperability.

#### References
- Tracking bug #41484826: https://bugs.chromium.org/p/chromium/issues/detail?id=41484826
- ChromeStatus.com entry: https://chromestatus.com/feature/5096945194598400
- Spec: https://w3c.github.io/webauthn/#sctn-creating-a-credential

```text
digest_markdown/webplatform/Payment/chrome-137-stable-en.md
```