## Performance

### Speculation rules: desktop "eager" eagerness improvements

On desktop, "eager" eagerness speculation rules prefetches and prerenders now trigger when users hover on a link for a shorter time than the "moderate" mouse hover time.

The previous behavior, of starting prefetch and prerenders as soon as possible, was the same as "immediate" eagerness. This new behavior is more useful as it better reflects the author's intent to be more eager than the "moderate" and less eager than "immediate".

[ChromeStatus.com entry](https://chromestatus.com/feature/5113430155591680) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#:~:text=early%20as%20possible.-,%22moderate%22,balance%20between%20%22eager%22%20and%20%22conservative%22.,-%22conservative%22)
