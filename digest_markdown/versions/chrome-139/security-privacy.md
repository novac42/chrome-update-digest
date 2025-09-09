---
layout: default
title: Chrome 139 - Security & Privacy
---

# Chrome 139 - Security & Privacy

[← Back to Chrome 139](./) | [View All Security & Privacy Updates](/areas/security-privacy/)

## Security

### Fire error event for Content Security Policy (CSP) blocked worker

Makes Chrome conform to the specification, checking the CSP during fetch and firing the error event asynchronously instead of throwing exception when script runs "new Worker(url)" or "new SharedWorker(url)".

[Tracking bug #41285169](https://issues.chromium.org/issues/41285169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872) | [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)


---

## Navigation
- [Chrome 139 Overview](./)
- [All Security & Privacy Updates](/areas/security-privacy/)
- [Browse Other Areas](./)
