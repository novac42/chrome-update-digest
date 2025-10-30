## Web APIs

### FedCM—Support showing third-party iframe origins in the UI

Before Chrome 142, FedCM always showed the top-level site in its UI.

This works well when the iframe is conceptually first-party (for example, `foo.com` might have an iframe `foostatic.com`, which is not meaningful to the user).

But if the iframe is actually third-party, it is better to show the iframe origin in the UI so users better understand who they are sharing their credentials with. For example, a photo editor might be embedded in a book publishing web app and might want to let users access files they stored before with the photo editor. This capability is now available.

[Tracking bug #390581529](https://issues.chromium.org/issues/390581529) | [ChromeStatus.com entry](https://chromestatus.com/feature/5176474637959168) | [Spec](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules

Reject JSON module script responses whose MIME type's type or subtype contains non-HTTP token code points (for example, spaces) when matched with `*+json`. This aligns with the MIME Sniffing specification and other engines. It is part of the Interop2025 modules focus area.

[Tracking bug #440128360](https://issues.chromium.org/issues/440128360) | [ChromeStatus.com entry](https://chromestatus.com/feature/5182756304846848) | [Spec](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing

This feature enables websites to support contextual biasing for speech recognition by adding a recognition phrase list to the Web Speech API.

Developers can provide a list of phrases as well as updating them to apply a bias to the speech recognition models in favor of those phrases. This helps improve accuracy and relevance for domain-specific and personalized speech recognition.

[ChromeStatus.com entry](https://chromestatus.com/feature/5225615177023488) | [Spec](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details

Adds `enterPictureInPictureReason` to the `MediaSessionActionDetails` sent to the `enterpictureinpicture` action in the Media Session API. This allows developers to distinguish between `enterpictureinpicture` actions triggered explicitly by the user (e.g. from a button in the user agent) and `enterpictureinpicture` actions triggered automatically by the user agent due to the content becoming occluded.

[Tracking bug #446738067](https://issues.chromium.org/issues/446738067) | [ChromeStatus.com entry](https://chromestatus.com/feature/6415506970116096) | [Spec](https://github.com/w3c/mediasession/pull/362)
