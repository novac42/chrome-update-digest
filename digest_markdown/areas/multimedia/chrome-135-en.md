---
layout: default
title: Chrome 135 Multimedia Update Digest
---

# Chrome 135 Multimedia Update Digest

## Area Summary

Chrome 135 introduces a notable enhancement in the Multimedia domain by expanding the capabilities of the Web Speech API. The main theme of this release is improved flexibility for audio input sources in speech recognition workflows. The most impactful change for developers is the ability to use any MediaStreamTrack, not just the default microphone, as input for speech recognition. This advancement empowers richer, more adaptable multimedia applications and aligns the web platform with modern user and developer expectations for audio processing. These updates matter because they unlock new scenarios for accessibility, media manipulation, and real-time communication on the web.

## Detailed Updates

This release focuses on a single but significant feature that broadens the input options for web-based speech recognition, offering developers greater control and integration possibilities.

### Add MediaStreamTrack support to the Web Speech API

#### What's New
Developers can now use any MediaStreamTrack as the audio source for the Web Speech API, rather than being limited to the user's default microphone.

#### Technical Details
Previously, the Web Speech API only accepted audio from the default microphone. With this update, developers can pass a MediaStreamTrack—such as audio from a screen capture, a remote peer connection, or a processed audio stream—directly to the API for speech recognition. This is achieved by extending the API's input handling to accept MediaStreamTrack objects, aligning with other modern web media APIs.

#### Use Cases
- Enabling speech recognition on audio from screen recordings or remote streams.
- Applying custom audio processing (e.g., noise reduction, effects) before speech recognition.
- Supporting accessibility scenarios where the audio source is not the user's microphone.
- Integrating with conferencing or collaborative applications that mix multiple audio sources.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5178378197139456)
- [Spec](https://wicg.github.io/speech-api)
