---
layout: default
title: enterprise-en
---

## Area Summary

Chrome 137 (stable) introduces targeted Enterprise telemetry enhancements focused on network visibility: Chrome Enterprise will collect and report local and remote IP addresses to improve security monitoring. The most impactful change for developers and IT teams is the integration of these IP addresses into Security Investigation Logs (SIT), enabling stronger incident response and forensic correlation. These updates advance the web platform for enterprise scenarios by improving auditability and allowing richer context in security investigations. Teams should evaluate logging, retention, and privacy practices in light of the new telemetry.

## Detailed Updates

The single Enterprise feature in this release tightens network-related telemetry for enterprise customers and security teams.

### IP address logging and reporting

#### What's New
Chrome Enterprise collects and reports local and remote IP addresses and sends those IP addresses to the Security Investigation Logs (SIT). Administrators will have an option to send IP address data as part of this capability.

#### Technical Details
- Collected data includes local and remote IP addresses tied to relevant browser activity and is forwarded to SIT for enterprise security investigation.
- Admins are provided with an opt-in mechanism to enable sending of IP address data (details and controls are referenced in the official link).

#### Use Cases
- Security investigations and incident response: correlate browser events with network endpoints.
- Audit and forensics: add network context to SIT entries for improved root-cause analysis.
- Enterprise monitoring: enrich existing security telemetry with browser-collected IP data for faster detection.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5110849951309824
