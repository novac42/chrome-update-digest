---
layout: default
title: Chrome 143 - Isolated Web Apps Updates
---

# Chrome 143 - Isolated Web Apps Updates

## Area Summary

Chrome 143 introduces a significant capability for Isolated Web Apps (IWA) with the Web Smart Card API, marking an important step in enabling enterprise-grade applications to migrate to the web platform. This update addresses a critical gap for organizations that rely on smart card authentication and secure credential management, particularly in government, healthcare, and financial sectors. By providing direct access to PC/SC (Personal Computer/Smart Card) implementations and card reader drivers in the host operating system, Chrome 143 enables developers to build web-based alternatives to traditional native smart card applications. The inclusion of enterprise policy controls ensures that administrators can manage this powerful API according to their organization's security requirements.

## Detailed Updates

This release focuses on bridging the gap between native smart card applications and the web platform, enabling secure authentication workflows within Isolated Web Apps.

### Web Smart Card API for Isolated Web Apps

#### What's New

The Web Smart Card API is now available exclusively for Isolated Web Apps, enabling smart card (PC/SC) applications to transition to the web platform. This API provides web applications with access to the PC/SC implementation and card reader drivers available in the host operating system, allowing developers to build web-based smart card authentication and secure credential management solutions.

#### Technical Details

This API is restricted to Isolated Web Apps to ensure a secure execution environment. The implementation exposes the PC/SC interface, which is the industry-standard API for smart card communication. This allows web applications to:

- Communicate with smart card readers connected to the system
- Send and receive Application Protocol Data Units (APDUs) to and from smart cards
- Manage smart card reader contexts and connections
- Access cryptographic operations performed by smart cards

The API includes comprehensive enterprise policy controls to manage its availability:

- **DefaultSmartCardConnectSetting**: Controls global availability of the API across the organization
- **SmartCardConnectAllowedForUrls**: Specifies which Isolated Web Apps can access the API
- **SmartCardConnectBlockedForUrls**: Explicitly blocks specific Isolated Web Apps from using the API

#### Use Cases

This API enables several important enterprise and security-focused use cases:

- **Enterprise Authentication**: Organizations can migrate existing smart card-based authentication systems to web applications while maintaining the same security guarantees
- **Government Applications**: Government agencies that mandate smart card authentication can now deploy web-based services that comply with their security requirements
- **Healthcare Systems**: Healthcare providers can build HIPAA-compliant web applications that leverage smart card authentication for accessing sensitive patient data
- **Financial Services**: Banks and financial institutions can develop web-based applications that use smart cards for transaction signing and secure authentication
- **Digital Signature Applications**: Document management systems can implement digital signature workflows using smart card-stored certificates

#### References

- [Tracking bug #1386175](https://issues.chromium.org/issues/1386175)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6411735804674048)
- [Spec](https://wicg.github.io/web-smart-card)
