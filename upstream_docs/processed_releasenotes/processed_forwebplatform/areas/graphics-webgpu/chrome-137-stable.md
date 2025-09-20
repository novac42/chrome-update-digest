# Graphics and WebGPU - Chrome 137

## Key Updates

### 1. Texture View for External Texture Binding
- Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding
- Simplifies shader logic in video effects pipelines
- Reduces need for dynamically compiling shaders

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: texture.createView() }, // Texture view for external texture
    { binding: 1, resource: { buffer: myBuffer } },
  ],
});
```

### 2. Buffer Copy Simplification
- New method overload allows omitting offsets and size parameters in `copyBufferToBuffer()`
- Simplifies copying entire buffers

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

### 3. WGSL Workgroup Uniform Load
- New `workgroupUniformLoad(ptr)` overload for atomic loads
- Atomically loads value for all workgroup invocations

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```

### 4. GPUAdapterInfo Power Preference
- Non-standard `powerPreference` attribute available with "WebGPU Developer Features" flag
- Returns `"low-power"` or `"high-performance"`

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```

### 5. Removed Compatibility Mode Attribute
- Experimental `compatibilityMode` attribute removed
- Replaced by standardized approach for compatibility

### 1. Texture View for External Texture Binding
- Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding
- Simplifies shader logic in video effects pipelines
- Reduces need for dynamically compiling shaders

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: texture.createView() }, // Texture view for external texture
    { binding: 1, resource: { buffer: myBuffer } },
  ],
});
```


### 2. Buffer Copy Simplification
- New method overload allows omitting offsets and size parameters in `copyBufferToBuffer()`
- Simplifies copying entire buffers

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```


### 3. WGSL Workgroup Uniform Load
- New `workgroupUniformLoad(ptr)` overload for atomic loads
- Atomically loads value for all workgroup invocations

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```


### 4. GPUAdapterInfo Power Preference
- Non-standard `powerPreference` attribute available with "WebGPU Developer Features" flag
- Returns `"low-power"` or `"high-performance"`

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```


### 5. Removed Compatibility Mode Attribute
- Experimental `compatibilityMode` attribute removed
- Replaced by standardized approach for compatibility