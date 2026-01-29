---
layout: default
title: Chrome 144 Origin Trials - English Digest
---

# Chrome 144 Origin Trials - English Digest

## Area Summary

Chrome 144 introduces two significant origin trials that advance different aspects of web platform capabilities. The Enhanced Canvas API TextMetrics feature brings sophisticated text manipulation capabilities to canvas-based applications, enabling precise text editing, selection handling, and glyph-level operations that were previously difficult or impossible to achieve. Context-aware media elements represent a fundamental shift in how web applications request media permissions, replacing JavaScript-triggered prompts with declarative, user-activated controls that provide clearer user intent signals and better recovery paths for previously denied permissions. Together, these features expand the canvas text editing ecosystem and modernize media permission workflows, addressing long-standing developer pain points.

## Detailed Updates

Chrome 144's origin trials focus on enhancing web application capabilities through improved text manipulation in canvas contexts and modernized permission models for media access.

### Enhanced Canvas API `TextMetrics`

#### What's New

The Canvas API `TextMetrics` interface has been significantly expanded to support selection rectangles, bounding box queries, and glyph cluster-based operations. This enhancement transforms the canvas into a more capable platform for complex text editing applications.

#### Technical Details

The expanded `TextMetrics` API provides developers with fine-grained access to text rendering details that enable accurate selection handling, precise caret positioning, and reliable hit testing. The cluster-based rendering capabilities work at the glyph level, allowing operations on individual character clusters rather than just strings of text. This granular control is essential for implementing sophisticated text editors and design tools in canvas contexts.

#### Use Cases

This feature enables a new generation of canvas-based text editing applications with capabilities that match native text editors. Developers can implement:
- Precise text selection with accurate visual feedback
- Caret positioning that respects complex scripts and ligatures
- Hit testing for determining which character the user clicked
- Advanced text effects such as independent character animations
- Per-character styling and manipulation for creative applications

The cluster-based operations are particularly valuable for applications requiring sophisticated text effects or working with complex scripts where individual glyphs don't map one-to-one with characters.

#### References

- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1646628613757337601)
- [Tracking bug #341213359](https://issues.chromium.org/issues/341213359)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5075532483657728)
- [Spec](https://github.com/whatwg/html/pull/11000)

### Context-aware media elements

#### What's New

Context-aware media elements introduce declarative, user-activated controls for accessing and interacting with media streams. This represents a fundamental shift from JavaScript-initiated permission prompts to browser-controlled UI elements that provide clearer signals of user intent.

#### Technical Details

Rather than triggering permission prompts directly from JavaScript, context-aware media elements embed a browser-controlled element in the page. When users click this element, it provides an unambiguous signal of intentional action, enabling better permission prompt UX. This approach evolved from the earlier generic `<permission>` element based on feedback from developers and browser vendors, resulting in capability-specific elements that offer more tailored and powerful developer experiences.

#### Use Cases

This feature addresses the long-standing problem of intrusive or confusing permission prompts by:
- Providing a declarative way to request media access that aligns with user expectations
- Enabling better recovery paths for users who previously denied permissions
- Reducing friction in the permission request flow through clearer user intent signals
- Offering more granular control over when and how permission prompts appear

The capability-specific design allows each element type to be optimized for its particular use case, whether accessing camera, microphone, or other media capabilities.

#### Developer Migration

Developers who participated in the earlier `<permission>` element origin trial should note that this feature represents an evolution of that concept. The shift to capability-specific elements provides better ergonomics and more targeted functionality for different media types.

#### References

- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3736298840857247745)
- [Tracking bug #443013457](https://issues.chromium.org/issues/443013457)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4926233538330624)
- [Spec](https://wicg.github.io/PEPC/permission-elements.html)
