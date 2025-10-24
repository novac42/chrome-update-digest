digest_markdown/webplatform/Origin trials/chrome-135-stable-en.md

# Chrome 135 Origin Trials Digest

## 1. Area Summary

Chrome 135 introduces several impactful Origin Trials that enhance security, user interaction, and performance for web developers. The main themes in this release focus on strengthening trust in web resources, enabling more secure device-bound sessions, improving user engagement mechanisms, and optimizing navigation through advanced prerendering hints. These features collectively advance the web platform by providing developers with new tools to build safer, more interactive, and performant applications. The updates matter because they address critical needs around resource integrity, session security, and seamless user experiences, all while allowing developers to experiment and provide feedback before broader adoption.

## 2. Detailed Updates

Below are the key Origin Trial features introduced in Chrome 135, each offering unique benefits and technical advancements for developers.

### Device bound session credentials

#### What's New
Enables websites to securely bind a session to a single device, ensuring that session renewal and authentication are tied to device-specific credentials.

#### Technical Details
The browser periodically renews the session as requested by the server, providing proof of possession of a private key unique to the device. This mechanism enhances session security by preventing session hijacking across devices.

#### Use Cases
- Secure authentication for sensitive applications (e.g., banking, enterprise portals)
- Reducing risks of session theft or replay attacks
- Enabling device-specific access controls

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824)
- [Spec](https://w3c.github.io/webappsec-dbsc)

---

### Interest invokers

#### What's New
Introduces the `interesttarget` attribute for `<button>` and `<a>` elements, allowing developers to define "interest" behaviors that trigger actions when users show interest in these elements.

#### Technical Details
By adding the `interesttarget` attribute, developers can specify target elements and actions (such as showing a popup or preview) that are triggered by user interactions indicating interest, rather than just clicks.

#### Use Cases
- Enhancing accessibility and user engagement
- Implementing richer UI interactions (e.g., previews, tooltips)
- Improving navigation and discoverability in web apps

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/813462682693795841)
- [Tracking bug #326681249](https://issues.chromium.org/issues/326681249)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176)
- [Spec](https://github.com/whatwg/html/pull/11006)

---

### Signature-based integrity

#### What's New
Provides a mechanism for verifying the provenance of web resources using digital signatures, allowing developers to require browsers to check that resources are signed by trusted servers.

#### Technical Details
Servers sign responses with an Ed25519 key pair, and browsers verify these signatures before using the resources. This builds a technical foundation for trust in third-party dependencies and mitigates supply chain risks.

#### Use Cases
- Ensuring integrity of critical scripts and assets
- Protecting against malicious or tampered dependencies
- Enabling safer use of third-party resources

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2704974526189404161)
- [Tracking bug #375224898](https://issues.chromium.org/issues/375224898)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824)
- [Spec](https://wicg.github.io/signature-based-sri)

---

### Speculation rules: target_hint field

#### What's New
Extends speculation rules syntax to include a `target_hint` field, allowing developers to specify the intended navigable target for prerendered pages.

#### Technical Details
The `target_hint` field provides hints (such as `_blank`) to indicate where a prerendered page will be activated, enabling more efficient and context-aware prerendering strategies.

#### Use Cases
- Optimizing navigation performance by preloading pages for specific targets
- Enhancing user experience with faster transitions
- Supporting advanced navigation patterns in single-page applications

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1858297796243750913)
- [Tracking bug #40234240](https://issues.chromium.org/issues/40234240)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5162540351094784)
- [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html)