## Origin trials

### Device bound session credentials

A way for websites to securely bind a session to a single device.

It will let servers have a session be securely bound to a device. The browser will renew the session periodically as requested by the server, with proof of possession of a private key.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824) | [Spec](https://w3c.github.io/webappsec-dbsc)

### Interest invokers

This feature adds an `interesttarget` attribute to `<button>` and `<a>` elements. The `interesttarget` attribute adds "interest" behaviors to the element, such that when the user "shows interest" in the element, actions are triggered on the target element. Actions can include things like showing a popover. The user agent will handle detecting when the user "shows interest" in the element—when hovering the element with a mouse, hitting special hotkeys on the keyboard, or long-pressing the element on touchscreens. When interest is shown or lost, an `InterestEvent` will be fired on the target, which have default actions in the case of popovers - showing and hiding the popover.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/813462682693795841) | [Tracking bug #326681249](https://issues.chromium.org/issues/326681249) | [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176) | [Spec](https://github.com/whatwg/html/pull/11006)

### Signature-based integrity

This feature provides web developers with a mechanism to verify the provenance of resources they depend upon, creating a technical foundation for trust in a site's dependencies. In short: servers can sign responses with a Ed25519 key pair, and web developers can require the user agent to verify the signature using a specific public key. This offers a helpful addition to URL-based checks offered by Content Security Policy on the one hand, and Subresource Integrity's content-based checks on the other.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2704974526189404161) | [Tracking bug #375224898](https://issues.chromium.org/issues/375224898) | [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824) | [Spec](https://wicg.github.io/signature-based-sri)

### Speculation rules: target_hint field

This extends speculation rules syntax to allow developers to specify the target_hint field.

This field provides a hint to indicate a target navigable where a prerendered page will eventually be activated. For example, when _blank is specified as a hint, a prerendered page can be activated for a navigable opened by window.open(). The field has no effect on prefetching.

The specification allows this field to accept any strings that are valid as navigable target name or keyword as the value, but this launch supports only one of `"_self"` or `"_blank"` strings. If the hint is not specified, it's treated as if `"_self"` is specified.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1858297796243750913) | [Tracking bug #40234240](https://issues.chromium.org/issues/40234240) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162540351094784) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html)
