## Origin trials

### Opt out of freezing on Energy Saver

This opt out trial lets sites opt out from the freezing on Energy Saver behavior that ships in Chrome 133.

[Origin Trial](/origintrials#/register_trial/4254212798004854785) | [Tracking bug #325954772](https://issues.chromium.org/issues/325954772) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424) | [Spec](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA

Reference Target is a feature to enable using IDREF attributes such as `for` and `aria-labelledby` to refer to elements inside a component's shadow DOM, while maintaining encapsulation of the internal details of the shadow DOM. The main goal of this feature is to enable ARIA to work across shadow root boundaries.

A component can specify an element in its shadow tree to act as its "reference target". When the host component is the target of a IDREF like a label's `for` attribute, the reference target becomes the effective target of the label.

The shadow root specifies the ID of the target element inside the shadow DOM. This is done either in JavaScript with the `referenceTarget` attribute on the `ShadowRoot` object, or in HTML markup using the `shadowrootreferencetarget` attribute on the `<template>` element.

[Origin Trial](/origintrials#/register_trial/2164542570904944641) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188237101891584)
