## JavaScript

### Align implementations on when RTP stats should be created

RTP stats objects, of type "outbound-rtp" or "inbound-rtp" in this case, represents a WebRTC stream. The identifier of this stream is the SSRC (a number). This feature aligns with the specification on when these stats should be created.

[Tracking bug #406585888](https://issues.chromium.org/issues/406585888) | [ChromeStatus.com entry](https://chromestatus.com/feature/4580748730040320) | [Spec](https://w3c.github.io/webrtc-stats/#the-rtp-statistics-hierarchy)
