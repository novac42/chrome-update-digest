---
layout: default
title: Chrome 136 Origin Trials - Developer Preview Features
---

# Chrome 136 Origin Trials - Developer Preview Features

## Area Summary

Chrome 136 introduces three significant origin trials that address key developer pain points across audio management, performance monitoring, and canvas rendering. The **Audio Output Devices API** enhancement with `setDefaultSinkId()` gives developers programmatic control over audio routing in multi-frame applications. A new **bimodal performance timing** API helps developers understand and optimize for real-world performance variations, particularly during cold starts. Additionally, Chrome is testing a **redesigned Canvas text rendering implementation** that could significantly impact performance for graphics-intensive applications. These trials collectively advance web platform capabilities in media control, performance analytics, and graphics rendering optimization.

## Detailed Updates

These origin trials offer developers early access to experimental features that could reshape how we handle audio devices, performance measurement, and canvas operations. Each trial addresses specific technical challenges developers face in production environments.

### Audio Output Devices API: setDefaultSinkId()

#### What's New
The MediaDevices interface gains a new `setDefaultSinkId()` method that allows top-level frames to programmatically change the default audio output device used by their subframes, providing centralized audio routing control.

#### Technical Details
This API extends the existing Audio Output Devices functionality by enabling parent frames to manage audio output destinations for embedded content. The method operates at the frame level, allowing applications to coordinate audio output across multiple nested contexts without requiring individual frame-level audio device selection.

#### Use Cases
Particularly valuable for complex web applications with multiple audio sources, video conferencing platforms, multimedia editors, and dashboard applications that need consistent audio routing across embedded components. Enables better user experience in multi-frame applications where audio output coordination is critical.

#### References
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864) | [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)

### Enable web applications to understand bimodal performance timings

#### What's New
A new performance monitoring API that helps developers identify and measure bimodal performance distributions in page load times, particularly distinguishing between "cold start" and "warm start" scenarios.

#### Technical Details
Web applications often experience bimodal performance patterns due to browser initialization states, system resource competition, and caching effects. This API provides insights into these performance variations by exposing timing data that distinguishes between different loading conditions, enabling more accurate performance analysis and optimization strategies.

#### Use Cases
Essential for performance-critical applications that need to understand real-world loading behavior, optimize for different user scenarios, and make data-driven decisions about resource loading strategies. Particularly valuable for applications serving diverse user bases with varying device capabilities and network conditions.

#### References
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384) | [Spec](https://w3c.github.io/navigation-timing/)

### Update of Canvas text rendering implementation

#### What's New
Chrome is testing a completely redesigned implementation of Canvas text rendering methods including `measureText()`, `fillText()`, and `strokeText()`, focusing on performance improvements for canvas-heavy applications.

#### Technical Details
This represents a fundamental architectural change in how Canvas text operations are processed internally. While not introducing new web-exposed APIs, the implementation changes could significantly impact rendering performance, text measurement accuracy, and overall canvas operation efficiency. The origin trial allows developers to test applications against the new rendering pipeline.

#### Use Cases
Critical for applications that rely heavily on canvas text rendering, including data visualization tools, games, drawing applications, PDF viewers, and any graphics-intensive web applications. Enables developers to validate performance impacts and ensure compatibility before the new implementation becomes standard.

#### References
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #389726691](https://bugs.chromium.org/p/chromium/issues/detail?id=389726691) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104000067985408)