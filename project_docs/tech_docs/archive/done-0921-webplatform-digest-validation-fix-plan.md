# 0921 WebPlatform Digest Validation Fix Plan

## Context
Repeated fallback digests were generated for Chrome 136 WebPlatform areas because the validator could not detect features produced by the LLM. The prompts instruct the model to emit feature sections as H3 headings with optional H4/H5 subheadings, but the validator only recognizes H3 titles and expects exact string matches.

## Goals
- Restore successful English digest generation for all areas without manual fallbacks.
- Preserve guardrails against hallucinated content and incorrect links.
- Maintain prompt/validator alignment going forward.

## Root Cause
1. `_validate_digest` searches for feature headings using a regex that only captures H3 titles, while the prompt allowed the LLM to emit features at H4 level. As a result, every feature was treated as missing.
2. Title comparison is case- and punctuation-sensitive, so even near-identical headings were flagged as missing.

## Workstream Breakdown
1. **Prompt Alignment**
   - Update both EN and ZH area prompts to explicitly require `### [Feature Title]` for each feature.
   - Clarify that deeper headings (`####` / `#####`) belong inside the feature block for supporting details.
   - Run a smoke test generation for one area to confirm structure.

2. **Validator Resilience**
   - Broaden `_validate_digest` to:
     - Accept H3 titles by default and, if no matches are found, treat H4 titles as a fallback.
     - Normalize feature titles (trim, lowercase, collapse whitespace, standardize punctuation) before set comparison.
   - Keep the unknown-link threshold at `<= 2` unless prompted by stakeholders.
   - Add inline comments describing the heading expectations to avoid future drift.

3. **Translation Guardrail Check**
   - Confirm the Chinese translation prompt mirrors the H3 requirement so the validator sees consistent structure post-translation.
   - Ensure translation validation still compares heading counts correctly after the prompt update.

4. **Regression Coverage**
   - Introduce a lightweight unit test for `_validate_digest` that covers:
     - H3 detection with normalized titles.
     - H4 fallback behavior.
     - Rejection of extra unknown links.
   - Add a fixture representing the Chrome 136 security/privacy YAML for deterministic testing.

## Timeline (Target)
- Prompt updates & quick manual validation: Day 0
- Validator normalization & tests: Day 1
- Full regeneration of Chrome 136 digests: Day 2

## Risks & Mitigations
- **Prompt drift in future releases**: Document heading expectations in both prompt files and validator comments; add test coverage.
- **Over-normalizing titles**: Limit normalization to lowercase, trimmed text, and replace smart quotes to avoid merging distinct features.
- **Potential hidden prompt copies**: Search for alternate prompt variants to keep them consistent with the new heading rule.

## Owners
- Prompt updates: Content tooling team (Alice Chen)
- Validator & tests: Platform automation team (Leo Zhang)

## Success Metrics
- 0 fallback digests for Chrome 136 after regeneration.
- Validator unit tests passing in CI.
- Manual spot check confirms headings and links align with YAML data.
