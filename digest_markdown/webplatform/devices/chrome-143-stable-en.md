# Chrome 143 Devices Area Update

## Area Summary

Chrome 143 brings a significant enhancement to the Gamepad API by introducing event handler attributes that simplify gamepad connection management. This update adds `ongamepadconnected` and `ongamepaddisconnected` event handler attributes to the `WindowEventHandlers` interface mixin, providing developers with more convenient ways to monitor gamepad connectivity. This feature aligns with the W3C Gamepad specification and makes it easier for developers to build responsive gaming experiences that react to controller connections. The addition of these event handler attributes represents a maturation of the Gamepad API, offering better developer ergonomics for a common use case in web-based gaming applications.

## Detailed Updates

This release focuses on improving the developer experience for handling gamepad events in web applications.

### Gamepad `ongamepadconnected` and `ongamepaddisconnected` event handler attributes

#### What's New

Chrome 143 adds `ongamepadconnected` and `ongamepaddisconnected` event handler attributes to the `WindowEventHandlers` interface mixin, enabling developers to handle gamepad connection events more conveniently through event handler attributes.

#### Technical Details

This feature extends the `WindowEventHandlers` interface mixin with two new event handler attributes:

- `window.ongamepadconnected`
- `document.body.ongamepadconnected`
- `window.ongamepaddisconnected`
- `document.body.ongamepaddisconnected`

These attributes provide a more concise syntax for registering gamepad connection event handlers, complementing the existing `addEventListener` approach. The implementation follows the standard event handler attribute pattern used throughout the web platform.

#### Use Cases

This feature simplifies gamepad event handling in web games and applications:

- **Simplified Event Registration**: Developers can use the concise `window.ongamepadconnected = handler` syntax instead of `window.addEventListener('gamepadconnected', handler)`
- **Controller Detection**: Games can immediately detect when players connect or disconnect their controllers and update UI accordingly
- **Dynamic Input Configuration**: Applications can dynamically reconfigure input handling when gamepads are connected or removed
- **Better User Experience**: Enables responsive UI updates that inform users about controller connectivity status

#### References

- [Tracking bug #40175074](https://issues.chromium.org/issues/40175074)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5109540852989952)
- [Spec](https://w3c.github.io/gamepad/#extensions-to-the-windoweventhandlers-interface-mixin)
