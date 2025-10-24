digest_markdown/webplatform/HTML-DOM/chrome-135-stable-en.md

# Chrome 135 HTML-DOM Update Digest (Stable)

## Area Summary

Chrome 135 introduces targeted enhancements to the HTML-DOM layer, focusing on improving both accessibility and integration with modern web payment flows. The main themes in this release are declarative UI behavior and streamlined payment initiation, which empower developers to build more accessible interfaces and integrate with payment ecosystems more efficiently. The addition of new attributes for button elements and support for payment-related link relations represent meaningful steps toward a more robust, interoperable, and user-friendly web platform. These updates matter because they reduce the need for custom scripting, promote best practices, and enable richer browser-native capabilities for web applications.

## Detailed Updates

This release brings two notable features to the HTML-DOM area, each designed to simplify development and enhance user experience through native browser support.

### Invoker Commands; the command and commandfor attributes

#### What's New
The `command` and `commandfor` attributes on `<button>` elements allow developers to declaratively assign behaviors to buttons, improving accessibility and reducing reliance on JavaScript event handlers.

#### Technical Details
By specifying `command` and `commandfor` attributes, buttons can be directly linked to specific actions or elements, enabling browsers to handle activation logic natively. This approach aligns with the HTML specification and ensures consistent behavior across browsers, while also making it easier for assistive technologies to interpret button intent.

#### Use Cases
- Creating accessible toolbars or dialog controls without custom scripting
- Ensuring consistent keyboard and assistive technology support for interactive elements
- Simplifying markup for complex UI components

#### References
- [Tracking bug #1490919](https://issues.chromium.org/issues/1490919)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5142517058371584)
- [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-commandfor)

### Link `rel=facilitated-payment` to support push payments

#### What's New
Support for `<link rel="facilitated-payment" href="...">` enables web pages to signal pending push payments, allowing browsers to notify registered payment clients.

#### Technical Details
When a page includes a `<link rel="facilitated-payment">`, the browser interprets this as a hint to engage payment handlers capable of processing push payments. This mechanism leverages the HTML link element and integrates with the Payment Handler API, streamlining the initiation of payment flows directly from the DOM.

#### Use Cases
- E-commerce sites prompting users to complete payments via registered payment apps
- Reducing friction in checkout flows by leveraging browser-native payment notifications
- Enabling seamless integration with third-party payment providers

#### References
- [Tracking bug #1477049](https://issues.chromium.org/issues/1477049)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5198846820352000)