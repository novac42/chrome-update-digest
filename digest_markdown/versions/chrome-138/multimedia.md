---
layout: default
title: Chrome 138 - Multimedia
---

# Chrome 138 - Multimedia

[← Back to Chrome 138](./) | [View All Multimedia Updates](/areas/multimedia/)

## Multimedia

### Add support for video frame orientation metadata to WebCodecs

Introduces `rotation: int` and `flip: bool` values to various video related interfaces in WebCodecs so that developers can work with frame sources that have orientation (For example, Android cameras, certain media). The `VideoFrame` interface grows the ability to create VideoFrames with arbitrary rotation and flip as well as accessors for this information on the VideoFrame object. The `VideoDecoderConfig` object gains rotation and flip fields that are emitted on decoded VideoFrame objects automatically. The `VideoEncoder` class gains mechanisms for passing rotation and flip information from `encode()` to the VideoDecoderConfig emitted as part of `EncodedVideoChunkMetadata`. If `encode()` is called with frames with different orientations a nonfatal exception will be thrown. `configure()` may be used to reset the allowed orientation.

**References:** [Tracking bug #40243431](https://bugs.chromium.org/p/chromium/issues/detail?id=40243431) | [ChromeStatus.com entry](https://chromestatus.com/feature/5098495055380480) | [Spec](https://w3c.github.io/webcodecs/#videoframe-interface)


---

## Navigation
- [Chrome 138 Overview](./)
- [All Multimedia Updates](/areas/multimedia/)
- [Browse Other Areas](./)
