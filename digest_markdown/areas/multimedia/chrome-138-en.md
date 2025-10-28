---
layout: default
title: chrome-138-en
---

## Area Summary

Chrome 138 (stable) introduces orientation metadata support in WebCodecs for multimedia frames. The change adds explicit orientation fields so developers can detect and propagate rotation and flip information from sources like Android cameras. This standardizes handling of frame orientation inside the WebCodecs pipeline, making rendering, encoding, and processing more predictable. For developers, the update reduces the need for ad-hoc transforms and simplifies interoperability between capture devices and web-based media processing.

## Detailed Updates

The single multimedia update below implements orientation metadata in WebCodecs and directly supports the summary above.

### Add support for video frame orientation metadata to WebCodecs

#### What's New
Introduces `rotation: int` and `flip: bool` values to various video-related interfaces in WebCodecs so that developers can work with frame sources that have orientation (for example, Android cameras, certain media). The `VideoFrame` interface gains the ability to create VideoFrames with orientation metadata.

#### Technical Details
- New orientation metadata fields (`rotation`, `flip`) are added to relevant WebCodecs interfaces, and VideoFrame construction APIs accept orientation information.
- This metadata travels with frames in the WebCodecs pipeline so downstream consumers (encoders, renderers, processors) can apply or preserve the intended orientation.
- Refer to the WebCodecs spec for the authoritative interface details and the ChromeStatus/tracking bug for rollout status.

#### Use Cases
- Correctly rendering camera capture that supplies hardware orientation metadata without extra CPU-bound rotation.
- Preserving source orientation during encoding/transcoding in web-based media workflows.
- Feeding oriented frames into rendering pipelines (Canvas, WebGL/WebGPU) or WebRTC with explicit orientation semantics.
- Simplifying media editing and player logic by avoiding manual metadata hacks.

#### References
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=40243431)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5098495055380480)
- [Link](https://w3c.github.io/webcodecs/#videoframe-interface)

Developer implications by domain (concise):
- webapi: New WebCodecs fields expand the VideoFrame contract; update code that constructs/consumes VideoFrames.
- graphics-webgpu: Texture uploads and shader transforms may use orientation metadata instead of pre-rotating pixels.
- javascript: Surface-level API additions; no language-level changes.
- multimedia: Clarifies codec/processing semantics when source hardware supplies orientation.
- devices: Improves integration with camera hardware that reports frame orientation.
- performance: Potentially reduces CPU work by avoiding software rotation; use metadata-aware pipelines.
- security-privacy: No new permission surface is introduced by orientation metadata.
