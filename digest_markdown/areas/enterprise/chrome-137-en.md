---
layout: default
title: chrome-137-en
---

### 1. Area Summary

Chrome 137 for Enterprise focuses on improved network telemetry for managed environments, specifically by collecting and reporting local and remote IP addresses to aid security investigations. The most impactful change for developers and admins is the addition of IP address logging and optional reporting into Security Investigation Logs (SIT), which enhances incident response and forensics. This update advances the platform by exposing richer operational signals for enterprise security tooling while introducing configuration and privacy considerations for administrators. Teams should evaluate integration, retention, and policy settings to leverage this telemetry responsibly.

## Detailed Updates

Below are the Enterprise-specific changes in this release and their practical implications for developers and administrators.

### IP address logging and reporting

#### What's New
Chrome Enterprise collects and reports local and remote IP addresses and sends those IP addresses to the Security Investigation Logs (SIT). In addition, Chrome Enterprise will allow admins to optionally send the IP addresse...

#### Technical Details
- The browser captures both local and remote IP address information as part of its enterprise telemetry surface and forwards that data into SIT.
- Admins have an optional control to enable sending IP addresses to SIT; this implies an admin-configurable policy or setting governs reporting behavior.
- The feature increases the fidelity of security logs available to enterprise investigation and monitoring tools.

#### Use Cases
- Incident response and forensic investigations that need network endpoint attribution for suspicious activity.
- Integration with SIEMs and centralized security tooling via SIT exports to correlate browser events with network logs.
- Compliance and audit workflows where visibility into client network context is required (subject to organizational privacy rules).

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5110849951309824
