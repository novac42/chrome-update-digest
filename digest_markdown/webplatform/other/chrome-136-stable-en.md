Area Summary

Chrome 136 (stable) introduces a user-facing improvement in the "other" category: direct context-menu actions for WebGPU canvases to save or copy rendered images. This small but practical change makes it easier for developers and users to capture GPU-rendered output without instrumenting pages or using external tooling. It advances the web platform by aligning WebGPU canvases with existing canvas UX (right-click Save/Copy), reducing friction for debugging, asset capture, and content workflows. These updates matter because they streamline developer iteration and user-facing content export for GPU-driven graphics on the web.

## Detailed Updates

Below are the detailed notes for the change summarized above and its implications for development workflows.

### Save and copy canvas images

#### What's New
Chrome users can now right-click on a WebGPU canvas and access context menu options "Save Image As…" or "Copy Image."

#### Technical Details
This feature exposes Save/Copy image actions from the browser context menu for canvases backed by WebGPU rendering. The change is tracked in the Chromium issue referenced below.

#### Use Cases
- Quick capture of a WebGPU-rendered frame for debugging or visual regression checks.
- Convenience for designers and testers to export renders without adding page-level image export code.
- Simplifies sharing snapshots of GPU-generated visuals during development reviews.

Relevance to area-specific concerns:
- graphics-webgpu: Directly benefits workflows around GPU rendering by easing capture of canvas output.
- webapi: Improves the end-user experience for canvas elements using WebGPU without requiring API changes.
- performance & debugging: Low-effort capture aids performance analysis and visual debugging workflows.
- multimedia & developer tooling: Facilitates asset extraction for documentation and testing.

#### References
- https://issues.chromium.org/issues/40902474

Saved to: digest_markdown/webplatform/other/chrome-136-stable-en.md