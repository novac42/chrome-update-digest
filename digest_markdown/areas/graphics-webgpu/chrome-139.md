---
layout: default
title: Graphics and WebGPU - Chrome 139
---

# Graphics and WebGPU - Chrome 139

## WebGPU Features

### 3D texture support for BC and ASTC compressed formats

The `"texture-compression-bc-sliced-3d"` and `"texture-compression-astc-sliced-3d"` WebGPU features add support for 3D textures using Block Compression (BC) and Adaptive Scalable Texture Compression (ASTC) formats. This lets you take advantage of the efficient compression capabilities of BC and ASTC formats for volumetric texture data, offering significant reductions in memory footprint and bandwidth requirements without substantial loss in visual quality. This is particularly valuable in fields such as scientific visualization, medical imaging, and advanced rendering techniques.

The following code snippet checks whether the adapter supports 3D textures with BC and ASTC compressed formats and requests a device with these features if they are available.
    
    
    const adapter = await navigator.gpu.requestAdapter();
    
    const requiredFeatures = [];
    if (adapter?.features.has("texture-compression-bc-sliced-3d")) {
      requiredFeatures.push(
        "texture-compression-bc",
        "texture-compression-bc-sliced-3d",
      );
    }
    if (adapter?.features.has("texture-compression-astc-sliced-3d")) {
      requiredFeatures.push(
        "texture-compression-astc",
        "texture-compression-astc-sliced-3d",
      );
    }
    const device = await adapter?.requestDevice({ requiredFeatures });
    
    // Later on...
    if (device.features.has("texture-compression-astc-sliced-3d")) {
      // Create a 3D texture using ASTC compression
    } else if (device.features.has("texture-compression-bc-sliced-3d")) {
      // Create a 3D texture using BC compression
    } else {
      // Fallback: Create an uncompressed 3D texture
    }
    

Explore 3D brain scans by checking out the [Volume Rendering - Texture 3D WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=volumeRenderingTexture3D) and see the [chromestatus entry](https://chromestatus.com/feature/5080855386783744).

![3D brain scans rendered using WebGPU.](/static/blog/new-in-webgpu-139/image/brain-scans.png) A brain scan image from a 3D texture with ASTC compressed format.


### New "core-features-and-limits" feature

A new `"core-features-and-limits"` feature is being introduced for the upcoming WebGPU compatibility mode. This feature indicates that the adapter or device supports core features and limits of the WebGPU spec. "core" WebGPU is the only version available at the moment, so all WebGPU implementations must include `"core-features-and-limits"` in their supported features.

In the future, when WebGPU compatibility mode ships, an adapter or a device may not have this feature to signify it is a compatibility mode adapter or device and not a core one. When enabled on a device, this lifts all compatibility mode restrictions (features and limits).

For a detailed explanation and usage in WebGPU compatibility mode, refer to the [explainer](https://gist.github.com/greggman/0dea9995e33393c546a4c2bd2a12e50e) and the following section. See [issue 418025721](https://issues.chromium.org/issues/418025721).


### Origin trial for WebGPU compatibility mode

WebGPU is a powerful API designed for modern graphics, aligning with technologies like Vulkan, Metal, and Direct3D 12. However, a significant number of devices still lack support for these newer APIs. For example, on Windows, 31% of Chrome users don't have Direct3D 11.1 or higher. On Android, 15% of Android users don't have Vulkan 1.1, including 10% who don't have Vulkan at all.

This creates a challenge for developers who want to maximize their application's reach. They're often forced to develop multiple implementations (for example, WebGPU and WebGL), accept a more limited audience with core WebGPU, or stick to WebGL, missing out on WebGPU's advanced features like GPU compute.

![Visual representation of WebGPU compatibility mode.](/static/blog/new-in-webgpu-139/image/webgpu-compatibility-mode.png) WebGPU compatibility mode expanded reach.

WebGPU compatibility mode offers a solution by providing an opt-in, slightly restricted version of the WebGPU API. This mode is designed to run older graphics APIs like OpenGL ES 3.1 and Direct3D11, significantly expanding your application's reach to devices that don't support modern, explicit graphics APIs required by core WebGPU.

Because compatibility mode is a subset of WebGPU, applications built with it are also valid WebGPU "core" applications. This means they will seamlessly run even on browsers that don't specifically support compatibility mode.

For many basic applications, enabling compatibility mode is as straightforward as passing `featureLevel: "compatibility"` when you call [requestAdapter()](https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter). More complex applications might require [minor adjustments](https://webgpufundamentals.org/webgpu/lessons/webgpu-compatibility-mode.html) to fit within the mode's restrictions. The [Generate Mipmap WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=generateMipmap) is a good example.
    
    
    // Request a GPUAdapter in compatibility mode
    const adapter = await navigator.gpu.requestAdapter({
      featureLevel: "compatibility",
    });
    
    const hasCore = adapter?.features.has("core-features-and-limits");
    const device = await adapter?.requestDevice({
      requiredFeatures: (hasCore ? ["core-features-and-limits"] : []),
    });
    
    if (device?.features.has("core-features-and-limits")) {
      // Compatibility mode restrictions will apply
    }
    

### Enable the feature

By default, [WebGPU compatibility mode](https://chromestatus.com/feature/6436406437871616) is not enabled in Chrome, but it can be experimented with in Chrome 139 by explicitly enabling the functionality. You can activate it locally by enabling the "Experimental Web Platform Features" [flag](/docs/web-platform/chrome-flags#chromeflags) at `chrome://flags/#enable-experimental-web-platform-features`.

To enable it for all visitors to your app, an [origin trial](/origintrials#/view_trial/1489002626799370241) is underway and set to end in Chrome 145 (Apr 21, 2026). To participate in the trial, refer to the [Get started with origin trials](/docs/web-platform/origin-trials#take_part_in_an_origin_trial) post.


### Dawn updates

A `message` argument is added to the `WGPUQueueWorkDoneCallback` function to be more consistent with other callback functions that take a status as well. See [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/528).

When emdawnwebgpu is linked with `-sSHARED_MEMORY`, its webgpu.cpp file is also compiled with this flag. See [Dawn CL 244075](https://dawn-review.googlesource.com/c/dawn/+/244075).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7204..chromium/7258?n=1000).

<!-- Deduplication: 4 → 4 features -->