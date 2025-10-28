## Area Summary

Chrome 139 adds on-device speech recognition support to the Web Speech API, enabling websites to confirm that audio and transcriptions are processed locally rather than sent to third parties. The release focuses on privacy-preserving, device-based recognition with an API to query per-language availability. For developers, the most impactful changes are stronger privacy guarantees, explicit feature-detection for on-device capabilities, and clearer offline/edge scenarios. These updates advance the web platform by expanding native device integrations for AI-driven input while reducing reliance on networked speech services.

## Detailed Updates

Below are the relevant details and practical guidance for the On-device AI changes introduced in Chrome 139.

### On-device Web Speech API

#### What's New
This feature adds on-device speech recognition support to the Web Speech API, allowing websites to ensure that neither audio nor transcribed speech are sent to a third-party service for processing. Websites can query the availability of on-device speech recognition for specific languages.

#### Technical Details
- The API extension provides a way to detect whether on-device recognition is available for a given language; feature-detection should be used to choose local vs. cloud fallbacks.
- Privacy model: the implementation guarantees that audio and resulting transcriptions are not dispatched to third-party services when on-device recognition is used.
- Primary platform tag: devices — integration points will be device-dependent (OS/model-level capabilities may affect availability).
- Developer considerations:
  - webapi / javascript: Use guarded feature detection and clear user prompts before activating microphone capture; fall back to existing cloud-based speech routes where on-device is unavailable.
  - security-privacy: Verify permission prompts and document the local-only processing guarantee to meet compliance and user expectations.
  - performance / multimedia: Expect lower latency and less network usage for supported locales, but test for CPU and battery impacts on target devices.
  - devices / pwa-service-worker: Consider offline-first UX paths for PWAs that rely on speech input; service workers cannot access microphones directly, so coordinate main-thread handlers.
  - webassembly / graphics-webgpu / css: No direct change to these specs from this feature, but on-device models might be integrated in the future via WASM or GPU compute—design for modular model loading and capability checks.
  - deprecations: No deprecations announced here; maintain cloud-based fallbacks for broad compatibility.

#### Use Cases
- Privacy-first voice input in web apps where sensitive speech must remain on-device.
- Offline-capable voice assistants in PWAs that can detect availability of local models and adapt UX.
- Reduced-latency voice interactions for dictation or command-and-control when on-device recognition is supported.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112)
- [Link](https://webaudio.github.io/web-speech-api)
