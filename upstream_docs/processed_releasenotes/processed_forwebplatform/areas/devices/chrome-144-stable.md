## Device

### `XRVisibilityMaskChange`

Adds an `XRVisibilityMaskChange` event that provides a list of vertices and a list of indices to represent the mesh of the visible portion of the user's viewport. This data can then limit the amount of the viewport drawn to, which improves performance. To better support this event, `XRView` objects are also given unique identifiers to allow easier pairing with the associated masks. This extends the core WebXR specification.

[Tracking bug #450538226](https://issues.chromium.org/issues/450538226) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073760055066624) | [Spec](https://immersive-web.github.io/webxr/#xrvisibilitymaskchangeevent-interface)
