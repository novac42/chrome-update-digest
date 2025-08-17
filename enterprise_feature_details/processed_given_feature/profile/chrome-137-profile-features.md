# Chrome 137 Profile-Related Features Report

*Generated on: 2025-07-08 16:57:10*

## Summary

- **Total features analyzed**: 0
- **Profile-related features found**: 10
- **Keywords used**: `profile|Profile|account|Account|identity|Identity|sync|Sync|sign-in|signin|multiple.*account|separate.*profile|data.*separation`

## User productivity/Apps

### Multiple Identity Support on iOS

**Relevance Score**: 145.0

**Type**: Chrome Browser changes
**Platform**: Mobile (iOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, account, Identity, Multiple Identity Support on iOS Chrome on iOS is introducing support for multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts will continue to share a single profile.This change aims to improve Chrome's enterprise offering and provide a more secure and organized browsing experience, especially for end users with both personal and work accounts on their device. Users will experience a one-time onboarding flow when adding a managed account to the device. They will be able to switch between accounts by tapping on the account, separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts will continue to share a single profile, data separation

**Description**:
Chrome on iOS is introducing support for multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts will continue to share a single profile.This change aims to improve Chrome's enterprise offering and provide a more secure and organized browsing experience, especially for end users with both personal and work accounts on their device. Users will experience a one-time onboarding flow when adding a managed account to the device. They will be able to switch between accounts by tapping on the account particle disk on theNew tabpage.Admins who enabled Chrome policies on iOS (instructionshere) can continue to leverage existing policies.Chrome 138 on iOS

**Key Context**: counts, particularly for managed (work or school) accounts. This update introduces separate browser **profile**s for each managed account, ensuring strict data separation between work and personal browsing. Regu | Multiple Identity Support on iOS Chrome on iOS is introducing support for multiple **account**s, particularly for managed (work or school) **account**s. This update introduces separate browser profi | Multiple **Identity** Support on iOS Chrome on iOS is introducing support for multiple accounts, particularly for managed

### Customizing managed profiles with custom logo and label

**Relevance Score**: 90.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, Profile, account

**Description**:
Chrome 137 has a new toolbar and profile menu customizations that help users easily identify if their Chrome profile is managed, whether they're on a work or personal device. This is especially useful for BYOD scenarios where employees use their own devices with managed accounts.To help tailor this experience, we're adding three new policies:-EnterpriseCustomLabel: Customize the text displayed on the toolbar element to match your organization's branding.-EnterpriseLogoUrl: Add your company logo to the profile menu.-EnterpriseProfileBadgeToolbarSettings: This policy can disable the default label for a managed profile in the Chrome toolbar.In Chrome 134, these policies became available to customize the logo and label shown on a managed profile. Starting Chrome 137, there are updates to the default behavior of the profile label and icon overlaid on the account avatar. In Chrome 138, managed profiles will show aworkorschoollabel in addition to the profile disk. In the profile menu, there will be a building icon overlaid on the account avatar. The expanded profile disk can be disabled viaEnterpriseProfileBadgeToolbarSettings.Chrome 134 on LaCrOS, macOS, Windows: Policies to customize the toolbar label and icon (in profile menu).Chrome 136 on Linux, macOS, Windows: Rollout ofManaged by your organizationin profile menu . The logo can be customized viaEnterpriseLogoUrlpolicy.Chrome 137 on Linux, macOS, Windows:Rollout of defaultworkandschoollabels in Chrome toolbar. The label can be turned off viaEnterpriseProfileBadgeToolbarSettings.

**Key Context**: Customizing managed **profile**s with custom logo and label Chrome 137 has a new toolbar and **profile** menu customizations that help | Customizing managed **profile**s with custom logo and label Chrome 137 has a new toolbar and **profile** menu customizations that help | ce. This is especially useful for BYOD scenarios where employees use their own devices with managed **account**s.To help tailor this experience, we're adding three new policies:-EnterpriseCustomLabel: Customize

### New remote commands and CSV export for the Managed Profile list

**Relevance Score**: 80.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: Profile, profile

**Description**:
and CSV export for the Managed profiles listThe Admin console will support profile-level "Clear cache" and "Clear cookies" remote commands, and CSV export for the Managed Profiles list. You can select one or multiple profiles and perform a remote command.Chrome 137 on Android, Linux, macOS, Windows:Adding CSV export for Managed profiles. You can export the Managed profile data outside of the Admin console.Chrome 138 on Linux, macOS, Windows: Profile-level support for theClear cacheandClear cookiesremote commands. In the Managed profile list, you will be able to select one or multiple profiles and perform a remote command.

**Key Context**: New remote commands and CSV export for the Managed **Profile** list and CSV export for the Managed **profile**s listThe Admin console will support **profile**-level "Clea | New remote commands and CSV export for the Managed **Profile** list and CSV export for the Managed **profile**s listThe Admin console will support **profile**-level "Clea

### Inactive profile deletion in Chrome Enterprise Core

**Relevance Score**: 60.0

**Type**: Chrome Browser changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, account

**Description**:
In June 2025, the inactive period for profile deletion setting started to roll out. In July 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. When releasing the setting, the inactivity period of time has a default value of 90 days. Meaning that by default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value using this setting. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.If you lower the set value, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is re-activated on a device, that profile will reappear in the console.Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:Policy will roll out in June. Deletion will start in July and the initial wave of deletion will complete by the end of August. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

**Key Context**: Inactive **profile** deletion in Chrome Enterprise Core In June 2025, the inactive period for **profile** deletion setting s | y default, all managed profiles that have been inactive for more than 90 days are deleted from your **account**. Administrators can change the inactive period value using this setting. The maximum value to deter

### Bookmarks and reading list improvements on Chrome Desktop

**Relevance Score**: 35.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: Account, Sync, Signin

**Description**:
On Chrome 138 on Desktop, some users who sign in to Chrome upon saving a new bookmark can now use and save bookmarks and reading list items in their Google Account. Relevant enterprise policies controlling bookmarks, as well asBrowserSignin,SyncDisabledorSyncTypesListDisabled, will continue to work as before, so admins can configure whether users can use and save items in their Google Account. SettingEditBookmarksEnabledto false will also prevent users from uploading a bookmark saved on their device to their Google Account.Chrome 138 on Linux, macOS, Windows

**Key Context**: me upon saving a new bookmark can now use and save bookmarks and reading list items in their Google **Account**. Relevant enterprise policies controlling bookmarks, as well asBrowserSignin,SyncDisabledorSyncType | n their Google Account. Relevant enterprise policies controlling bookmarks, as well asBrowserSignin,**Sync**Disabledor**Sync**TypesListDisabled, will continue to work as before, so admins can configure whether us | items in their Google Account. Relevant enterprise policies controlling bookmarks, as well asBrowser**Signin**,SyncDisabledorSyncTypesListDisabled, will continue to work as before, so admins can configure wheth

### Chrome Enterprise Overview page

**Relevance Score**: 30.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS), Mobile (Android, iOS)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile

