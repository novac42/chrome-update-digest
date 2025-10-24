digest_markdown/webplatform/Devices/chrome-135-stable-en.md

```markdown
# Chrome 135 Devices Area Digest

## Area Summary

Chrome 135 introduces a significant update in the Devices area, focusing on enhancing session security by binding sessions to individual devices. The main theme is strengthening authentication and session management, providing developers with new tools to ensure that sessions cannot be hijacked or transferred between devices. The most impactful change is the introduction of device-bound session credentials, which leverages cryptographic keys to tie a session to a specific device. This advancement improves the security model of web applications, making it harder for attackers to reuse stolen session tokens and aligning the web platform with modern security best practices. These updates are crucial for developers building applications that require strong guarantees of user identity and session integrity.

## Detailed Updates

Below are the detailed updates for the Devices area in Chrome 135, highlighting the new feature and its implications for developers.

### Device bound session credentials

#### What's New
A new mechanism allows websites to securely bind a user session to a single device, ensuring that session tokens cannot be reused on other devices.

#### Technical Details
This feature enables servers to associate a session with a device by requiring proof of possession of a private key stored on the device. The browser periodically renews the session as requested by the server, presenting cryptographic proof that the session remains bound to the original device. This is currently available as an [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089), allowing developers to experiment with the API and provide feedback.

#### Use Cases
- Securing high-value or sensitive web applications (e.g., banking, enterprise portals) against session hijacking.
- Enforcing device-specific access policies for regulated industries.
- Enhancing user trust by ensuring that sessions cannot be transferred or replayed on unauthorized devices.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824)
- [Spec](https://w3c.github.io/webappsec-dbsc)
```