---
layout: default
title: Chrome 144 Devices Updates
---

# Chrome 144 Devices Updates

## Area Summary

Chrome 144 brings a significant performance enhancement to the WebXR ecosystem with the introduction of the XRVisibilityMaskChange event. This update addresses a key optimization challenge in virtual and augmented reality experiences by providing developers with precise viewport visibility information. By enabling applications to limit rendering to only the visible portions of the user's viewport, this feature can substantially reduce GPU workload and improve frame rates in immersive experiences. The addition extends the core WebXR specification with practical performance tooling that benefits both developers and end users experiencing VR/AR content.

## Detailed Updates

This release focuses on a single but impactful enhancement that gives WebXR developers better control over rendering performance through visibility masking.

### XRVisibilityMaskChange

#### What's New

Chrome 144 introduces the `XRVisibilityMaskChange` event, a new WebXR API that exposes the visible portion of a user's viewport as a mesh representation. This event provides developers with vertex and index data that precisely defines which areas of the viewport are actually visible to the user, accounting for optical characteristics of VR/AR headsets.

#### Technical Details

The `XRVisibilityMaskChange` event delivers two key pieces of data: a list of vertices and a list of indices that together represent the mesh geometry of the visible viewport area. To support proper pairing between masks and views, `XRView` objects have been enhanced with unique identifiers, making it straightforward to associate each visibility mask with its corresponding view. This implementation extends the core WebXR specification with functionality that was previously unavailable in the standard API.

#### Use Cases

The primary application of this feature is performance optimization in WebXR experiences. By knowing exactly which portions of the viewport are visible, developers can implement view frustum culling or stencil-based rendering techniques that skip drawing pixels outside the visible area. This is particularly valuable for complex VR/AR scenes where GPU performance is critical, as it can significantly reduce fragment shader workload and improve frame rates. The feature is especially beneficial for high-fidelity applications like architectural visualizations, training simulations, and immersive gaming experiences where maintaining consistent frame rates is essential for user comfort.

#### References

- [Tracking bug #450538226](https://issues.chromium.org/issues/450538226)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5073760055066624)
- [Spec](https://immersive-web.github.io/webxr/#xrvisibilitymaskchangeevent-interface)
