## CSS

### Custom property enumeration in `getComputedStyle()`

When iterating over `window.getComputedStyle(element)` in Chrome, there was a bug where it forgets to include any custom properties set on the element. Therefore, `length()` on the returned object forgets to account for the number of custom properties set. This bug is fixed from Chrome 141, aligning Chrome with Firefox and Safari.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070655645155328) | [Spec](https://drafts.csswg.org/cssom/#dom-window-getcomputedstyle)
