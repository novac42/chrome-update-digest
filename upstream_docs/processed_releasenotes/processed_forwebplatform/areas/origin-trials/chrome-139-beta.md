## New origin trials

In Chrome 139 you can opt into the following new [origin trials](/docs/web-platform/origin-trials).

### Prompt API

The [Prompt API](/docs/ai/prompt-api) is designed for interacting with an AI language model using text, image, and audio inputs. It supports various use cases, from generating image captions and performing visual searches to transcribing audio, classifying sound events, generating text following specific instructions, and extracting information or insights from text. It supports [structured outputs](/docs/ai/structured-output-for-prompt-api) which ensure that responses adhere to a predefined format, typically expressed as a JSON schema, to enhance response conformance and facilitate seamless integration with downstream applications that require standardized output formats. This API is also exposed in Chrome Extensions. This origin trial is for exposure on the web.

### Full frame rate render blocking attribute

We propose to add a new render blocking token full-frame-rate to the blocking attributes. When the renderer is blocked with the full-frame-rate token, the renderer will work at a lower frame rate so as to reserve more resources for loading.

### WebGPU Compatibility mode

Adds an opt-in, lightly restricted subset of the WebGPU API capable of running older graphics APIs such as OpenGL and Direct3D11. By opting into this mode and obeying its constraints, developers can extend the reach of their WebGPU applications to many older devices that do not have the modern, explicit graphics APIs that core WebGPU requires. For simple applications, the only required change is to specify the `"compatibility"` featureLevel when calling `requestAdapter`. For more advanced applications, some modifications may be necessary to accommodate the mode's restrictions. Since Compatibility mode is a subset, the resulting applications are also valid WebGPU Core applications and will run even on user agents that do not support Compatibility mode.
