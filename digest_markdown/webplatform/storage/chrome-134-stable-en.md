digest_markdown/webplatform/storage/chrome-134-stable-en.md

# Area Summary

Chrome 134 advances Shared Storage with focused enhancements around observability, contribution control, and concurrency safety. Key changes add an interestGroups() accessor to the Shared Storage worklet, permit per-context contribution limits via a new maxContributions field for Private Aggregation, and integrate the Web Locks API into Shared Storage worklets. Together these updates improve measurement accuracy, give callers finer control over aggregation behavior, and reduce race-condition–driven duplicate reporting—important for developers implementing secure, reliable cross-site measurement and storage-backed logic.

## Detailed Updates

The items below expand on the summary, highlighting what changed, how it works at a high level, and practical developer uses.

### Allow reading interest groups in Shared Storage Worklet

#### What's New
Adds an `interestGroups()` method to the Shared Storage worklet that returns the Protected Audience interest groups associated with the shared storage origin's owner, including some additional metadata.

#### Technical Details
Exposes a worklet-level API method that enumerates Protected Audience interest groups for the shared storage origin. This is surfaced in the Shared Storage worklet execution context (JavaScript/webapi surface).

#### Use Cases
Gives Protected Audience buyers and measurement integrations better visibility into interest-group state for debugging, attribution, and validation of shared-storage-driven logic while operating within the worklet environment.

#### References
https://chromestatus.com/feature/5074536530444288

### Private Aggregation API: per-context contribution limits for Shared Storage callers

#### What's New
Enables Shared Storage callers to customize the number of contributions per Private Aggregation report via a new `maxContributions` field.

#### Technical Details
Callers can set `maxContributions` to override the default contribution count for a given context when producing Private Aggregation reports. This is a webapi-facing configuration knob defined in the Private Aggregation API draft linked below.

#### Use Cases
Useful for developers and measurement systems that need to control aggregation granularity or limit per-context report size to balance privacy, payload size, and downstream processing.

#### References
https://issues.chromium.org/issues/376707230
https://chromestatus.com/feature/5189366316793856
https://github.com/patcg-individual-drafts/private-aggregation-api/pull/164/files

### Support Web Locks API in Shared Storage

#### What's New
Integrates the Web Locks API into Shared Storage worklets to prevent race conditions (for example, duplicate reporting in cross-site reach measurement caused by concurrent `get()`/`set()` flows).

#### Technical Details
Introduces `navigator.locks.request` availability inside the Shared Storage worklet execution environment so worklet code can obtain locks and serialize critical sections of `get()`/`set()` logic to avoid duplication or inconsistent state.

#### Use Cases
Helps measurement and storage-heavy workloads that require coordinated updates across concurrent tasks—improving correctness and reducing the need for ad-hoc locking patterns at the application layer.

#### References
https://issues.chromium.org/issues/373899210
https://chromestatus.com/feature/5133950203461632

File saved to: digest_markdown/webplatform/storage/chrome-134-stable-en.md