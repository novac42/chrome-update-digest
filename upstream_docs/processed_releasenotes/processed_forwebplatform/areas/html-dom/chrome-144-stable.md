## DOM

### The `<geolocation>` element

Introduces the `<geolocation>` element, a declarative, user-activated control for accessing the user's location. It streamlines the user and developer journey by handling the permission flow and directly providing location data to the site. This often eliminates the need for a separate JavaScript API call.

This addresses the long-standing problem of permission prompts triggering directly from JavaScript without a strong signal of user intent. By embedding a browser-controlled element in the page, the user's click provides a clear, intentional signal. This enables a better prompt UX and, crucially, provides a recovery path for users who previously denied the permission.

**Note:** This feature was previously developed and tested in an origin trial as the more generic `<permission>` element. Based on feedback from developers and other browser vendors, it evolved into the capability-specific `<geolocation>` element to provide a more tailored and powerful developer experience.

[Tracking bug #435351699](https://issues.chromium.org/issues/435351699) | [ChromeStatus.com entry](https://chromestatus.com/feature/5125006551416832) | [Spec](https://wicg.github.io/PEPC/permission-elements.html)
