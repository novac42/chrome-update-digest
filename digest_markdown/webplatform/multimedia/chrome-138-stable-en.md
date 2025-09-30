Area Summary

Chrome 138 (stable) adds explicit orientation metadata support to the WebCodecs video surface, introducing rotation and flip flags for video frames. The primary impact for developers is easier, semantically-correct handling of camera and other oriented video sources (e.g., Android cameras) without ad-hoc transforms. This advances the web platform by exposing source orientation at the API level, enabling more efficient GPU uploads and avoiding redundant CPU-side rotation. These changes matter for multimedia-heavy apps (video editors, conferencing, AR) that need consistent frame orientation and better rendering performance.

## Detailed Updates

The single Multimedia update in this release directly addresses how video frame orientation is represented and consumed by web applications and low-level media pipelines.

### Add support for video frame orientation metadata to WebCodecs

#### What's New
Introduces `rotation: int` and `flip: bool` values to various video-related interfaces in WebCodecs so that developers can work with frame sources that have orientation metadata. The `VideoFrame` interface is extended to allow creation of VideoFrames with arbitrary rotation and flip metadata.

#### Technical Details
- New metadata fields: `rotation` (integer, degrees) and `flip` (boolean) are surfaced on WebCodecs video interfaces and VideoFrame construction.
- These fields let consumers know the intended visual orientation without requiring the pixel buffer itself to be pre-rotated.
- This is a WebCodecs-level change (see spec link) and will interact with GPU upload and compositor paths; implementers can use the metadata to select orientation-aware texture uploads or shader-based transforms instead of CPU-side reformatting.

#### Use Cases
- Mobile camera apps and web-based capture pipelines: correctly interpret EXIF/camera orientation from Android and other devices.
- Real-time video (conferencing, streaming): avoid full-frame CPU transforms on every frame, reducing latency and CPU usage.
- Media processing pipelines (encoding/decoding): preserve orientation metadata across encode/decode cycles and apply transforms only where necessary (render vs. storage).

#### Area Expertise Notes
- webapi: WebCodecs API expanded to include orientation metadata; developers should check creation/consumption points for VideoFrame.
- graphics-webgpu: Orientation metadata enables more efficient GPU-side handling (texture coordinate transforms or shader rotation) rather than CPU reblits.
- javascript: WebCodecs integration in JS will surface additional properties on VideoFrame; update app logic to consult these fields.
- performance: Reduces redundant pixel manipulations and can lower end-to-end latency for real-time apps.
- multimedia: Clarifies codec and container handling of orientation by separating pixel data from presentation orientation.
- devices: Helps normalize behavior for device cameras that present frames in device-native orientations.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40243431
- https://chromestatus.com/feature/5098495055380480
- https://w3c.github.io/webcodecs/#videoframe-interface

File path for this digest:
digest_markdown/webplatform/Multimedia/chrome-138-stable-en.md