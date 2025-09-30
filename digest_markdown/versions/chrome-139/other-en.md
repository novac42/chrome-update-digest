---
layout: default
title: other-en
---

## Area Summary

Chrome 139 (stable) introduces an experiment in the "other" area that exposes a WebGPU compatibility mode for developer testing. The main theme is enabling early experimentation with WebGPU behavior changes that are not yet on by default. The most impactful change for developers is the ability to opt into compatibility behavior to validate workloads and surface migration gaps. These updates advance the web platform by letting implementers and authors test GPU-oriented code paths ahead of default rollout.

## Detailed Updates

The single update below follows from the summary and highlights how to experiment with WebGPU compatibility behavior in Chrome 139.

### Enable the feature

#### What's New
By default, WebGPU compatibility mode is not enabled in Chrome, but it can be experimented with in Chrome 139 by explicitly enabling the functionality. You can activate it locally by enabling the "Experimental Web Platform Features" flag.

#### Technical Details
- The feature is behind an experimental flag in Chrome 139 and is not enabled by default.
- Developers must explicitly opt in to exercise the compatibility mode and observe any compatibility-related behaviors or regressions.

#### Use Cases
- Validate and test WebGPU-based applications against forthcoming compatibility behaviors before they become default.
- Surface and report discrepancies in GPU-backed web content to aid migration and implementation work.
- Use as a staging step for libraries and frameworks that rely on WebGPU to ensure forward compatibility.

#### References
- WebGPU compatibility mode: https://chromestatus.com/feature/6436406437871616
