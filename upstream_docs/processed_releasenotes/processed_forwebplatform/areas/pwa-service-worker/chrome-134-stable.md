## PWA

### Document subtitle (Fix PWA app titles)

This feature allows to specify complementary information about the current window of an installed running PWA. It adds a subtitle to the page to provide contextual information that is displayed in the window's title bar. This replaces the text contained in the HTML title element.

[Tracking bug #1351682](https://issues.chromium.org/issues/1351682) | [ChromeStatus.com entry](https://chromestatus.com/feature/5168096826884096) | [Spec](https://github.com/whatwg/html/compare/main...diekus:html:main)

### User link capturing on PWAs

Web links automatically direct users to installed web apps. To better align with users' expectations around installed experiences, Chrome makes it easier to move between the browser and installed web apps. When the user clicks a link that could be handled by an installed web app, the link will open in that installed web app. Users can change this behavior through the installed web app's settings. Developers can control this behavior with the [`launch_handler`](/docs/web-platform/launch-handler) manifest property, and can reference this [developer documentation](https://docs.google.com/document/d/e/2PACX-1vSqYzAmiLr-58OgSWBITtAAu6_2XUpjjNEdMvc6IdZn9DjQCeVrE0SKViumyly0cpryxAONMq62zwHw/pub) for more information about how deep linking works with installed web apps.

[ChromeStatus.com entry](https://chromestatus.com/feature/5194343954776064)
