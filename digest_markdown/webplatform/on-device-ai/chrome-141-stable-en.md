# Area Summary

Chrome 141 stable advances On-device AI by introducing a JavaScript Proofreader API that enables AI-assisted text proofreading in the browser. The primary impact for developers is an origin-trial-gated capability to suggest corrections for input text, backed by an AI language model. This update moves the web platform toward native, standardized text-assistance primitives accessible via web APIs. It matters because it lets teams explore integrated AI text help without relying on ad hoc extensions or non-standard integrations.

## Detailed Updates

Below is the on-device AI feature available in Chrome 141 stable, with pointers to its status and specification.

### Proofreader API

#### What's New
A JavaScript API for proofreading input text with suggested corrections, backed by an AI language model. Available via an Origin Trial.

#### Technical Details
- API surface defined in Web IDL (see Spec).
- Participation and enablement through the Origin Trial for Chrome 141 stable.
- Development is tracked via the linked tracking bug and ChromeStatus entry.

#### Use Cases
- Provide suggested corrections for user-entered text.
- Integrate AI-assisted proofreading in web editors and input flows.

#### References
- [proofreading input text with suggested corrections](/blog/proofreader-api-ot)
- [Origin Trial](/origintrials#/register_trial/1988902185437495297)
- [Tracking bug #403313556](https://issues.chromium.org/issues/403313556)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164677291835392)
- [Spec](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)