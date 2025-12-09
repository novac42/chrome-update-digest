## JavaScript

### ICU 77 (supporting Unicode 16)

The Unicode support library ICU (International Components for Unicode) is upgraded from version 74.2 to 77.1, adding support for Unicode 16 and updating locale data. Two changes could pose some risk for web applications that assume a specific format from the Intl JS APIs:

  1. The default Italian number formatting changed to omit the thousand separator for 4-digit numbers. For example `new Intl.NumberFormat("it").format(1234)` will return 1234 instead of 1.234. The old behavior can be achieved with the `useGrouping` parameter for the `Intl.NumberFormat` constructor.
  2. In some English locales (`en-AU`, `en-GB`, and `en-IN`), a comma was added after full-length weekdays, for example, changing Saturday 30 April 2011 to Saturday, 30 April 2011. Web applications should avoid relying on the precise formatting of dates and they may change again in future.

[Tracking bug #421834885](https://issues.chromium.org/issues/421834885) | [ChromeStatus.com entry](https://chromestatus.com/feature/5143313833000960) | [Spec](https://tc39.es/ecma402)

### EditContext: TextFormat underlineStyle and underlineThickness

The [EditContext API](https://developer.mozilla.org/docs/Web/API/EditContext) shipped with a bug in Chrome where the [`TextFormat`](https://developer.mozilla.org/docs/Web/API/TextFormat) object supplied by the [textformatupdate event](https://developer.mozilla.org/docs/Web/API/EditContext/textformatupdate_event) provides incorrect values for the `underlineStyle` and `underlineThickness` properties. Before Chrome 143 the possible values are `None`, `Solid`, `Dotted`, `Dashed`, `Squiggle` and `None`, `Thin`, `Thick`. However the specification lists `none`, `solid`, `dotted`, `dashed`, `wavy` and `none`, `thin`, `thick`.

The correct values as specified are now implemented from Chrome 143.

[Tracking bug #354497121](https://issues.chromium.org/issues/354497121) | [ChromeStatus.com entry](https://chromestatus.com/feature/6229300214890496) | [Spec](https://w3c.github.io/edit-context/#textformatupdateevent)

### `DataTransfer` property for `insertFromPaste`, `insertFromDrop` and `insertReplacementText` input events

Populate the `dataTransfer` property on input events with an `inputType` of `insertFromPaste`, `insertFromDrop`, and `insertReplacementText` to provide access to clipboard and drag-drop data during editing operations in contenteditable elements.

The `dataTransfer` object contains the same data that was available during the `beforeinput` event.

This feature only applies to contenteditable elements. For form controls (textarea, input), the behavior remains unchanged—the data property contains the inserted text and `dataTransfer` remains null.

[Tracking bug #401593412](https://issues.chromium.org/issues/401593412) | [ChromeStatus.com entry](https://chromestatus.com/feature/6715253274181632) | [Spec](https://w3c.github.io/input-events/#dom-inputevent-datatransfer)

### FedCM: Support structured JSON responses from IdPs

Allows Identity Providers (IdPs) to return structured JSON objects instead of plain strings to Relying Parties (RPs) using the `id_assertion_endpoint`.

This change simplifies integration for developers by eliminating the need to manually serialize and parse JSON strings. It enables more dynamic and flexible authentication flows, allowing RPs to interpret complex responses directly and support varied protocols like OAuth2, OIDC, or IndieAuth without out-of-band agreements.

[Tracking bug #346567168](https://issues.chromium.org/issues/346567168) | [ChromeStatus.com entry](https://chromestatus.com/feature/5153509557272576) | [Spec](https://github.com/w3c-fedid/FedCM/pull/771)
