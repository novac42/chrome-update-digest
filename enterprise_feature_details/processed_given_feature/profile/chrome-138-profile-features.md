# Chrome 138 Profile-Related Features Report

*Generated on: 2025-07-08 16:57:54*

## Summary

- **Total features analyzed**: 0
- **Profile-related features found**: 7
- **Keywords used**: `profile|Profile|account|Account|identity|Identity|sync|Sync|sign-in|signin|multiple.*account|separate.*profile|data.*separation`

## User productivity/Apps

### History sync opt-in using the profile pill

**Relevance Score**: 145.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, sync, Sync, sign-in, separate from the sign-in flow. For Enterprise users, the expanded profile

**Description**:
In Chrome 138, some signed-in users see a new option to opt in to history and tab sync. This change is designed to offer the benefits of history sync in a non-disruptive way by using the profile pill to display a short in-line message. Users who click on the profile pill are taken to their profile menu where they can choose to turn on sync. The goal is to provide users with an intuitive and contextually relevant entry point for syncing data like browsing history, separate from the sign-in flow. For Enterprise users, the expanded profile pill only appears after 4 hours of browser inactivity.
    Relevant enterprise policies controlling History or Tab sync ([SyncDisabled](https://chromeenterprise.google/policies/#SyncDisabled), [SyncTypesListDisabled](https://chromeenterprise.google/policies/#SyncTypesListDisabled) and [SavingBrowserHistoryDisabled](https://chromeenterprise.google/policies/#SavingBrowserHistoryDisabled)) continue to work as before.
    - **Chrome 138 on Linux, macOS, Windows:** Feature starts gradual rollout.

**Key Context**: History sync opt-in using the **profile** pill In Chrome 138, some signed-in users see a new option to opt in to history and tab sync. This c | History **sync** opt-in using the profile pill In Chrome 138, some signed-in users see a new option to opt in to his | History **sync** opt-in using the profile pill In Chrome 138, some signed-in users see a new option to opt in to his

### Multiple identity support on iOS

**Relevance Score**: 145.0

**Type**: Chrome Enterprise Core changes
**Platform**: Mobile (iOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, account, identity, Multiple identity support on iOS Chrome on iOS now supports multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular account, separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts continue to share a single profile, data separation

**Description**:
Chrome on iOS now supports multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts continue to share a single profile.
    This change aims to improve Chrome's enterprise offering and provide a more secure and organized browsing experience, especially for end users with both personal and work accounts on their device. Users experience a one-time onboarding flow when adding a managed account to the device. They can switch between accounts by tapping on the account particle disk on the **New tab** page.
    Admins who enabled Chrome policies on iOS ([see instructions](https://support.google.com/chrome/a/answer/6304822)) can continue to use existing policies.
    - **Chrome 138 on iOS**

**Key Context**: counts, particularly for managed (work or school) accounts. This update introduces separate browser **profile**s for each managed account, ensuring strict data separation between work and personal browsing. Regu | Multiple identity support on iOS Chrome on iOS now supports multiple **account**s, particularly for managed (work or school) **account**s. This update introduces separate browser profi | Multiple **identity** support on iOS Chrome on iOS now supports multiple accounts, particularly for managed (work or scho

## Security/Privacy

### Enhanced Safe Browsing is a synced setting

**Relevance Score**: 45.0

**Type**: Chrome Browser changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: account, sync

**Description**:
In Chrome 138, Chrome's Enhanced Safe Browsing is a synced feature. This means that if a user opts into Enhanced Safe Browsing on one device, this protection level automatically applies across all other devices where they are signed into Chrome with the same account. The goal is to provide stronger, more consistent security protection and a standardized user experience.
    Users who enable Enhanced Safe Browsing benefit from its protections, for example, proactive phishing protection, improved detection of malware and malicious extensions consistently across their synced Chrome instances on Desktop (Windows, macOS, Linux, ChromeOS), Android, and iOS. Users receive onscreen notifications when their Enhanced Safe Browsing setting is synced.
    The Safe Browsing protection level is an existing feature, controlled by the [SafeBrowsingProtectionLevel](https://chromeenterprise.google/policies/#SafeBrowsingProtectionLevel) policy.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows**

**Key Context**: evel automatically applies across all other devices where they are signed into Chrome with the same **account**. The goal is to provide stronger, more consistent security protection and a standardized user exper | Enhanced Safe Browsing is a **sync**ed setting In Chrome 138, Chrome's Enhanced Safe Browsing is a **sync**ed feature. This means that if a

### Bookmarks and reading list improvements on Chrome Desktop

**Relevance Score**: 35.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS)
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: Account, Sync, Signin

**Description**:
For Chrome 138 on Desktop, some users who sign in to Chrome upon saving a new bookmark can now use and save bookmarks and reading list items in their Google Account. Relevant enterprise policies controlling bookmarks, as well as [BrowserSignin](https://chromeenterprise.google/policies/#BrowserSignin), [SyncDisabled](https://chromeenterprise.google/policies/#SyncDisabled) or [SyncTypesListDisabled](https://chromeenterprise.google/policies/#SyncTypesListDisabled), continue to work as before, so admins can configure whether or not users can use and save items in their Google Account. Setting [EditBookmarksEnabled](https://chromeenterprise.google/policies/#EditBookmarksEnabled) to false also prevents users from uploading a bookmark saved on their device to their Google Account.
    - **Chrome 138 on Linux, macOS, Windows**

**Key Context**: me upon saving a new bookmark can now use and save bookmarks and reading list items in their Google **Account**. Relevant enterprise policies controlling bookmarks, as well as [BrowserSignin](https://chromeenter | ng bookmarks, as well as [BrowserSignin](https://chromeenterprise.google/policies/#BrowserSignin), [**Sync**Disabled](https://chromeenterprise.google/policies/#**Sync**Disabled) or [**Sync**TypesListDisabled](https:/ | ems in their Google Account. Relevant enterprise policies controlling bookmarks, as well as [Browser**Signin**](https://chromeenterprise.google/policies/#Browser**Signin**), [SyncDisabled](https://chromeenterprise.

### Deprecate asynchronous range removal for Media Source extensions

**Relevance Score**: 35.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: sync

**Description**:
The [Media Source standard](https://www.w3.org/TR/media-source-2/) changed in the past to disallow ambiguously-defined behavior involving asynchronous range removals:
    - `SourceBuffer.abort()` no longer aborts `SourceBuffer.remove()` operations
    - Setting `MediaSource.duration` can no longer truncate currently buffered media
    Exceptions are thrown in both of these cases now. Safari and Firefox have long shipped this behavior; Chromium is the last browser remaining with the old behavior. Use counters show ~0.001%-0.005% of page loads hit the deprecated behavior. If a site hits this issue, playback may now break. Usage of abort() cancelling removals is increasing, so it's prudent to resolve this deprecation before more incompatible usage appears.
    - **Chrome 138 on Windows, macOS, Linux, Android**

**Key Context**: Deprecate a**sync**hronous range removal for Media Source extensions The [Media Source standard](https://www.w3.org/TR/

## Management

### Inactive profile deletion in Chrome Enterprise Core

**Relevance Score**: 70.0

**Type**: Chrome Enterprise Core changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: Management
**Matched Keywords**: profile, account

**Description**:
In June 2025, the inactive period for profile deletion setting started to roll out. In July 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. The inactivity period of time has a default value of 90 days. By default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value using this setting. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.
    If you lower the set value, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is re-activated on a device, that profile will reappear in the console.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:** Policy will roll out in June. Deletion will start in July and the initial wave of deletion will complete by the end of August. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

**Key Context**: Inactive **profile** deletion in Chrome Enterprise Core In June 2025, the inactive period for **profile** deletion setting s | y default, all managed profiles that have been inactive for more than 90 days are deleted from your **account**. Administrators can change the inactive period value using this setting. The maximum value to deter

### URL Filtering capabilities on iOS

**Relevance Score**: 40.0

**Type**: Chrome Enterprise Premium changes
**Platform**: Mobile (iOS)
**Status**: Current
**Categories**: Management
**Matched Keywords**: profile

**Description**:
The current WebProtect URL Filtering capabilities on Desktop are being extended to mobile so that organizations can audit, warn, or block certain URLs or categories of URLs from loading on managed Chrome browsers or managed user profiles on mobile devices. This feature is part of Chrome Enterprise Premium and aims to provide secure and safe internet access for enterprise users on any device. Admins can create URL filtering rules to ensure that employees can only access safe and authorized URLs on iOS devices. Chrome reports URL filtering events and unsafe site events via the Reporting Connector on mobile. This feature allows administrators to manage which URLs can be accessed on managed Chrome browsers or profiles on company-owned or BYOD iOS devices.
    Key changes include:
    - Admins can block, warn, or audit users when accessing certain sites or categories.
    - Users see interstitial pages when attempting to visit blocked or warned URLs.
    - Chrome reports URL filtering events.
    - Updates to the `chrome://management` page reflect the new functionality.
    - **Chrome 138 on iOS:** The URL Filtering feature becomes available on iOS.

**Key Context**: or block certain URLs or categories of URLs from loading on managed Chrome browsers or managed user **profile**s on mobile devices. This feature is part of Chrome Enterprise Premium and aims to provide secure an

## Keyword Analysis

| Keyword | Frequency |
|---------|-----------|
| profile | 4 |
| sync | 3 |
| account | 3 |
| Sync | 2 |
| sign-in | 1 |
| separate from the sign-in flow. For Enterprise users, the expanded profile | 1 |
| identity | 1 |
| Multiple identity support on iOS Chrome on iOS now supports multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular account | 1 |
| separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts continue to share a single profile | 1 |
| data separation | 1 |
| Account | 1 |
| Signin | 1 |