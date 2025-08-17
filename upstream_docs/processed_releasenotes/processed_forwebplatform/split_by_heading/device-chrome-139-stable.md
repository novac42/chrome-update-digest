## Device

### WebXR depth sensing performance improvements

Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, with the goal of improving the performance of the generation or consumption of the depth buffer.

The key mechanisms exposed are: the ability to request the raw or smooth depth buffer, the ability to request that the runtime stop or resume providing the depth buffer, and the ability to expose a depth buffer that does not align with the user's view exactly, so that the user agent does not need to perform unnecessary re-projections every frame.

[Tracking bug #410607163](https://issues.chromium.org/issues/410607163) | [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864) | [Spec](https://immersive-web.github.io/depth-sensing)
