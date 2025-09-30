---
layout: default
title: enterprise-en
---

## Area Summary

Chrome 137 (stable) for Enterprise focuses on enhanced security monitoring and incident response. The release adds collection and reporting of local and remote IP addresses and forwards those addresses to the Security Investigation Logs (SIT). Administrators are indicated to have an optional control related to sending IP addresses. These updates strengthen enterprise visibility for investigations and centralized security tooling.

## Detailed Updates

Below are the Enterprise-area changes that expand on the summary above.

### IP address logging and reporting

#### What's New
Chrome Enterprise is enhancing security monitoring and incident response capabilities by collecting and reporting local and remote IP addresses and sending those IP addresses to the Security Investigation Logs (SIT). In addition, Chrome Enterprise will allow admins to optionally send the IP addresse...

#### Technical Details
- The release notes state that Chrome will collect both local and remote IP addresses and report them into SIT.
- The notes also indicate an administrative option to optionally send IP addresses (see the reference for full details).

#### Use Cases
- Improves enterprise security monitoring and incident response by surfacing network-level indicators in centralized logs.
- Enables organizations using SIT to correlate browser activity with IP-level data for investigations.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5110849951309824

Save path: digest_markdown/webplatform/Enterprise/chrome-137-stable-en.md
