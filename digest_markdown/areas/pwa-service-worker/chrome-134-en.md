---
layout: default
title: chrome-134-en
---

## Detailed Updates

The following items expand on the summary above and describe what changed, how it works, and practical developer uses.

### Document subtitle (Fix PWA app titles)

#### What's New
Adds a page subtitle for installed running PWAs that supplies complementary information displayed in the window's title bar, replacing the text from the HTML title element for that window.

#### Technical Details
The feature exposes a separate subtitle value associated with the current window of an installed PWA; when present it is shown in the window title area instead of the document's HTML <title>. See the linked spec and tracking bug for implementation and interoperability notes.

#### Use Cases
- Show contextual state or view names (e.g., "Inbox — Work") in the PWA window title without modifying the document title used for tabs.
- Improve clarity for multi-window PWAs where each window represents different content or user context.

#### References
- Tracking bug #1351682: https://issues.chromium.org/issues/1351682
- ChromeStatus.com entry: https://chromestatus.com/feature/5168096826884096
- Spec: https://github.com/whatwg/html/compare/main...diekus:html:main

### User link capturing on PWAs

#### What's New
Links that could be handled by an installed web app are automatically directed to that app, simplifying navigation between the browser and installed experiences to better match user expectations.

#### Technical Details
When a user clicks a navigational link that is eligible for handling by an installed web app, Chrome will open the link in the installed app rather than keeping navigation confined to the browser. Refer to the developer documentation and ChromeStatus entry for eligibility criteria and behavior details.

#### Use Cases
- Ensure deep links from web pages open the installed app for a more integrated user flow.
- Reduce user friction when moving between browser context and app context, improving retention and engagement for PWAs.

#### References
- developer documentation: https://docs.google.com/document/d/e/2PACX-1vSqYzAmiLr-58OgSWBITtAAu6_2XUpjjNEdMvc6IdZn9DjQCeVrE0SKViumyly0cpryxAONMq62zwHw/pub
- ChromeStatus.com entry: https://chromestatus.com/feature/5194343954776064