**Description**:
Chrome Browser Enterprise is introducing a newOverviewpage in the Chrome browser section of the Google Admin console. The Overview page allows IT administrators to quickly find key information about their deployment:- Active and inactive profiles and enrolled browsers- Identify browsers out-of-date and with pending updates- Identify high-risk extensions (according to Spin.AI) and get a preview of most requested extensionsThe Overview page also allows you to quickly access key actions, such as, managing extensions (block and allow) and accessing browser and profile lists.Chrome 137 on Android, iOS, Linux, macOS, Windows

**Key Context**: lows IT administrators to quickly find key information about their deployment:- Active and inactive **profile**s and enrolled browsers- Identify browsers out-of-date and with pending updates- Identify high-risk

### Happy Eyeballs V3

**Relevance Score**: 15.0

**Type**: Chrome Browser changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: sync

**Description**:
This launch is an internal optimization in Chrome that implements Happy Eyeballs V3 to achieve better network connection concurrency. Happy Eyeballs V3 performs DNS resolutions asynchronously and staggers connection attempts with preferable protocols (H3/H2/H1) and address families (IPv6/IPv4) to reduce user-visible network connection delay. This feature is gated by a temporary policyHappyEyeballsV3Enabled.Chrome 140 on Android, ChromeOS, Linux, macOS, Windows

**Key Context**: ls V3 to achieve better network connection concurrency. Happy Eyeballs V3 performs DNS resolutions a**sync**hronously and staggers connection attempts with preferable protocols (H3/H2/H1) and address families

## Security/Privacy

### Enhanced Safe Browsing as a synced setting

**Relevance Score**: 45.0

**Type**: Chrome Browser changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: account, sync

**Description**:
Chrome's Enhanced Safe Browsing is becoming a synced feature. This means that if a user opts into Enhanced Safe Browsing on one device, this protection level will automatically apply across all other devices where they are signed into Chrome with the same account. The goal is to provide stronger, more consistent security protection and a standardized user experience.Users who enable Enhanced Safe Browsing will benefit from its protections, for example, proactive phishing protection, improved detection of malware and malicious extensions) consistently across their synced Chrome instances on Desktop (Windows, macOS, Linux, ChromeOS), Android, and iOS. Users will be notified of this change via UI elements when their Enhanced Safe Browsing setting is synced.The Safe Browsing protection level is an existing feature, controlled by theSafeBrowsingProtectionLevelpolicy.Chrome 138 on Android, ChromeOS, Linux, macOS, Windows

