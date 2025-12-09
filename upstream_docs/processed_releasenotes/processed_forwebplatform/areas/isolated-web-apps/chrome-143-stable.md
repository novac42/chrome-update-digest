## Isolated Web Apps

### Web Smart Card API for Isolated Web Apps

Available on Isolated Web Apps (IWA) only. Enables smart card (PC/SC) applications to move to the Web platform. It gives them access to the PC/SC implementation (and card reader drivers) available in the host OS.

Administrators can control the availability of this API either:

  * Globally—using the `DefaultSmartCardConnectSetting` policy.
  * Per-application—using the `SmartCardConnectAllowedForUrls` and `SmartCardConnectBlockedForUrls` policies.

[Tracking bug #1386175](https://issues.chromium.org/issues/1386175) | [ChromeStatus.com entry](https://chromestatus.com/feature/6411735804674048) | [Spec](https://wicg.github.io/web-smart-card)
