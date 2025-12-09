## Area Summary

Chrome 143 (stable) advances JavaScript-related platform capabilities across internationalization, editable text APIs, input event data, and federated identity. The release upgrades ICU to support Unicode 16, fixes and refines EditContext TextFormat properties, exposes clipboard/drag data on certain input events, and allows IdPs in FedCM to return structured JSON. These changes reduce developer friction for localization, rich-text editing, paste/drop handling, and authentication flows, and they tighten parity between platform behavior and web specs.

## Detailed Updates

The following items expand on the summary above with concise technical and developer-focused details.

### ICU 77 (supporting Unicode 16)

#### What's New
Chrome's ICU library is upgraded to 77.1, adding Unicode 16 support and updated locale data.

#### Technical Details
The upgrade updates Intl-related behavior (locale data, collation, formatting). The release notes warn that two changes could pose risk for web apps that assume specific output formats from Intl JS APIs.

#### Use Cases
Improves correctness for internationalized formatting, sorting, and locale-sensitive operations; apps relying on exact Intl string formats should validate outputs after the upgrade.

#### References
- [Tracking bug #421834885](https://issues.chromium.org/issues/421834885)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5143313833000960)
- [Spec](https://tc39.es/ecma402)

### EditContext: TextFormat underlineStyle and underlineThickness

#### What's New
Chrome fixes the EditContext/TextFormat behavior so underlineStyle and underlineThickness are correctly exposed via the textformatupdate event.

#### Technical Details
The EditContext API now supplies a corrected TextFormat object in textformatupdate callbacks, aligning implementation with the W3C Edit Context spec for rich-text attribute reporting.

#### Use Cases
Enables robust handling of underline styling and thickness in web editors and IME integrations; beneficial for collaborative editors and accessibility tooling that reads format attributes.

#### References
- [EditContext API](https://developer.mozilla.org/docs/Web/API/EditContext)
- [`TextFormat`](https://developer.mozilla.org/docs/Web/API/TextFormat)
- [textformatupdate event](https://developer.mozilla.org/docs/Web/API/EditContext/textformatupdate_event)
- [Tracking bug #354497121](https://issues.chromium.org/issues/354497121)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6229300214890496)
- [Spec](https://w3c.github.io/edit-context/#textformatupdateevent)

### `DataTransfer` property for `insertFromPaste`, `insertFromDrop` and `insertReplacementText` input events

#### What's New
Input events with inputType of insertFromPaste, insertFromDrop, and insertReplacementText now include a populated dataTransfer property.

#### Technical Details
The InputEvent interface exposes a DataTransfer object on those input events, giving script access to the same clipboard and drag-drop payloads available during paste/drop operations, per the input events spec.

#### Use Cases
Allows editors and contenteditable handlers to inspect and process pasted or dropped content synchronously in input event handlers without separate clipboard or drag event plumbing.

#### References
- [Tracking bug #401593412](https://issues.chromium.org/issues/401593412)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6715253274181632)
- [Spec](https://w3c.github.io/input-events/#dom-inputevent-datatransfer)

### FedCM: Support structured JSON responses from IdPs

#### What's New
FedCM now accepts structured JSON objects from Identity Providers at the id_assertion_endpoint instead of only plain strings.

#### Technical Details
IdPs may return parsed JSON in assertions consumed by Relying Parties; the browser surfaces these structured responses, removing the need for manual string serialization and parsing in RP code.

#### Use Cases
Simplifies FedCM integrations, enables richer assertion payloads (claims, metadata), and reduces encoding/decoding errors in federated sign-in flows.

#### References
- [Tracking bug #346567168](https://issues.chromium.org/issues/346567168)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5153509557272576)
- [Spec](https://github.com/w3c-fedid/FedCM/pull/771)