**Key Context**: l will automatically apply across all other devices where they are signed into Chrome with the same **account**. The goal is to provide stronger, more consistent security protection and a standardized user exper | Enhanced Safe Browsing as a **sync**ed setting Chrome's Enhanced Safe Browsing is becoming a **sync**ed feature. This means that if a user o

### New policies in Chrome browser

**Relevance Score**: 30.0

**Type**: Chrome Browser changes
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: profile

**Description**:
PolicyDescriptionGeminiSettingsSettings for Gemini integrationAutofillPredictionSettingsSettings for Autofill with AIProvisionalNotificationsAllowedAllows the app to use provisional notification authorization on iOSRelaunchFastIfOutdatedRelaunch fast if outdatedUserSecurityAuthenticatedReportingEnable cloud reporting of security signals in managed profilesBuiltInAIAPIsEnabledAllow pages to use the built-in AI APIsOnSecurityEventEnterpriseConnectorConfiguration policy for the OnSecurityEvent Chrome Enterprise Connector (now available on iOS)UserSecuritySignalsReportingEnable cloud reporting of security signals in managed profiles
    |Policy|Description|
    |GeminiSettings|Settings for Gemini integration|
    |AutofillPredictionSettings|Settings for Autofill with AI|
    |ProvisionalNotificationsAllowed|Allows the app to use provisional notification authorization on iOS|
    |RelaunchFastIfOutdated|Relaunch fast if outdated|
    |UserSecurityAuthenticatedReporting|Enable cloud reporting of security signals in managed profiles|
    |BuiltInAIAPIsEnabled|Allow pages to use the built-in AI APIs|
    |OnSecurityEventEnterpriseConnector|Configuration policy for the OnSecurityEvent Chrome Enterprise Connector (now available on iOS)|
    |UserSecuritySignalsReporting|Enable cloud reporting of security signals in managed profiles|
    RelaunchFastIfOutdated
    OnSecurityEventEnterpriseConnector

**Key Context**: if outdatedUserSecurityAuthenticatedReportingEnable cloud reporting of security signals in managed **profile**sBuiltInAIAPIsEnabledAllow pages to use the built-in AI APIsOnSecurityEventEnterpriseConnectorConfig

### 2SV enforcement for admins

**Relevance Score**: 25.0

**Type**: Chrome Browser changes
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: account, identity

**Description**:
To better protect your organization’s information, Google will soon require all accounts with access to admin.google.com to have 2-Step Verification (2SV) enabled. As a Google Workspace administrator, you need to confirm your identity with 2SV, which requires your password plus something additional, such as your phone or a security key.The enforcement will be rolled out gradually over the coming months. You should enable 2SV for the admin accounts in your organization before Google enforces it. For more information, see thisHelp Center article.
    To better protect your organization’s information, Google will soon require all accounts with access to admin.google.com to have 2-Step Verification (2SV) enabled. As a Google Workspace administrator, you need to confirm your identity with 2SV, which requires your password plus something additional, such as your phone or a security key.
    The enforcement will be rolled out gradually over the coming months. You should enable 2SV for the admin accounts in your organization before Google enforces it. For more information, see thisHelp Center article.

**Key Context**: orcement for admins To better protect your organization’s information, Google will soon require all **account**s with access to admin.google.com to have 2-Step Verification (2SV) enabled. As a Google Workspace a | ve 2-Step Verification (2SV) enabled. As a Google Workspace administrator, you need to confirm your **identity** with 2SV, which requires your password plus something additional, such as your phone or a security

## Keyword Analysis

| Keyword | Frequency |
|---------|-----------|
| profile | 6 |
| account | 5 |
| Profile | 2 |
| sync | 2 |
| Identity | 1 |
| Multiple Identity Support on iOS Chrome on iOS is introducing support for multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts will continue to share a single profile.This change aims to improve Chrome's enterprise offering and provide a more secure and organized browsing experience, especially for end users with both personal and work accounts on their device. Users will experience a one-time onboarding flow when adding a managed account to the device. They will be able to switch between accounts by tapping on the account | 1 |
| separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts will continue to share a single profile | 1 |
| data separation | 1 |
| Account | 1 |
| Sync | 1 |
| Signin | 1 |
| identity | 1 |