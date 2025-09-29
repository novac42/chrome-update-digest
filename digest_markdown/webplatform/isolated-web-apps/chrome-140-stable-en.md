# Chrome 140 Stable - Isolated Web Apps Updates

## Area Summary

Chrome 140 introduces a significant advancement for Isolated Web Apps (IWAs) with the new Controlled Frame API, representing a major step forward in secure web application architecture. This feature enables IWAs to embed any content, including third-party resources that traditional `<iframe>` elements cannot handle, while maintaining strict security boundaries. The Controlled Frame API brings desktop-class application capabilities to the web platform by providing granular control over embedded content, similar to native application frameworks. This update reinforces Chrome's commitment to enabling more powerful and secure web applications through the IWA model, offering developers new possibilities for creating sophisticated web-based applications with enhanced isolation and control mechanisms.

## Detailed Updates

Building on the foundation of Isolated Web Apps, Chrome 140 delivers a powerful new embedding capability that expands what's possible within the secure IWA environment.

### Controlled Frame API (available only to IWAs)

#### What's New
The Controlled Frame API introduces a new way for Isolated Web Apps to embed content that goes beyond the limitations of traditional `<iframe>` elements. This API allows IWAs to embed all types of content, including third-party resources that cannot be embedded using standard web technologies, while providing enhanced control over the embedded content's behavior and interactions.

#### Technical Details
The Controlled Frame API operates exclusively within the Isolated Web Apps security model, ensuring that the powerful embedding capabilities are only available to applications that meet IWA's strict isolation requirements. Unlike standard `<iframe>` elements, which are subject to various security restrictions and cross-origin policies that can prevent embedding of certain third-party content, Controlled Frame provides a more flexible embedding mechanism. The API allows developers to control various aspects of the embedded content's execution environment and behavior, giving IWAs capabilities similar to native application frameworks on other platforms.

#### Use Cases
This feature enables developers to create more sophisticated web applications that can integrate diverse content sources without being constrained by traditional web security limitations. Potential applications include business applications that need to embed legacy systems, educational platforms that integrate multiple third-party tools, or enterprise software that requires seamless integration of various web services. The controlled environment ensures that even when embedding untrusted third-party content, the host IWA maintains security and stability.

#### References
- [Isolated Web Apps explainer](https://github.com/WICG/isolated-web-apps/blob/main/README.md)
- [Tracking bug #40191772](https://issues.chromium.org/issues/40191772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5199572022853632)
- [Spec](https://wicg.github.io/controlled-frame)