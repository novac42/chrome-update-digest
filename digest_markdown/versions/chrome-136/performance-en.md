---
layout: default
title: performance-en
---

### 1. Area Summary

Chrome 136 (stable) introduces an origin-trial-driven capability that helps web applications detect and reason about bimodal page-load performance distributions (e.g., cold vs warm starts). The most impactful change for developers is the ability to segment telemetry and metrics by whether expensive, platform-level startup effects influenced a navigation. This enables more accurate percentile reporting, better performance regressions detection, and targeted optimizations (defer/heftier work scheduling) without changing end-user behavior. These updates advance the web platform by exposing signals that reduce noise in real-world performance measurement and allow teams to prioritize engineering effort more effectively.

## Detailed Updates

Below are the relevant details and developer implications connected to the summary above.

### Enable web applications to understand bimodal performance timings

#### What's New
An origin trial in Chrome 136 provides a way for web applications to detect when page-load timings are affected by bimodal factors (such as a browser cold start) so developers can separate those cases from normal navigations in telemetry and analysis.

#### Technical Details
This capability is exposed via an origin trial (see Origin Trial link). Conceptually it lets pages distinguish navigations impacted by system-level initialization or other out-of-app factors from typical navigations—reducing skew in aggregated timing distributions. Integrations will sit alongside existing timing interfaces (e.g., Navigation Timing) so instrumentation and analytics pipelines can filter or label affected events. Use this to avoid misattributing platform-level jitter to application regressions.

#### Use Cases
- Segment performance telemetry to exclude cold-start outliers when computing p50/p90/p99.
- Make A/B test cohorts more reliable by filtering navigations affected by platform initialization.
- Defer noncritical JS/CSS/worker initialization on warm paths while ensuring cold-start resilience.
- Improve CI/perf dashboards by separating platform-induced variance from application regressions.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384)
- [Link](https://w3c.github.io/navigation-timing/)

Output file: digest_markdown/webplatform/Performance/chrome-136-stable-en.md
