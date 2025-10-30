---
layout: default
title: chrome-142-en
---

### 1. Area Summary

Chrome 142’s Multimedia updates focus on refining the Media Session API to provide richer context for Picture-in-Picture (PiP) interactions. The most impactful change adds a reason field to the `enterpictureinpicture` action details, enabling developers to distinguish user-initiated PiP from other triggers. This improves app-level decision-making for UI/behavior and aligns the web platform with clearer media control semantics. These incremental API improvements help developers build more predictable and user-respecting media experiences.

### 2. Detailed Updates

Below are the Multimedia-area changes that implement the summary above and how they matter to developers.

### Media session: add reason to `enterpictureinpicture` action details

#### What's New
Adds `enterPictureInPictureReason` to the `MediaSessionActionDetails` passed to the `enterpictureinpicture` action in the Media Session API, allowing developers to distinguish between `enterpictureinpicture` actions triggered explicitly by the user and other triggers.

#### Technical Details
A new field, `enterPictureInPictureReason`, is included in the `MediaSessionActionDetails` object delivered to the `enterpictureinpicture` action handler. Handlers can inspect this field to determine the origin of the PiP request (e.g., user agent UI vs. programmatic).

#### Use Cases
- Adjust UI or consent flows when PiP was explicitly requested by the user versus initiated programmatically.
- Implement different analytics, telemetry, or accessibility behavior based on the PiP entry reason.
- Provide safer defaults or guardrails for programmatic PiP triggers.

#### References
- [Tracking bug #446738067](https://issues.chromium.org/issues/446738067)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6415506970116096)  
- [Spec](https://github.com/w3c/mediasession/pull/362)

Notes on relevance: primary tags for this update include webapi, multimedia, and webgpu (as provided), with direct applicability to Media Session API consumers and media-centric web apps.
