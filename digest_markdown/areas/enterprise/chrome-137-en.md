---
layout: default
title: chrome-137-en
---

## Detailed Updates

Below are the Enterprise-area changes implied by the summary above.

### IP address logging and reporting

#### What's New
Chrome Enterprise collects and reports local and remote IP addresses and sends those IP addresses to the Security Investigation Logs (SIT). Administrators can optionally enable sending IP addresses.

#### Technical Details
Chrome captures network endpoint information (local and remote IPs) and includes that data in SIT entries for enterprise security tooling to consume. Admin controls are provided so organizations can choose whether to forward IP address data as part of their investigation logs.

#### Use Cases
- Security monitoring and incident response: enrich alerts with network context for faster root-cause analysis.
- Forensic investigations: correlate endpoint IPs across events in SIT.
- Administrative policy control: allow orgs to balance telemetry utility against privacy/compliance needs.

#### References
- https://chromestatus.com/feature/5110849951309824
