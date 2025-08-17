# Chrome Enterprise Release Notes (Chrome 139)

Source: https://support.google.com/chrome/a/answer/7679408

Skip to main content
[][1]
[Chrome Enterprise and Education Help][2]
[][3]
[Sign in][4]
[][1]
[Google Help][5]
[
  * Help Center
][6][
  * Community
][7][
  * Chrome Enterprise and Education
][8]
[
  * Privacy Policy
][9][
  * Terms of Service
][10]
  * Submit feedback

Send feedback on...
This help content & information
General Help Center experience
Next
  * [Help Center][6]
  * [Community][7]
  * 

[Chrome Enterprise and Education][8]
# Chrome Enterprise and Education release notes
Last updated on: July 30, 2025 
 _For administrators who manage Chrome browser or ChromeOS devices for a business or school._
Select the required tab to see Chrome browser or ChromeOS updates.
  * Chrome browser updates published on [Chrome browser Early Stable Release][11].
  * ChromeOS updates are published one week before [ChromeOS Stable Release][11].

## Chrome 139 release summary
Chrome browser changes | Security/ Privacy | User productivity/ Apps | Management  
---|---|---|---  
[AI Mode for search recommendations in Chrome][12] |  | ✓ |   
[Admin-configurable site search][13] |  | ✓ | ✓  
[Chrome on Android no longer supports Android Oreo or Android Pie][14] |  |  | ✓  
[Malicious APK download checks][15] | ✓ |  |   
[Migrate extensions to Manifest V3 before June 2025][16] | ✓ | ✓ | ✓  
[New tab page footer][17] | ✓ | ✓ | ✓  
[Prevent accidental password deletions on Chrome][18] | ✓ |  |   
[Promotional notifications][19] |  |  | ✓  
[Remove risky extension flags in Chrome][20] | ✓ |  |   
[Remove SwiftShader fallback][21] | ✓ |  |   
[Shared tab groups][22] |  | ✓ |   
[Support accounts in pending state on Chrome iOS][23] | ✓ |  |   
[Upcoming change for CA certificates included in the Chrome Root Store][24] | ✓ |  |   
[Stop sending Purpose: prefetch header from prefetches and prerenders][25] | ✓ |  | ✓  
[Chrome removes support for macOS 11][26] |  |  | ✓  
[Fire error event instead of throwing exception for CSP blocked worker][27] |  |  | ✓  
[Randomizing TCP port allocation on Windows][28] |  |  | ✓  
[New policies in Chrome browser][29] |  |  | ✓  
[Removed policies in Chrome browser][30] |  |  | ✓  
Chrome Enterprise Core changes | Security/ Privacy | User productivity/ Apps | Management  
[Group based policies for connector configuration selection][31] |  |  | ✓  
[New remote commands and CSV export for the Managed Profile List][32] |  |  | ✓  
[New tab page cards for Microsoft 365][33] |  | ✓ | ✓  
[Regionalize covered Chrome Enterprise data][34] |  |  | ✓  
Chrome Enterprise Premium changes | Security/ Privacy | User productivity/ Apps | Management  
[Active account detection][35] | ✓ |  | ✓  
[Chrome Enterprise Connectors API][36] | ✓ |  | ✓  
[Copy and paste rules protection][37] | ✓ |  | ✓  
[Data Loss Prevention support for iFrames][38] | ✓ |  | ✓  
[Enable watermarking on Single Page Applications][39] | ✓ |  | ✓  
Upcoming Chrome browser changes | Security/ Privacy | User productivity/ Apps | Management  
[2SV enforcement for admins][40] |  |  | ✓  
[Automated password change][41] | ✓ |  |   
[Contextual search suggestions in Chrome address bar][42] |  | ✓ |   
[Enhanced autofill][43] |  | ✓ |   
[Gemini in Chrome][44] |  | ✓ |   
[Happy Eyeballs V3][45] | ✓ |  | ✓  
[Launch Chrome into new profile from command line][46] | ✓ |  | ✓  
[PostQuantum cryptography for DTLS in WebRTC][47] | ✓ |  |   
[ServiceWorkerAutoPreload][48] |  |  | ✓  
[CSS find-in-page highlight pseudos][49] |  | ✓ | ✓  
[Deprecate special font size rules for H1 within some elements][50] |  |  | ✓  
[IP protection][51] | ✓ |  | ✓  
[Local network access restrictions][52] | ✓ |  | ✓  
[Probabilistic reveal tokens][53] | ✓ |  | ✓  
[Propagate Viewport overscroll-behavior from Root][54] | ✓ |  | ✓  
[Script blocking in Incognito][55] | ✓ |  | ✓  
[SharedWorker script inherit controller for blob script URL][56] |  |  | ✓  
[Strict Same Origin Policy for Storage Access API][57] | ✓ |  |   
[Web App Manifest: specify update eligibility, icon urls are Cache-Control: immutable][58] |  |  | ✓  
[Clear window name for cross-site navigations that switches browsing context group][59] | ✓ |  |   
[Disallow non-trustworthy plaintext HTTP prerendering][60] | ✓ |  |   
[HSTS tracking prevention][61] | ✓ |  |   
[Disallow spaces in non-file:// URL hosts][62] |  |  | ✓  
[Remove third-party storage partitioning policies][63] | ✓ |  |   
[SafeBrowsing API v4 → v5 migration][64] | ✓ |  |   
[Isolated Web Apps][65] |  |  | ✓  
[UI Automation accessibility framework provider on Windows][66] |  | ✓ |   
Upcoming Chrome Enterprise Core changes | Security/ Privacy | User productivity/ Apps | Management  
[Inactive profile deletion in Chrome Enterprise Core][67] | ✓ |  | ✓  
[Chrome Enterprise Overview page][68] |  |  | ✓  
Upcoming Chrome Enterprise Premium changes | Security/ Privacy | User productivity/ Apps | Management  
[Increased file size support for Data Loss Prevention scans][69] | ✓ |  | ✓  
[Watermarking customization][70] | ✓ |  | ✓  
[Chrome browser rule UX refactor][71] | ✓ |  | ✓  
[DOWNLOAD Release notes (PDF)][72]
↑ back to top
The enterprise release notes are available in 9 languages. You can read about Chrome's updates in English, German, French, Dutch, Spanish, Portuguese, Korean, Indonesian, and Japanese. Allow 1 to 2 weeks for translation for some languages.
Chrome Enterprise and Education release notes are published in line with the [Chrome release schedule][11], on the Early Stable date for Chrome browser.
## Chrome browser changes 
  * **AI Mode for search recommendations in Chrome**![back to top][73]
AI Mode is a feature that helps users dive deeper into topics they care about by showing AI Mode for search recommendations in Chrome. A new policy, [_AIModeSettings_][74], is available to control search recommendations in the address bar and **New tab** page search box. This policy also controls AI Mode recommendations in the address bar and the new tab page omnibox.
    * Chrome 138 on ChromeOS, Linux, macOS, Windows: AI Mode recommendations starts rolling out in the address bar and the new tab page search box. The AI Mode entry point is also rolled out in the new tab page search box.
    * **Chrome 139**
      * **on Windows, macOS, Linux and ChromeOS:** The AI Mode entrypoint button in the address bar begins rollout. AI Mode inline compose box in new tab page omnibox begins rollout. 
      * **on Android, iOS:** The**** AI Mode entrypoint in the new tab page omnibox begins to roll out. And for iOS **** the AI Mode recommendations starts rollout in the address bar as well. 
![][75]
![][76]
![][77]

  * **Admin-configurable site search**![back to top][73]
Site search shortcuts are a way to use the address bar (omnibox) as a search box for a specific site without navigating directly to the site’s URL, similar to how you can use the omnibox to perform a broad Google search of the web. Administrators can now create site shortcuts for users to shortcut to the most critical enterprise sites. Users can initiate a search by typing the shortcut or @shortcut (for example, @work), followed by Space or Tab, in the address bar.
Admins control these shortcut settings using the [_SiteSearchSettings_][78] policy.
    * Chrome 128 on ChromeOS, Linux, macOS, Windows: Gradual rollout
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows** : Adding an additional policy parameter allowing admins to specify **Allow user override** , which allows users to edit, disable, or delete admin-set shortcuts
![][79]
![Chrome Web Store][80]

  * **Chrome on Android no longer supports Android Oreo or Android Pie**![back to top][73]
The last version of Chrome that supports Android Oreo or Android Pie is Chrome 138, and it includes a message to affected users informing them to upgrade their operating system. Chrome 139 and later versions will not be supported on, nor shipped or available to, users running Android Oreo or Android Pie.
    * **Chrome 139 on Android:** Chrome on Android no longer supports Android Oreo or Android Pie.

  * **Malicious APK download checks**![back to top][73]
Chrome on Android now contacts Google servers about Android Package Kit (APK) files downloaded in Chrome, to get a verdict about their safety. If a downloaded APK file is determined to be dangerous, Chrome shows a warning and blocks the download, to protect users against mobile malware. Such download warnings are bypassable by the user through the Chrome UI. These malicious APK download checks are performed for users enrolled in Standard Protection or Enhanced Protection from Google Safe Browsing. This feature can be disabled by setting the Safe Browsing mode to _No Protection_ using the [_SafeBrowsingProtectionLevel_][81] policy.
    * **Chrome 139 on Android**
![Chrome Web Store][82]

  * **Migrate extensions to Manifest V3 before June 2025**![back to top][73]
Extensions must be updated to use Manifest V3. Chrome extensions are transitioning to a new manifest version, Manifest V3. This brings improved privacy for your users—for example, by moving to a model where extensions modify requests declaratively, without the ability to see individual requests. This also improves extension security, as remotely-hosted code is disallowed on Manifest V3. 
Beginning June 2024, Chrome gradually disables Manifest V2 extensions running in the browser. An enterprise policy - [_ExtensionManifestV2Availability_][83] \- can be used to test Manifest V3 in your organization ahead of the migration. Additionally, machines on which the policy is enabled are not subject to the disabling of Manifest V2 extensions until June 2025 - at which point the policy is to be removed.
You can see which Manifest version is being used by all Chrome extensions running on your fleet using the **Apps & extensions** usage page in Chrome Enterprise Core. 
    * Chrome 127 on ChromeOS, LaCrOS, Linux, macOS, Windows: Chrome will gradually disable Manifest V2 extensions on user devices. Only those with the [_ExtensionManifestV2Availability_][83] enterprise policy enabled would be able to continue using Manifest V2 extensions in their organization.
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows:** Remove [_ExtensionManifestV2Availability_][83] policy.

  * **New tab page footer**![back to top][73]
An update to the **New tab** page includes a new footer designed to provide users with greater transparency and control over their Chrome experience.
    * Chrome 138 on ChromeOS, Linux, macOS, Windows:**** Extension Attribution will begin to show on the NTP. If an extension has changed your default **New tab** page, you'll now see a message in the footer that attributes the change to that specific extension. This message often includes a link directly to the extension in the Chrome Web Store, making it easier to identify and manage unwanted extensions. If you're an administrator, you can disable this attribution using the [_NTPFooterExtensionAttributionEnabled_][84] policy.
    * **Chrome 139 on Linux, macOS, Windows** : Browser management disclosure will be shown if one of the policies to customize the footer is set by an enterprise admin. For users whose Chrome browser is managed by a trusted source, the **New tab** page footer will now display a management disclosure notice. This helps you understand how your browser is being managed. Administrators can disable this notice with the [_NTPFooterManagementNoticeEnabled_][85] policy. Additionally, organizations can customize the footer's appearance using the [_EnterpriseLogoUrlForBrowser_][86] and [_EnterpriseCustomLabelForBrowser_][87] policies to display a custom logo and label.
    * Chrome 140 on Linux, macOS, Windows: A default notice (_Managed by <domain name>_) will start to be shown in the **New tab** page footer for all managed browsers. Visibility can be changed with the [_NTPFooterManagementNoticeEnabled_][85] policy. 
![Chrome Web Store][88]

  * **Prevent accidental password deletions on Chrome**![back to top][73]
To reduce the risk of accidental deletion of passwords on [_Delete browsing data_][89], Chrome 139 now points users to Google Password Manager settings, where they can better manage and delete passwords and passkeys. The feature removes the **Passwords and other sign-in data** selection in![More][90] ![and then][91] **Delete browsing data** and instead directs users to Google Password Manager where they can delete individually or in bulk.
This feature does not impact the existing enterprise policies [_ClearBrowsingDataOnExitList_][92] and [_BrowsingDataLifetime_][93]**.**
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows:** Feature will gradually roll out 
![Chrome Web Store][94]

  * **Promotional notifications**![back to top][73]
In Chrome 128, new promotional OS-level notifications began to be shown to users. These notifications are governed by the [_PromotionsEnabled_][95] enterprise policy.
    * Chrome 128 on ChromeOS, Linux, macOS, Windows
    * **Chrome 139 on Windows:** In Chrome 138, promotional notifications were only activated on Chrome clients when upgrading from Windows 10 to Windows 11. From Chrome 139, this is being extended to all Windows Chrome installations. Notifications will still be only shown to a subset of low-engaged users, and these can be disabled through the [_PromotionsEnabled_][95] enterprise policy.

  * **Remove risky extension flags in Google Chrome**![back to top][73]
To enhance the security and stability of the Chrome browser for our users, official Chrome branded builds will be removing `--extensions-on-chrome-urls` and `--disable-extensions-except` command-line flags starting in Chrome 139. This change aims to mitigate the risks associated with harmful and unwanted extensions. 
Developers can still use the both flags in non-branded builds such as [_Chromium and Chrome For Testing_][96]**.**
    * **Chrome 139 on Linux, macOS, Windows**

  * **Remove SwiftShader fallback**![back to top][73]
Allowing automatic fallback to [_WebGL_][97] backed by [_SwiftShader_][98] is deprecated and WebGL context creation now fails instead of falling back to SwiftShader. This was done for two primary reasons: 
    1. SwiftShader is a high security risk due to JIT-ed code running in Chromium's GPU process.
    2. Users have a poor experience when falling back from a high-performance GPU-backed WebGL to a CPU-backed implementation. Users have no control over this behavior and it is difficult to describe in bug reports.
SwiftShader is a useful tool for web developers to test their sites on systems that are headless or do not have a supported GPU. This use case will still be supported by opting in but is not intended for running untrusted content. To opt in to lower security guarantees and allow SwiftShader for WebGL, run the chrome executable with the `--enable-unsafe-swiftshader` command-line switch.
During the deprecation period, a warning will appear in the javascript console when a WebGL context is created and backed with SwiftShader. Passing `--enable-unsafe-swiftshader `will remove this warning message.
Chromium and other browsers do not guarantee WebGL availability. It is important to test and handle WebGL context creation failure and fall back to other web APIs such as Canvas2D or an appropriate message to the user. 
    * **Chrome 139**
      * **on Linux, macOS:** Swiftshader will be disabled on macOS and Linux. Users on machines without a GPU will not be able to use WebGL.
      * **On Windows:** The fallback to Swiftshader after three out-of-memory (OOM) errors will be disabled on Windows. Swiftshader usage will be limited to devices without a GPU or those with a GPU on the blocklist. 

  * **Shared tab groups**![back to top][73]
Users can now collaborate on tabs using the shared tab groups feature. With this feature, users can create and use a set of tabs on their desktop or mobile device and their collaborative partners can browse the same tabs on their devices. When one person changes a tab in the group, the changes are reflected across all users’ browsers in the group. An enterprise policy, **TabGroupSharingSettings** , will be available in Chrome 140 to control this feature.
    * Chrome 138 on Android, ChromeOS, Linux, macOS, Windows: Rollout of the ability to join and use a shared tab group. Users on Stable Chrome will not be able to create a shared tab group (the entry point will not be available) - this part of the feature will only be available on Beta/Dev/Canary for this phase of rollout. 
    * **Chrome 139 on iOS:** As early as Chrome 139, support for iOS will rollout
    * Chrome 140 on Android, iOS, ChromeOS, Linux, macOS, Windows: **TabGroupSharingSettings** Enterprise policy will be available to the enterprise owner in the admin console.

  * **Support accounts in pending state on Chrome iOS**![back to top][73]
Accounts whose credentials somehow became invalid are no longer automatically signed out and removed from Chrome on iOS. Instead, these accounts stay signed in to the browser, in a newly introduced _pending state_ associated with a persistent error indication in the UI so users are encouraged to resolve it. This also means that local data associated with these accounts are no longer automatically deleted, but instead kept on disk. Existing policies controlling sign-in (for example, [_BrowserSignin_][99]) continue to work as before.
    * **Chrome 139 on iOS:** Feature will gradually roll out 

  * **Upcoming change for CA certificates included in the Chrome Root Store**![back to top][73]
In response to sustained compliance failures, Chrome 139 changes how publicly-trusted TLS server authentication, that is, websites or certificates issued by Chunghwa Telecom and Netlock, are trusted by default. This applies to Chrome 139 and later on Windows, macOS, ChromeOS, Android, and Linux; iOS policies do not allow use of the Chrome Root Store in Chrome for iOS.
Specifically, TLS certificates validating to the Chunghwa Telecom or Netlock root CA certificates included in the Chrome Root Store and issued:
\- after July 31, 2025, will no longer be trusted by default.
\- on or before July 31, 2025, will be unaffected by this change. 
If a Chrome user or an enterprise explicitly trusts any of the affected Chunghwa Telecom or Netlock certificates on a platform and version of Chrome relying on the Chrome Root Store, for example, when explicit trust is conveyed through a Windows Group Policy Object, the Signed Certificate Timestamp (SCT) constraints described above will be overridden and certificates will function as they do today. 
For additional information and testing resources, see [_Sustaining Digital Certificate Security - Upcoming Changes to the Chrome Root Store_][100].
To learn more about the Chrome Root Store, see this [_FAQ_][101].
    * **Chrome 139 on Android, ChromeOS, Linux, macOS, Windows:** All versions of Chrome 139 and higher that rely on the Chrome Root Store will honor the blocking action, but the blocking action will only begin for certificates issued after July 31, 2025.

  * **Stop sending Purpose: prefetch header from prefetches and prerenders**![back to top][73]
Now that prefetches and prerenders are using the Sec-Purpose header for prefetches and prerenders, this change removes the legacy `Purpose: prefetch` header that is still currently passed. This update is behind a feature flag or kill switch to prevent compatibility issues.
The scope includes speculation rules prefetch, speculation rules prerender, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`.
    * **Chrome 139 on Windows, macOS, Linux, Android**

  * **Chrome to remove support for macOS 11**![back to top][73]
Chrome 138 is the last release to support macOS 11; Chrome 139 and later will no longer support macOS 11, which is outside of its support window with Apple. Running on a supported operating system is essential to maintaining security.
On Macs running macOS 11, Chrome will continue to work, showing a warning infobar, but will not update any further. If a user wishes to have their Chrome updated, they need to update their computer to a support version of macOS. For new installations of Chrome 139 and later, macOS 12 and later will be required.
    * **Chrome 139 on Windows, macOS, Linux**

  * **Fire error event instead of throwing exception for CSP blocked worker**![back to top][73]
When blocked by [_Content Security Policy (CSP)_][102], Chromium currently throws a SecurityError from the constructor of Worker and SharedWorker. To be spec-compliant, the CSP needs to be checked as part of fetch and then fire error events asynchronously instead of throwing an exception when the script runs new Worker(url) or new SharedWorker(url). 
This update aims to make Chromium spec-conformant, which is, it no longer throws exceptions following constructor calls, and fires error events asynchronously.
    * **Chrome 139 on Windows, macOS, Linux, Android**

  * **Randomizing TCP port allocation on Windows**![back to top][73]
This feature enables TCP port randomization on Windows versions 2020 H1 and later. We do not anticipate issues with rapid re-use of prior ports (which can cause rejections due to port re-use timeouts) on these versions. The rapid port re-use issue stems from [_the Birthday problem_][103], where the probability of randomly re-picking an already used port quickly approaches 100% with each new port chosen, unlike sequential port re-use models.
    * **Chrome 139 on Windows, macOS, Linux**

  * **New policies in Chrome browser**![back to top][73]
**Policy** | **Description**  
---|---  
[_GeminiSettings_][104] |  Settings for Gemini integration  
[_WatermarkStyle_][105] |  Configure Custom Watermark Settings  
[_EnableUnsafeSwiftShader_][106] |  Allow software WebGL fallback using SwiftShader  
[_NTPFooterManagementNoticeEnabled_][85] |  Control the visibility of the management notice on the New Tab Page for managed browsers  
[_EnterpriseLogoUrlForBrowser_][86] |  Enterprise Logo URL for a managed browser  
[_EnterpriseCustomLabelForBrowser_][87] |  Set a custom enterprise label for a managed browser  
[_LocalNetworkAccessRestrictionsEnabled_][107] |  Specifies whether to apply restrictions to requests to local network endpoints  
[_LocalNetworkAccessAllowedForUrls_][108] |  Allow sites to make requests to local network endpoints.  
[_LocalNetworkAccessBlockedForUrls_][109] |  Block sites from making requests to local network endpoints.  

  * **Removed policies in Chrome browser**![back to top][73]
**Policy** | **Description**  
---|---  
[_ExtensionManifestV2Availability_][83] |  Control Manifest v2 extension availability  
[_SelectParserRelaxationEnabled_][110] |  Controls whether the new HTML parser behavior for the &lt;select&gt; element is enabled  
[_KeyboardFocusableScrollersEnabled_][111] |  Enable keyboard focusable scrollers  

## Chrome Enterprise Core changes  

  * **Group based policies for connector configuration selection**![back to top][73]
Reporting connector configurations that receive events sent by managed browsers can now be [_configured by groups_][112] in addition to organizational units. 
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows**
![Chrome Web Store][113]
![Chrome Web Store][114]

  * **New remote commands and CSV export for the Managed profiles list**![back to top][73]
The Admin console will support profile-level "Clear cache" and "Clear cookies" remote commands, and CSV export for the Managed Profiles list. You can select one or multiple profiles and perform a remote command.
    * Chrome 137 on Android, Linux, macOS, Windows: Adding CSV export for Managed profiles. 
    * **Chrome 139 on Linux, macOS, Windows:** Profile-level support for remote commands. 

  * **New tab page cards for Microsoft 365**![back to top][73]
Enterprise users with Outlook or SharePoint can now access their upcoming meetings or suggested files directly from the **New tab** page. This streamlined experience eliminates the need to switch tabs or waste time searching for your next meeting, allowing you to focus on what matters most. Admins can enable the cards with [_NTPSharepointCardVisible_][115] and [_NTPOutlookCardVisible_][116]. For Microsoft tenants who do not allow for self-authorization, the admin must also consent to the app permissions during first authentication or approve the app for use in Microsoft Entra.
    * Chrome 134 on Linux, macOS, Windows: Available to Trusted Testers 
    * Chrome 137 on Linux, macOS, Windows: Gradual rollout to all customers 
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows:** Users do not need to be signed into Chrome to use this feature
![Chrome Web Store][117]
![Chrome Web Store][118]

  * **Regionalize covered Chrome Enterprise data**![back to top][73]
Starting in Chrome 139, Admins can use data regions to store users’ covered Chrome Enterprise data in a specific geographic location. The location options are United States, European Union (labeled Europe in the Google Admin console), or No preference. The initial migration will not complete until the end of Chrome 140. This can be set in the Google Admin console via **Data > Compliance > Data regions > Region > Data at rest**. For more information about the types of data covered, see the [_Chrome Enterprise Service Specific Terms_][119]. 
    * **Chrome 139 on Android, iOS, ChromeOS, Linux, macOS, Windows:** Rollout will begin. Admins may be able to set a region; however, data may not be fully regionalized until the end of Chrome 140.
    * Chrome 140 on Android, iOS, ChromeOS, Linux, macOS, Windows: The initial migration will be fully regionalized.

## Chrome Enterprise Premium changes
Read more about the differences between [_Chrome Enterprise Core and Chrome Enterprise Premium_][120].
  * **Active account detection**![back to top][73]
Chrome Enterprise can now detect whether an employee is using their corporate or personal Google account on Google Workspace pages like Google Drive, Docs, or Gmail. This allows administrators to create more granular Data Loss Prevention (DLP) rules to prevent sensitive data from being moved to personal accounts, addressing a critical data exfiltration risk.**** For instance, an administrator can now configure a policy in the Google Admin console to block a file upload to a personal Google Drive account while still allowing it to a corporate account.**** To use this feature, administrators should create or update their DLP rules to include the new **Google Workspace Web app signed-in account** condition. There is no single enterprise policy to enable or disable this feature; control is managed through the creation of these specific DLP rules.
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows:** The Chrome browser can detect the active user account on Google Workspace pages and sends this information as a new signal with Data Loss Prevention (DLP) scan requests.

  * **Chrome Enterprise Connectors API**![back to top][73]
Chrome Enterprise is introducing programmatic management for Chrome Enterprise Connectors. This update exposes connector settings as new and updated policies within the existing Chrome Policy API, allowing IT administrators and technology partners to manage these configurations at scale. Previously, this was a manual process in the Google Admin console. This update enables automation, which helps reduce manual errors and improve the efficiency of managing integrations with third-party security solutions.
Administrators can use the Chrome Policy API to programmatically control settings for event reporting, content analysis, and real-time URL checks. This launch includes updates to the [_OnSecurityEventEnterpriseConnector_][121] policy and adds new policies such as [_OnFileAttachedEnterpriseConnector_][122], [_OnFileDownloadedEnterpriseConnector_][123], [_OnFileTransferEnterpriseConnector_][124], [_OnBulkDataEntryEnterpriseConnector_][125], [_OnPrintEnterpriseConnector_][126], and [_EnterpriseRealTimeUrlCheckMode_][127].
For technical details, developers should refer to the main [_Chrome Policy API documentation_][128]
    * **Chrome 139 on Android, iOS, Linux, macOS, Windows:** This rollout adds support for programmatic management of Chrome Enterprise Connectors via a new API

  * **Copy and paste rules protection**![back to top][73]
To help organizations better prevent data exfiltration on mobile devices, Chrome is extending its existing desktop clipboard data controls. Administrators can now use the [_DataControlsRules_][129] policy to set rules that block or warn users when they attempt to copy or paste content that violates organizational policies. This feature allows admins to define data boundaries and prevent sensitive information from being pasted from a work context into personal apps or websites on their mobile fleet. This addresses a significant security gap and a frequently requested feature from enterprise customers who have cited the lack of mobile data controls as a concern. To use this feature, administrators can configure clipboard restrictions within the [_DataControlsRules_][129] policy, providing a consistent management experience across desktop and mobile to strengthen their organization's overall security posture.
    * **Chrome 139 on Android:** Copy and Paste rules protection becomes available on Android

  * **Data Loss Prevention support for iFrames**![back to top][73]
To enhance security and prevent data exfiltration, Chrome's Data Loss Prevention (DLP) capabilities are being extended to the content within iFrames. Currently, DLP rules configured by administrators do not apply to content inside an iFrame, which allows a potential security loophole where users can bypass restrictions. This feature closes that gap. With this change, when a user performs a DLP-triggering action (such as uploading a file) from a site loaded in an iFrame, Chrome will send the entire URL hierarchy, from the source iFrame up to the top-level page, to be evaluated against all applicable DLP rules.
The motivation for this change is to provide a more robust security posture and eliminate a known method for bypassing data protection policies. No new enterprise policies are required to enable this functionality; it will work with existing DLP rules configured via the [_Connector policies_][130]. Administrators should be aware that their existing rules will now apply to iFrame contexts, which may block user actions that were previously permitted.
    * **Chrome 139 on Linux, macOS, Windows:** Initial launch of Data Loss Prevention support for iFrames. This phase adds enforcement for file upload events originating from within an iFrame context and it will work with existing DLP rules configured via the [_OnFileAttachedEnterpriseConnector_][122] policy
    * Chrome 140 on Linux, macOS, Windows: This expanded phase combines two feature rollouts, extending DLP iFrame support to include enforcement for both file download and printing actions.

  * **Enable watermarking on Single Page Applications**![back to top][73]
To enhance data security, Chrome Enterprise Premium’s watermarking feature now supports Single Page Applications (SPAs). This addresses a significant customer request, as watermarks previously only applied to traditional websites. This capability is controlled by your existing Data Loss Prevention (DLP) policies in the Google Admin Console; no new policy configuration is required for this enhancement.
IT administrators should be aware of a key technical limitation. SPAs utilize same-document navigations, which cannot be paused for a security scan like a standard page load. Consequently, there may be a brief delay before a watermark appears after navigating within an SPA. Additionally, DLP rules set to _Warn_ or _Block_ will not display an interstitial page for these SPA navigations; the action would only trigger on a full page reload.
    * **Chrome 139 on ChromeOS, Linux, macOS, Windows:** This rollout adds support for watermarking on Single Page Applications (SPAs)

↑ back to top
## Coming soon
**Note:** The items listed below are experimental or planned updates. They might change, be delayed, or canceled before launching to the Stable channel.
#### Upcoming Chrome browser changes
  * **2SV enforcement for admins** ![back to top][73]
To better protect your organization’s information, Google will soon require all accounts with access to admin.google.com to have 2-Step Verification (2SV) enabled. As a Google Workspace administrator, you need to confirm your identity with 2SV, which requires your password plus something additional, such as your phone or a security key.
The enforcement will be rolled out gradually over the coming months. You should enable 2SV for the admin accounts in your organization before Google enforces it. For more information, see this [_About 2SV enforcement for admins_][131].
    * Chrome 137 on ChromeOS, Linux, macOS, Windows: 2SV enforcement starts
    * **Chrome 140 on ChromeOS, Linux, macOS, Windows: 2SV mandatory**

  * **Automated password change** ![back to top][73]
When Chrome detects that a user has signed into a website with a known compromised password, it will offer the user to change it automatically. This feature will be available on a set of eligible sites. The feature uses AI, and can be controlled via the Enterprise policy **AutomatedPasswordChangeSettings**.
    * **Chrome 140 on ChromeOS, Linux, macOS, Windows**
[**_![][132]_**][133]

  * **Contextual search suggestions in Chrome Address bar** ![back to top][73]
With this feature you can ask anything about the page you’re on, directly in context. Building on the existing Search habit of the address bar, users can ask a question with Google Lens by selecting anything on screen or asking with words. A Google Lens action in the address bar and contextual suggestions guide people to the feature when it’s most helpful. This feature is gated by the existing [_LensOverlaySettings_][134] policy.
    * Chrome 138 on ChromeOS, Linux, macOS, Windows: Feature starts rollout
    * **Chrome 140 on ChromeOS, Linux, macOS, Windows:** If the [_LensOverlaySettings_][134] policy is not set this feature will respect the [_GenAiDefaultSettings_][135] policy if present.
![][136]

  * **Enhanced autofill** ![back to top][73]
Starting in Chrome 137, some users can turn on Autofill with AI, a new feature that helps users fill out online forms more easily. On relevant forms, Chrome can use AI to better understand the form and offer users to automatically fill in previously saved info. Admins can control the feature using the existing [_GenAiDefaultSettings_][135] policy and a new [_AutofillPredictionSettings_][137] policy.
    * Chrome 137 on ChromeOS, Linux, macOS, Windows
    * **Chrome 140 on ChromeOS, Linux, macOS, Windows:** The existing "Autofill with AI" feature will be renamed to "Enhanced autofill", allow users to save and fill additional types of info, and become available in more countries and languages.

  * **Gemini in Chrome** ![back to top][73]
Gemini is now integrated into Chrome on macOS and Windows, and can understand the content of your current page. Users can now seamlessly get key takeaways, clarify concepts, and find answers, all without leaving their Chrome tab. This integration includes both chat—where users can interact with Gemini via text, and Gemini Live, with which users can interact with Gemini via voice.
In Chrome 140, [_Gemini in Chrome_][138] will become available for users signed into Chrome in the US. Admins can turn off this feature (value 1) using the [_GeminiSettings_][104] policy or by using the [_GenAiDefaultSettings_][135] (value 2). For more details, see [_Gemini in Chrome_][138] in the Help Center.
    * Chrome 137 on macOS, Windows: Feature is available for some Google AI Pro and Ultra subscribers in the US and on pre-Stable (Dev, Canary, Beta) channels in the US.
    * **Chrome 140 on macOS, Windows:** Feature gradually rolls out on Stable for users signed into Chrome in the US. 

  * **Happy Eyeballs V3** ![back to top][73]
This launch is an internal optimization in Chrome that implements [_Happy Eyeballs V3_][139] to achieve better network connection concurrency. Happy Eyeballs V3 performs DNS resolutions asynchronously and staggers connection attempts with preferable protocols (H3/H2/H1) and address families (IPv6 or IPv4) to reduce user-visible network connection delay. This feature is gated by a temporary policy [_HappyEyeballsV3Enabled_][140].
    * **Chrome 140 on Android, ChromeOS, Linux, macOS, Windows**

  * **Launch Chrome into new profile via command line** ![back to top][73]
This enhancement addresses a critical gap for our enterprise partners and admin who need to launch web applications from their native app catalogs directly into a specific managed Chrome profile using Chrome CLI (command line interface). Currently, if the designated profile does not exist, Chrome defaults to the last-used profile, creating a disjointed and insecure user experience. With this new feature, when a specified profile is not found, Chrome will initiate the existing profile creation flow, pre-populating the user's email address to streamline the setup process. This is a key technical enabler for admins aiming to onboard their enterprise users to Chrome Enterprise via Managed Profiles.
    * **Chrome 140 on Linux, macOS, Windows**

  * **PostQuantum cryptography for DTLS in WebRTC** ![back to top][73]
This feature enables the use of PostQuantum Cryptography (PQC) with WebRTC connections. The motivation for PQC is to get WebRTC media traffic up to date with the latest cryptography protocols and prevent _Harvest Now to Crack Later_ scenarios. 
This feature will be controllable by an enterprise policy **WebRtcPostQuantumKeyAgreementEnabled** , to allow enterprise users to opt out of PQC. The policy will be temporary and is planned to be removed by Chrome 150.
    * **Chrome 140 on Android, ChromeOS, Linux, macOS, Windows, Fuchsia**
    * Chrome 150 on Android, ChromeOS, Linux, macOS, Windows, Fuchsia: Remove Enterprise Policy

  * **ServiceWorkerAutoPreload mode** ![back to top][73]
ServiceWorkerAutoPreload is a mode where the browser issues the network request in parallel with the service worker bootstrap, and consumes the network request result inside the fetch handler if the fetch handler returns the response with respondWith(). If the fetch handler result is fallback, it passes the network response directly to the browser. ServiceWorkerAutoPreload is defined as an optional browser optimization, which will change the existing service worker behavior.
A temporary enterprise policy called **ServiceWorkerAutoPreloadEnabled** will be added to control this feature.
    * **Chrome 140 on Android, Windows:** policy will be made available
    * Chrome 144 on Android, Windows: policy will be removed

  * **CSS find-in-page highlight pseudos** ![back to top][73]
Exposes find-in-page search result styling to authors as a highlight pseudo-element, like selection and spelling errors. This allows authors to change the foreground and background colors or add text decorations, which can be especially useful if the UA defaults have insufficient contrast with the page colors or are otherwise unsuitable.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Deprecate special font size rules for H1 within some elements** ![back to top][73]
The HTML spec contains a list of [_special rules for <h1> tags _][141]nested within <article>, <aside>, <nav>, or <section> tags. These special rules are deprecated, because they cause accessibility issues. Namely, they visually reduce the font size for nested <h1>s so that they "look" like <h2>s, but nothing in the accessibility tree reflects this demotion.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **IP protection** ![back to top][73]
This feature limits availability of a user’s original IP address in third-party contexts in **Incognito mode** , enhancing Incognito's protections against cross-site tracking when users choose to browse in this mode. IP addresses facilitate a range of use cases, including routing traffic and preventing fraud and spam. However, they can also be used for tracking. For Chrome users who choose to browse in Incognito mode, we want to provide additional control over their IP address, without breaking essential web functionality. To strike this balance between protection and usability, this proposal focuses on limiting the use of IP addresses in a third-party context in Incognito mode. To that end, this proposal uses a list-based approach, where only domains on the [_Masked Domain List (MDL)_][142] in a third-party context will be impacted. For enterprises, this feature can be controlled via the [_PrivacySandboxIpProtectionEnabled_][143] enterprise policy.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Local network access restrictions** ![back to top][73]
Chrome 140 restricts the ability to make requests to the user's local network, gated behind a permission prompt. A local network request is any request from a public website to a local IP address or loopback, or from a local website (for example,. intranet) to loopback. Gating the ability for websites to perform these requests behind a permission mitigates the risk of cross-site request forgery attacks against local network devices such as routers, and reduces the ability of sites to use these requests to fingerprint the user's local network.
This permission is restricted to secure contexts. If granted, the permissions additionally relaxes mixed content blocking for local network requests (since many local devices are not able to obtain publicly trusted TLS certificates for various reasons).
This work supersedes a prior effort called [_Private Network Access_][144], which used preflight requests to have local devices opt-in. Enterprises that need to disable or auto-grant the permission can do so using the [_LocalNetworkAccessAllowedForUrls_][108] and [_LocalNetworkAccessBlockedForUrls_][109] policies. The value of '*' can be used to allow local network access on all URLs, matching the behavior prior to rolling out the restrictions.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Probabilistic Reveal Tokens** ![back to top][73]
To ensure that all businesses can continue to estimate the amount of fraud on their systems, train models to defend against fraud, and analyze emerging fraudulent behavior while still mitigating the ability to track users at scale using IP addresses, we propose to introduce a delayed IP sampling mechanism called Probabilistic Reveal Tokens (PRTs) alongside IP Protection for use in protected traffic.
PRTs will be included on proxied requests in a new HTTP header added by the browser for domains that indicate they want to receive them via a signup process. Each PRT will contain a ciphertext, generated by an Issuer and re-randomized for unlinkability by the browser prior to the request, that the recipient can decrypt after a delay. Google will be the issuer for Chrome's implementation. A minority of the decrypted PRTs contain the client's pre-proxy IP address (that is, non-masked, and as observed by the token issuer), while the remaining PRTs provide no information about the client's original IP address. This results in only a small percent of PRTs containing and revealing the user's IP. Since PRTs will only be attached when IP Protection is enabled, admins can use the [_PrivacySandboxIpProtectionEnabled_][143] policy to control IP Protection and PRTs.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Propagate Viewport overscroll-behavior from Root** ![back to top][73]
This feature will propagate overscroll-behavior from the root instead of the body. The [_CSS working group resolved_][145] on not propagating properties from the body to the viewport. Rather, properties of the viewport are to be propagated from the root element e.g. [_scroll-behavior_][146], [_scroll-snap-type_][147], [_scroll-padding_][148]. As such, overscroll-behavior should be propagated from the root element. However, Chrome has had a longstanding issue of propagating overscroll-behavior from the body rather than the root, which deviates from the behavior of Safari(WebKit) and Firefox(Gecko). This feature intends to fix this by propagating overscroll-behavior from the root rather than the body.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Script blocking in Incognito** ![back to top][73]
Mitigating API Misuse for Browser Re-Identification, otherwise known as Script Blocking, is a feature that will block scripts engaging in known, prevalent techniques for browser re-identification in third-party contexts. These techniques typically involve the misuse of existing browser APIs to extract additional information about the user's browser or device characteristics.
This feature uses a list-based approach, where only domains marked as “Impacted by Script Blocking” on the Masked Domain List (MDL) in a third-party context will be impacted. When the feature is enabled, Chrome will check network requests against the blocklist. The Chromium's subresource_filter component will be reused, which is responsible for tagging and filtering subresource requests based on page-level activation signals, and a ruleset is used to match URLs for filtering. The enterprise policy name is **PrivacySandboxFingerprintingProtectionEnabled**.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **SharedWorker script inherit controller for blob script URL** ![back to top][73]
According to [_Worker client case (github)_][149], workers should inherit controllers for the blob URL. However, existing code allows only dedicated workers to inherit the controller, and shared workers do not inherit the controller. This is the fix to make Chromium behavior adjust to the specification. An enterprise policy [_SharedWorkerBlobURLFixEnabled_][150] is available to control this feature.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Strict Same Origin Policy for Storage Access API** ![back to top][73]
We plan to adjust the [_Storage Access API_][151] semantics to strictly follow the Same Origin Policy, to enhance security. Using document.requestStorageAccess() in a frame only attaches cookies to requests to the iframe's origin (not site) by default. The [_CookiesAllowedForUrls_][152] policy or Storage Access Headers can still be used to unblock cross-site cookies.
    * **Chrome 140 on Windows, macOS, Linux, Android**

  * **Web App Manifest: specify update eligibility, icon URLs are Cache-Control: immutable** ![back to top][73]
As early as Chrome 139, the Web App manifest will specify an update eligibility algorithm. This makes the update process more deterministic and predictable, giving the developer more control over whether (and when) updates should apply to existing installations, and allowing removal of the 'update check throttle' that user agents currently need to implement to avoid wasting network resources.
    * **Chrome 141 on Windows, macOS, Linux**
    * Chrome 142 on Android

  * **Clear window name for cross-site navigations that switches browsing context group** ![back to top][73]
The value of the window.name property is currently preserved throughout the lifetime of a tab, even with navigation that switches browsing context groups, which can leak information and potentially be used as a tracking vector. Clear the window.name property in this case addresses this issue. 
This update will introduce a new temporary enterprise policy, **ClearWindowNameCrossSiteBrowsing** , which will stop working in Chrome 146.
    * **Chrome 142 on Windows, macOS, Linux, Android, iOS**

  * **Disallow non-trustworthy plaintext HTTP prerendering** ![back to top][73]
This launch will provide the capability to disallow non-trustworthy plaintext HTTP prerendering.
    * **Chrome 142 on Windows, macOS, Linux, Android**

  * **HSTS tracking prevention** ![back to top][73]
This update will mitigate user tracking by third-parties via the [_HTTP Strict Transport Security (HSTS)_][153] cache. This feature only allows HSTS upgrades for top-level navigations and blocks HSTS upgrades for sub-resource requests. Doing so makes it infeasible for third-party sites to use the HSTS cache in order to track users across the web.
    * **Chrome 142 on Windows, macOS, Linux, Android**

  * **Disallow spaces in non-file:// URL hosts** ![back to top][73]
According to the [_URL Standard specification_][154], URL hosts cannot contain the space character, but currently URL parsing in Chromium allows spaces in the host. This causes Chromium to fail several tests included in the [_Interop2024 HTTPS URLs for WebSocket_][155] and [_URL focus_][156] areas. To bring Chromium into spec compliance, we would like to remove spaces from URL hosts altogether, but a difficulty with this is that they are used in the host part in Windows file:// URLs ([_Github_][157]).
    * **Chrome 145 on Android, ChromeOS, LaCrOS, Linux, macOS, Windows, Fuchsia**

  * **Remove Third-party storage partitioning policies** ![back to top][73]
Third-party storage partitioning became the default in Chrome 115. The chrome:// flag that allowed users to disable this feature was removed in Chrome 128, and the deprecation trial ended with Chrome 139. In Chrome 145, the enterprise policies [_DefaultThirdPartyStoragePartitioningSetting_][158] and [_ThirdPartyStoragePartitioningBlockedForOrigins_][159] will be removed. Users are advised to transition to alternative storage solutions, either by adapting to third-party storage partitioning or by using `document.requestStorageAccess({...})` where needed.
If you have any feedback, you can add it [_here in the Chromium bug_][160].
    * **Chrome 145 on Android, ChromeOS, Linux, macOS, Windows, Fuchsia:** Removal of [_DefaultThirdPartyStoragePartitioningSetting_][158] and [_ThirdPartyStoragePartitioningBlockedForOrigins_][159]

  * **SafeBrowsing API v4 → v5 migration** ![back to top][73]
Chrome calls into the [_SafeBrowsing v4 API_][161] will be migrated to call into the [_v5 API_][162] instead. The method names are also different between v4 and v5. If admins have any v4-specific URL allowlisting to allow network requests to https://safebrowsing.googleapis.com/v4*, these should be modified to allow network requests to the whole domain instead: safebrowsing.googleapis.com. Otherwise, rejected network requests to the v5 API will cause security regressions for users. For more details, see [_Migration From V4 - Safe Browsing_][163]. 
    * **Chrome 145 on Android, iOS, ChromeOS, Linux, macOS, Windows:** Feature would gradually roll-out 

  * **Isolated Web Apps** ![back to top][73]
Isolated Web Apps (IWAs) are an extension of existing work on PWA installation and Web Packaging that provide stronger protections against server compromise and other tampering that is necessary for developers of security-sensitive applications.
Rather than being hosted on live web servers and fetched over HTTPS, these applications are packaged into Web Bundles, signed by their developer, and distributed to end-users through one or more of the potential methods described in the [_explainer_][164]. 
In this initial release, IWAs will only be installable through an admin policy on enterprise-managed ChromeOS devices.
    * **Chrome 146 on Windows** This rollout adds support for Isolated Web Apps in enterprise-managed browser configurations on Windows.

  * **UI Automation accessibility framework provider on Windows** ![back to top][73]
Starting in Chrome 126, Chrome will start directly supporting accessibility client software that uses Microsoft Windows's UI Automation accessibility framework. Prior to this change, such software interoperated with Chrome by way of a compatibility shim in Microsoft Windows. This change is being made to improve the accessible user experience for many users. It provides complete support for Narrator, Magnifier, and Voice Access; and will improve third-party apps that use Windows's UI Automation accessibility framework. Users of Chrome will find reduced memory usage and processing overhead when used with accessibility tools. It will also ease development of software using assistive technologies.
Administrators may use the [_UiAutomationProviderEnabled_][165] enterprise policy starting in Chrome 125 to either force-enable the new provider (so that all users receive the new functionality), or disable the new provider. This policy will be supported through Chrome 146, and will be removed in Chrome 147. This one-year period is intended to give enterprises sufficient time to work with third-party vendors so that they may fix any incompatibilities resulting from the switch from Microsoft's compatibility shim to Chrome's UI Automation provider.
    * Chrome 125 on Windows: The [_UiAutomationProviderEnabled_][165] policy is introduced so that administrators can enable Chrome's UI Automation accessibility framework provider and validate that third-party accessibility tools continue to work.
    * Chrome 126 on Windows: The Chrome variations framework will be used to begin enabling Chrome's UI Automation accessibility framework provider for users. It will be progressively enabled to the full stable population, with pauses as needed to address compatibility issues that can be resolved in Chrome. Enterprise administrators may continue to use the [_UiAutomationProviderEnabled_][165] policy to either opt-in early to the new behavior, or to temporarily opt-out through Chrome 146.
    * **Chrome 147 on Windows:** The [_UiAutomationProviderEnabled_][165] policy will be removed from Chrome. All clients will use the browser's UI Automation accessibility framework provider.

### **Upcoming Chrome Enterprise Core updates**
** **
  * **Inactive profile deletion in Chrome Enterprise Core** ![back to top][73]
In June 2025, the inactive period for profile deletion setting started to roll out. In August 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. When releasing the setting, the inactivity period of time has a default value of 90 days. Meaning that by default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value [_using this setting_][166]. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.
If the set value is lowered, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is reactivated on a device, that profile will reappear in the console.
    * **Chrome 140 on Android, ChromeOS, Linux, macOS, Windows:** Policy was rolled out in June. Deletion will start in August and the initial wave of deletion will complete by the beginning of September. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

** **
  * **Chrome Enterprise Overview page** ![back to top][73]
This feature is introducing a new **Overview** page in the Chrome browser section of the Google Admin console. The Overview page allows IT administrators to quickly find key information about their deployment:
\- Active & inactive profiles and enrolled browsers
\- Identify browsers out-of-date and with pending updates
\- Identify high-risk extensions (according to Spin.AI) and get a preview of most requested extensions
\- Security Insights (for example, sensitive file uploads or downloads)
The Overview page also allows admins to quickly access key actions such as managing extensions, accessing the browser or profile list and setting Update policies, to name a few.
    * Chrome 137 on Android, iOS, Linux, macOS, Windows
    * **Chrome 141 on Android, iOS, Linux, macOS, Windows:** New filtering available on the Overview page for Organization Unit and Activity Dates

#### Upcoming Chrome Enterprise Premium changes
  * **Increased file size support for Data Loss Prevention scans**![back to top][73]
Chrome Enterprise Premium now extends its Data Loss Prevention (DLP) and malware scanning capabilities to include large and encrypted files. Previously, files larger than 50 MB and all encrypted files were skipped during content scanning. This update closes that critical security gap. For policies configured to save evidence, files **up to 2GB** can now be sent to the Evidence Locker. This provides administrators with greater visibility and control, significantly reducing the risk of data exfiltration through large file transfers.
No new policy is required to enable this feature. It is automatically controlled by the existing DLP rule configurations in the Google Admin Console. If admins have rules that apply to file uploads, downloads, or printing, they will now also apply to large and encrypted files.
    * **Chrome 140 on Linux, macOS, Windows:** Feature is rolled out

  * **Watermarking customization**![back to top][73]
Chrome Enterprise Premium now allows administrators to customize the appearance of watermarks. This enhancement is motivated by the need to improve user experience, addressing concerns such as eyestrain and readability on pages with existing watermarks.
To control the watermark's appearance, administrators should use the new [_WatermarkStyle_][105] policy. Within this policy, admins can configure the following:
    * 'font_size': Sets the font size of the text in pixels. 
    * 'fill_opacity': Sets the fill opacity of the text, from 0 (transparent) to 100 (opaque). 
    * 'outline_opacity': Sets the outline opacity of the text, from 0 (transparent) to 100 (opaque). 
This provides administrators with greater flexibility to balance security requirements with end-user productivity.
    * **Chrome 140 on ChromeOS, Linux, macOS, Windows:** This launch enables administrators to customize watermark font size and opacity using the new [_WatermarkStyle_][105] policy in the Google Admin Console.
    * Chrome 141 on ChromeOS, Linux, macOS, Windows:**** As an enhancement, a new chrome:// enterprise page is introduced that allows administrators to preview their configured watermark style before deployment.

  * **Chrome browser rule UX refactor**![back to top][73]
To enhance the [_Data Loss Prevention (DLP)_][167] rule creation experience, the Google Admin console is being updated to streamline how administrators define policies for different applications like Chrome and Workspace. This first introduces mutually exclusive application groups, meaning that a single DLP rule can now only target one application group at a time—either Workspace apps (like Drive, Gmail), Chrome browser triggers (like file upload, URL visited), or ChromeOS triggers. This change simplifies rule configuration, eliminates potential conflicts from overlapping app selections, and lays the groundwork for more specialized and user-friendly workflows tailored to each platform's needs.
Administrators will see an updated "Apps" selection interface using radio buttons to enforce this single-group selection for new rules. Existing rules that previously combined applications from multiple groups will be transparently migrated by the system into separate, compliant, single-platform rules to ensure continued protection and a seamless transition. Banners within the Admin console will provide information regarding these changes and the migration process. No new enterprise policies are introduced with this update; the changes are to the rule configuration interface.
    * **Chrome 141 on ChromeOS, Linux, macOS, Windows:** Enables mutually exclusive app selection for DLP rule configuration in Admin Console
[**_![][168]_**][169]

↑ back to top
[Sign up for emails about future releases][170]
## Previous release notes 
Chrome version & targeted Stable channel release date  
---  
[Chrome 137: May 20, 2025][171]  
[Chrome 136: April 23, 2025][172]  
[Chrome 135: March 26, 2025][173]  
[Chrome 134: February 26, 2025][174]  
[Previous release notes][175] →  
## Additional resources
  * To try out new features before they're released, sign up for the [trusted tester program][176].
  * Connect with other Chrome Enterprise IT admins through the [Chrome Enterprise Customer Forum][177].
  * How Chrome releases work—[Chrome Release Cycle][178]. 
  * For specific dates, see the [Chrome release schedule][11]. 
  * Chrome Browser downloads and Chrome Enterprise product overviews—[Chrome Browser for enterprise][179].
  * Chrome version status and timelines—[Chrome Platform Status][180] | [Google Update Server Viewer][181].
  * Announcements: [Chrome Releases Blog][182] | [Chromium Blog][183].
  * Developers: Learn about [changes to the web platform][184].

## Still need help?
  * Google Workspace, Cloud Identity customers (authorized access only)—[Contact support][185]
  * Chrome Browser Enterprise Support—Sign up to [contact a specialist][186]
  * [Chrome Administrators Forum][187]
  * [Chrome Enterprise and Education Help Center][188]

_Google and related marks and logos are trademarks of Google LLC. All other company and product names are trademarks of the companies with which they are associated._
## Was this helpful?
How can we improve it?
YesNo
Submit
[Chrome browser ][189] [ChromeOS][190]
More
## Need more help?
### Try these next steps:
[ Post to the help community  Get answers from community members  ][7]
true
## [Help][191]
  * 1 of 7
Chrome Enterprise and Education release notes
  * 2 of 7
[Allow or restrict third-party cookies][192]
  * 3 of 7
[Set up ChromeOS devices for hybrid work][193]
  * 4 of 7
[Prepare Chromebooks for distance learning at home][194]
  * 5 of 7
[Manage change and encourage ChromeOS devices adoption][195]
  * 6 of 7
[Previous release notes][196]
  * 7 of 7
[ChromeOS Long-term Support (LTS) release notes][197]

  * ©2025 Google 
  * [Privacy Policy][9]
  * [Terms of Service][10]

Language  Deutsch‎español‎español (Latinoamérica)‎français‎Indonesia‎italiano‎Nederlands‎polski‎português (Brasil)‎svenska‎Türkçe‎русский‎‏العربية中文（简体）‎中文（繁體）‎日本語‎한국어‎ English‎
Enable Dark Mode
Send feedback on...
This help content & information General Help Center experience
Search
Clear search
Close search
Google apps
Main menu
2401142928988174995
true
Search Help Center
true
true
true
true
true
410864
false
false
false
false

   [1]: </?tab=uu>
   [2]: </chrome/a>
   [3]: <https://www.google.co.jp/intl/en/about/products?tab=uh>
   [4]: <https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=http://support.google.com/chrome/a/answer/7679408&ec=GAZAdQ>
   [5]: </>
   [6]: </chrome/a/?hl=en>
   [7]: </chrome/a/community?hl=en&help_center_link=CLDb1AMSP0Nocm9tZSBFbnRlcnByaXNlIGFuZCBFZHVjYXRpb24gcmVsZWFzZSBub3RlcyAtIENocm9tZSBicm93c2VyCg>
   [8]: <//chromeenterprise.google/>
   [9]: <//www.google.com/intl/en/privacy.html>
   [10]: <https://www.google.com/accounts/TOS>
   [11]: <https://chromiumdash.appspot.com/schedule>
   [12]: </chrome/a/answer/7679408#chromeBrsrA139>
   [13]: </chrome/a/answer/7679408#chromeBrsrB139>
   [14]: </chrome/a/answer/7679408#chromeBrsrC139>
   [15]: </chrome/a/answer/7679408#chromeBrsrD139>
   [16]: </chrome/a/answer/7679408#chromeBrsrE139>
   [17]: </chrome/a/answer/7679408#chromeBrsrF139>
   [18]: </chrome/a/answer/7679408#chromeBrsrG139>
   [19]: </chrome/a/answer/7679408#chromeBrsrH139>
   [20]: </chrome/a/answer/7679408#chromeBrsrI139>
   [21]: </chrome/a/answer/7679408#chromeBrsrJ139>
   [22]: </chrome/a/answer/7679408#chromeBrsrK139>
   [23]: </chrome/a/answer/7679408#chromeBrsrL139>
   [24]: </chrome/a/answer/7679408#chromeBrsrM139>
   [25]: </chrome/a/answer/7679408#chromeBrsrN139>
   [26]: </chrome/a/answer/7679408#chromeBrsrO139>
   [27]: </chrome/a/answer/7679408#chromeBrsrP139>
   [28]: </chrome/a/answer/7679408#chromeBrsrQ139>
   [29]: </chrome/a/answer/7679408#chromeBrsrR139>
   [30]: </chrome/a/answer/7679408#chromeBrsrS139>
   [31]: </chrome/a/answer/7679408#chromeECA139>
   [32]: </chrome/a/answer/7679408#chromeECB139>
   [33]: </chrome/a/answer/7679408#chromeECC139>
   [34]: </chrome/a/answer/7679408#chromeECD139>
   [35]: </chrome/a/answer/7679408#chromeEPA139>
   [36]: </chrome/a/answer/7679408#chromeEPB139>
   [37]: </chrome/a/answer/7679408#chromeEPC139>
   [38]: </chrome/a/answer/7679408#chromeEPD139>
   [39]: </chrome/a/answer/7679408#chromeEPE139>
   [40]: </chrome/a/answer/7679408#upChromeBrsrA139>
   [41]: </chrome/a/answer/7679408#upChromeBrsrB139>
   [42]: </chrome/a/answer/7679408#upChromeBrsrC139>
   [43]: </chrome/a/answer/7679408#upChromeBrsrD139>
   [44]: </chrome/a/answer/7679408#upChromeBrsrE139>
   [45]: </chrome/a/answer/7679408#upChromeBrsrF139>
   [46]: </chrome/a/answer/7679408#upChromeBrsrG139>
   [47]: </chrome/a/answer/7679408#upChromeBrsrH139>
   [48]: </chrome/a/answer/7679408#upChromeBrsrI139>
   [49]: </chrome/a/answer/7679408#upChromeBrsrJ139>
   [50]: </chrome/a/answer/7679408#upChromeBrsrK139>
   [51]: </chrome/a/answer/7679408#upChromeBrsrL139>
   [52]: </chrome/a/answer/7679408#upChromeBrsrM139>
   [53]: </chrome/a/answer/7679408#upChromeBrsrN139>
   [54]: </chrome/a/answer/7679408#upChromeBrsrO139>
   [55]: </chrome/a/answer/7679408#upChromeBrsrP139>
   [56]: </chrome/a/answer/7679408#upChromeBrsrQ139>
   [57]: </chrome/a/answer/7679408#upChromeBrsrR139>
   [58]: </chrome/a/answer/7679408#upChromeBrsrS139>
   [59]: </chrome/a/answer/7679408#upChromeBrsrT139>
   [60]: </chrome/a/answer/7679408#upChromeBrsrU139>
   [61]: </chrome/a/answer/7679408#upChromeBrsrV139>
   [62]: </chrome/a/answer/7679408#upChromeBrsrW139>
   [63]: </chrome/a/answer/7679408#upChromeBrsrX139>
   [64]: </chrome/a/answer/7679408#upChromeBrsrY139>
   [65]: </chrome/a/answer/7679408#upChromeBrsrZ139>
   [66]: </chrome/a/answer/7679408#upChromeBrsrAA139>
   [67]: </chrome/a/answer/7679408#upChromeECA139>
   [68]: </chrome/a/answer/7679408#upChromeECB139>
   [69]: </chrome/a/answer/7679408#upChromeEPA139>
   [70]: </chrome/a/answer/7679408#upChromeEPB139>
   [71]: </chrome/a/answer/7679408#upChromeEPC139>
   [72]: <https://storage.googleapis.com/support-kms-prod/1iM7RUU5V5QNxswHqpLzwrCOU0jMyKRMmdNZ>
   [73]: //storage.googleapis.com/support-kms-prod/875e9907-0d60-4f4e-a960-862bc24a29f4
   [74]: <https://chromeenterprise.google/policies/#AIModeSettings>
   [75]: //lh7-rt.googleusercontent.com/docsz/AD_4nXcgO2UvTOvD21zQPmxeV0IHMOIrdOHrnm2zZr1LGbJ15ZsAYaHn-dGU53HH-3HKKDRL36xpC_whdMf2N7MXJav5sG8RqWqdPhCrWI_dxYkSRPqekbq4gemBp8RALRBQThsJwOs5zx0sqFauuLX-34HLLSFYjYlPN37O1dwEPXgXfQKw?key=T_n_QOlTLKvRPMS_dO8mww
   [76]: //lh7-rt.googleusercontent.com/docsz/AD_4nXdrp9RFV523JtvQld4VUtk6QOt5Bw0hlZPQXaoJWEhgLHIAe8iPtxIGKy102916uEfNnOpritx8nxZKyQBFtt6WDtO6HT79ulv-6jy6eoatNCnS9n_e0AmCRJSGEXXohpcHT_vdxfloSUBUeV_P1W0G_cirY6YtJqoH2Ukm0J4Cq6A?key=T_n_QOlTLKvRPMS_dO8mww
   [77]: //lh7-rt.googleusercontent.com/docsz/AD_4nXeDlc_uICvVXlqP1gIvPVtaDfaIatC1Vci-3X1PJgNiE_4RHK1Miv-7RWWWopJls58Q_3OfRTCPHEJfAdkw9w-svrR3phL4FoSFBy0BHCnezn8YI4VvyW7mr17ary0cGDtFRHufzFNC3_nilD_CjEX-dkK9Due1zCnFfvF5V1RcFebZ?key=T_n_QOlTLKvRPMS_dO8mww
   [78]: <https://chromeenterprise.google/policies/#SiteSearchSettings>
   [79]: //storage.googleapis.com/support-kms-prod/JXuSEMHx36odYohRMvFV3vF955dwKBlICxdK
   [80]: //storage.googleapis.com/support-kms-prod/4Tm7Qw11ovHUc4iffj68FM6Sp19MICnPoce7
   [81]: <https://chromeenterprise.google/policies/#SafeBrowsingProtectionLevel>
   [82]: //storage.googleapis.com/support-kms-prod/dF24jQU2k0NBQIXa8V1ArjvyVP3r1lZn9bKG
   [83]: <https://chromeenterprise.google/policies/#ExtensionManifestV2Availability>
   [84]: <https://chromeenterprise.google/policies/#NTPFooterExtensionAttributionEnabled>
   [85]: <https://chromeenterprise.google/policies/#NTPFooterManagementNoticeEnabled>
   [86]: <https://chromeenterprise.google/policies/#EnterpriseLogoUrlForBrowser>
   [87]: <https://chromeenterprise.google/policies/#EnterpriseCustomLabelForBrowser>
   [88]: //storage.googleapis.com/support-kms-prod/OdRIpNFoZ2OqUgcYwybXCMQJjHMUvuAHVcRs
   [89]: <https://support.google.com/chrome/answer/2392709>
   [90]: //lh7-rt.googleusercontent.com/docsz/AD_4nXfDQ2hZnGpM7gu4FYsEIghflvjrep9ggi4185BQiFy0y0PY4uSncVBIH7YbXFXtYMxqJJNOfGj843_4vRiELYEcREcAb5-7qmhO_OzLO401kZ1B_UUYNzIOjdihRGuF4nhfNR_RgHfRa2xZkvUwbssL6mo76QU?key=mteu4N1GlYLou4GHcpRftg
   [91]: //lh7-rt.googleusercontent.com/docsz/AD_4nXfwsIIbiBAsd213q8-TFR4PktBPLntpiUwU6Z_mfUujpPAAaE8c-tcLrfM6je98xnxuzR9MWUndrlWaiCxGrNjOStklamzIo9iwLnrOjkIJKJhQQRhSm_IixzBE8qNQGonxnaKAzIdbegLFXiTBGbJ_Z8YRXb0P?key=mteu4N1GlYLou4GHcpRftg
   [92]: <https://chromeenterprise.google/policies/#ClearBrowsingDataOnExitList>
   [93]: <https://chromeenterprise.google/policies/#BrowsingDataLifetime>
   [94]: //storage.googleapis.com/support-kms-prod/znSeq7qSafE8dUZpg1rXhM9Tx9jRQOJek0d0
   [95]: <https://chromeenterprise.google/policies/#PromotionsEnabled>
   [96]: <https://developer.chrome.com/blog/chrome-for-testing>
   [97]: <https://get.webgl.org/>
   [98]: <https://github.com/google/swiftshader>
   [99]: <https://chromeenterprise.google/policies/#BrowserSignin>
   [100]: <https://security.googleblog.com/2025/05/sustaining-digital-certificate-security-chrome-root-store-changes.html>
   [101]: <https://chromium.googlesource.com/chromium/src/+/main/net/data/ssl/chrome_root_store/faq.md>
   [102]: <https://www.w3.org/TR/CSP3/>
   [103]: <https://www.youtube.com/watch?app=desktop&v=m7hI2LulMxE>
   [104]: <https://chromeenterprise.google/policies/#GeminiSettings>
   [105]: <https://chromeenterprise.google/policies/#WatermarkStyle>
   [106]: <https://chromeenterprise.google/policies/#EnableUnsafeSwiftShader>
   [107]: <https://chromeenterprise.google/policies/#LocalNetworkAccessRestrictionsEnabled>
   [108]: <https://chromeenterprise.google/policies/#LocalNetworkAccessAllowedForUrls>
   [109]: <https://chromeenterprise.google/policies/#LocalNetworkAccessBlockedForUrls>
   [110]: <https://chromeenterprise.google/policies/#SelectParserRelaxationEnabled>
   [111]: <https://chromeenterprise.google/policies/#KeyboardFocusableScrollersEnabled>
   [112]: <https://support.google.com/chrome/a/answer/11375053>
   [113]: //storage.googleapis.com/support-kms-prod/vmjs4jVLbJSAYHlL9PUJoyX3uz6zOTQG2dqE
   [114]: //storage.googleapis.com/support-kms-prod/2TXDSSkncLi6ZawknRF0LeWbEDLgJE8rURR0
   [115]: <https://chromeenterprise.google/policies/#NTPSharepointCardVisible>
   [116]: <https://chromeenterprise.google/policies/#NTPOutlookCardVisible>
   [117]: //storage.googleapis.com/support-kms-prod/VxWZJfJbNXOXFyouF882SbqyRxEoy5HoCvwV
   [118]: //storage.googleapis.com/support-kms-prod/SC8TU5N3ZEMucZePcxW9742B9F6yvT5ZJsVK
   [119]: <https://chromeenterprise.google/terms/service-terms/>
   [120]: <https://chromeenterprise.google/products/chrome-enterprise-premium>
   [121]: <https://chromeenterprise.google/policies/#OnSecurityEventEnterpriseConnector>
   [122]: <https://chromeenterprise.google/policies/#OnFileAttachedEnterpriseConnector>
   [123]: <https://chromeenterprise.google/policies/#OnFileDownloadedEnterpriseConnector>
   [124]: <https://chromeenterprise.google/policies/#OnFileTransferEnterpriseConnector>
   [125]: <https://chromeenterprise.google/policies/#OnBulkDataEntryEnterpriseConnector>
   [126]: <https://chromeenterprise.google/intl/en_ca/policies/#OnPrintEnterpriseConnector>
   [127]: <https://chromeenterprise.google/policies/#EnterpriseRealTimeUrlCheckMode>
   [128]: <https://developers.google.com/chrome/policy/reference/rest>
   [129]: <https://chromeenterprise.google/policies/#DataControlsRules>
   [130]: <https://support.google.com/chrome/a/answer/10106035?sjid=5991552215396607268-NA>
   [131]: <https://support.google.com/a/answer/16271818>
   [132]: //lh7-rt.googleusercontent.com/docsz/AD_4nXeWhTIWOEyarTmEqb6LOfTBTrr71e6G6O5vwJJukvGhMLFmXb1WOBAxuO_cEdI8zMzFgLL7vrLL04Wmiw_2m-oi-twT6Xghl_YzNH1ppH2Vm5I0IheEb_K7uMvhPVN4it_iFXD2SYxE9lv4KuGrwfPyN6dX5sdz?key=mteu4N1GlYLou4GHcpRftg
   [133]: <https://screenshot.googleplex.com/3FX8Zc46htvBw3V.png>
   [134]: <https://chromeenterprise.google/policies/#LensOverlaySettings>
   [135]: <https://chromeenterprise.google/policies/#GenAiDefaultSettings>
   [136]: //screenshot.googleplex.com/5QqMe93RestsmPJ.png
   [137]: <https://chromeenterprise.google/policies/#AutofillPredictionSettings>
   [138]: <https://support.google.com/chrome/a/answer/16291696?sjid=13521622013667211355-NA>
   [139]: <https://datatracker.ietf.org/doc/draft-ietf-happy-happyeyeballs-v3/>
   [140]: <https://chromeenterprise.google/policies/#HappyEyeballsV3Enabled>
   [141]: <https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings>
   [142]: <https://support.google.com/privacysandbox/answer/16085975?hl=en&ref_topic=16076404#:~:text=The%20Masked%20Domain%20List%20(MDL)%20is%20a%20list%20of%20domains,in%20the%20IP%20Protection%20explainer.>
   [143]: <https://chromeenterprise.google/policies/#PrivacySandboxIpProtectionEnabled>
   [144]: <https://developer.chrome.com/blog/local-network-access?hl=en>
   [145]: <https://github.com/w3c/csswg-drafts/issues/6079#issuecomment-816307011>
   [146]: <https://drafts.csswg.org/css-overflow/#:~:text=not%20propagated%20to%20the%20viewport>
   [147]: <https://drafts.csswg.org/css-scroll-snap/#:~:text=not%20propagated%20from%20HTML%20body>
   [148]: <https://drafts.csswg.org/css-scroll-snap/#:~:text=padding%20values%20are%20not%20propagated%20from%20HTML%20body>
   [149]: <https://w3c.github.io/ServiceWorker/#control-and-use-worker-client>
   [150]: <https://chromeenterprise.google/policies/#SharedWorkerBlobURLFixEnabled>
   [151]: <https://privacysandbox.google.com/cookies/storage-access-api>
   [152]: <https://chromeenterprise.google/policies/#CookiesAllowedForUrls>
   [153]: <https://datatracker.ietf.org/doc/html/rfc6797>
   [154]: <https://url.spec.whatwg.org/#forbidden-host-code-point>
   [155]: <https://wpt.fyi/results/websockets?label=master&label=experimental&aligned&view=interop&q=label%3Ainterop-2024-websockets>
   [156]: <https://wpt.fyi/results/url?label=master&label=experimental&aligned&view=interop&q=label%3Ainterop-2023-url>
   [157]: <https://github.com/whatwg/url/issues/599>
   [158]: <https://chromeenterprise.google/policies/#DefaultThirdPartyStoragePartitioningSetting>
   [159]: <https://chromeenterprise.google/policies/#ThirdPartyStoragePartitioningBlockedForOrigins>
   [160]: <http://crbug.com/425248669>
   [161]: <https://developers.google.com/safe-browsing/v4>
   [162]: <https://developers.google.com/safe-browsing/reference>
   [163]: <https://developers.google.com/safe-browsing/reference/Migration.From.V4>
   [164]: <https://github.com/WICG/isolated-web-apps/blob/main/README.md>
   [165]: <https://chromeenterprise.google/policies/#UiAutomationProviderEnabled>
   [166]: <https://support.google.com/chrome/a/answer/2657289#inactive_period_for_profile_deletion&zippy=%2Cinactive-period-for-profile-deletion>
   [167]: <https://support.google.com/chrome/a/answer/13876556>
   [168]: //lh7-rt.googleusercontent.com/docsz/AD_4nXd73M9NfPc24xfw_p5uaB1BezIt81cSV6CA33IEhAhIWLj0DbWFDSehcr6rMxAnIbb4Xdbayr4IyLe46EVPtrKCkWNzlCrajiqCwiCbBPQp3MLLIA0VNLHcVNEqkigNnQk3kV4Imen_T9TAwR_yA_vD12ik4AFy?key=mteu4N1GlYLou4GHcpRftg
   [169]: <https://img800-dot-cr-status.appspot.com/feature/6209161750380544/attachment/5515177512140800>
   [170]: <https://chromeenterprise.google/release-notes/signup/>
   [171]: </chrome/a/answer/10314655#137>
   [172]: </chrome/a/answer/10314655#136>
   [173]: </chrome/a/answer/10314655#135>
   [174]: </chrome/a/answer/10314655#134>
   [175]: </chrome/a/answer/10314655>
   [176]: <https://chromeenterprise.google/engage/trusted-testers/sign-up/>
   [177]: </chrome/a/answer/9267808>
   [178]: <https://chromium.googlesource.com/chromium/src/+/master/docs/process/release_cycle.md>
   [179]: <https://chrome.com/enterprise>
   [180]: <https://chromestatus.com/roadmap>
   [181]: <https://chromiumdash.appspot.com/>
   [182]: <https://chromereleases.googleblog.com/>
   [183]: <https://blog.chromium.org/>
   [184]: <https://blog.chromium.org/search/label/beta>
   [185]: <https://support.google.com/chrome/a/answer/4389193>
   [186]: <https://chromeenterprise.google/browser/support/>
   [187]: <https://productforums.google.com/forum/#!forum/chrome-admins>
   [188]: </chrome/a#topic=4386908>
   [189]: <https://support.google.com/chrome/a/answer/7679408?co=CHROME_ENTERPRISE._Product%3DChromeBrowser>
   [190]: <https://support.google.com/chrome/a/answer/7679408?co=CHROME_ENTERPRISE._Product%3DChromeOS>
   [191]: </chrome/a?hl=en#topic=7679105>
   [192]: </chrome/a/answer/14439269?hl=en&ref_topic=7679105>
   [193]: </chrome/a/answer/9823931?hl=en&ref_topic=7679105>
   [194]: </chrome/a/answer/9773702?hl=en&ref_topic=7679105>
   [195]: </chrome/a/answer/9885964?hl=en&ref_topic=7679105>
   [196]: </chrome/a/answer/10314655?hl=en&ref_topic=7679105>
   [197]: </chrome/a/answer/12239814?hl=en&ref_topic=7679105>

