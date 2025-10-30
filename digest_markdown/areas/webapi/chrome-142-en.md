---
layout: default
title: chrome-142-en
---

## Detailed Updates

The following entries expand on each change from the summary and spell out technical constraints, likely integration points, and developer use cases.

### FedCM—Support showing third-party iframe origins in the UI

#### What's New
FedCM's UI can now surface a third-party iframe's origin instead of always showing the top-level site. This improves fidelity when the embedded iframe is truly third-party.

#### Technical Details
Before Chrome 142 FedCM always showed the top-level site in its UI. The update detects when the relevant credential-requesting context is a third-party iframe and exposes that iframe origin in the FedCM prompt UI.

#### Use Cases
- Sites embedding third-party identity flows (e.g., cross-origin auth frames) can present users with the actual iframe origin, improving transparency and consent quality.
- Helps privacy/security reviewers and UX designers ensure correct origin visibility for federated sign-in flows.

#### References
- [Tracking bug #390581529](https://issues.chromium.org/issues/390581529)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5176474637959168)
- [Spec](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules

#### What's New
Chrome rejects JSON module responses whose MIME type type or subtype contains non-HTTP token code points (for example, spaces) when matched with `*+json`, aligning behavior with the MIME Sniffing specification.

#### Technical Details
The change enforces that type/subtype components must parse as valid HTTP tokens when applying a `*+json` match. This mirrors the algorithm in the MIME Sniffing spec and brings Chrome in line with other engines as part of the Interop2025 modules focus.

#### Use Cases
- Authors delivering JSON modules should ensure MIME types are well-formed (no spaces or invalid token characters) to avoid fetch/module rejection.
- Tooling and servers can be tightened to emit compliant MIME types, preventing runtime module load failures.

#### References
- [Tracking bug #440128360](https://issues.chromium.org/issues/440128360)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5182756304846848)
- [Spec](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing

#### What's New
Websites can add and update a recognition phrase list to bias speech recognition models toward specific phrases.

#### Technical Details
The API exposes a phrase-list mechanism on the Web Speech API recognition interface so developers can supply contextual phrases that the underlying model will prefer during recognition.

#### Use Cases
- Voice-driven forms or commands where a domain-specific vocabulary improves recognition accuracy.
- Updating phrase lists dynamically to reflect UI state (e.g., current playlist names or recent search terms) to reduce recognition errors.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5225615177023488)
- [Spec](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details

#### What's New
The Media Session API's `enterpictureinpicture` action now includes `enterPictureInPictureReason` in its action details to indicate why PiP was requested.

#### Technical Details
An `enterPictureInPictureReason` field is added to MediaSessionActionDetails sent to the `enterpictureinpicture` action. This enables distinguishing between triggers such as explicit user actions (for example, a UA-provided button) and other kinds of requests.

#### Use Cases
- Player implementations can adapt UI/behavior based on whether PiP was user-initiated versus initiated by script or other flows.
- Analytics and telemetry can distinguish user-driven PiP from programmatic requests for better UX tuning.

#### References
- [Tracking bug #446738067](https://issues.chromium.org/issues/446738067)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6415506970116096)
- [Spec](https://github.com/w3c/mediasession/pull/362)

File to save:
digest_markdown/webplatform/Web API/chrome-142-stable-en.md
