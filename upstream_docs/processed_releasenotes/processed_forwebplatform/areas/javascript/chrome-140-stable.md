## JavaScript

### `Uint8Array` to and from base64 and hex

Base64 is a common way to represent arbitrary binary data as ASCII. JavaScript has `Uint8Arrays` for binary data. However, it lacks a built-in mechanism to encode that data as base64, or to take base64 data and produce a corresponding `Uint8Array`. This feature adds the ability and methods for converting between hex strings and `Uint8Arrays`.

[ChromeStatus.com entry](https://chromestatus.com/feature/6281131254874112) | [Spec](https://tc39.es/proposal-arraybuffer-base64/spec)

### View transition finished promise timing change

The current finished promise timing happens within the rendering lifecycle steps. This means that code that runs as a result of promise resolution happens after the visual frame that removes the view transition has been produced. This can cause a flicker at the end of the animation if the script moves styles to preserve a visually similar state. This change resolves the issue by moving the view transition cleanup steps to run asynchronously after the lifecycle is completed.

[Tracking bug #430018991](https://issues.chromium.org/issues/430018991) | [ChromeStatus.com entry](https://chromestatus.com/feature/5143135809961984)
