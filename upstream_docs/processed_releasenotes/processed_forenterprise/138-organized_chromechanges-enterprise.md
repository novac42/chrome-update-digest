### User productivity/Apps

**Current — Chrome 138**

* **# Chrome on Android no longer supports Android Oreo or Android Pie**
  • Type: Chrome Browser changes
  • Platform: Mobile (Android)
  • Update: The last version of Chrome that supports Android Oreo or Android Pie is Chrome 138, and it includes a message to affected users informing them to upgrade their operating system. Chrome 139 and newer versions will not be supported on, nor shipped or available to, users running Android Oreo or Android Pie.
    - **Chrome 139 on Android:** Chrome on Android no longer supports Android Oreo or Android Pie.

* **# Gemini in Chrome**
  • Type: Chrome Browser changes
  • Platform: Desktop (Windows, macOS)
  • Update: Gemini is now integrated into Chrome on macOS and Windows, and can understand the content of your current page. Users can now seamlessly get key takeaways, clarify concepts, and find answers, all without leaving their Chrome tab. This integration includes both chat—where users can interact with Gemini via text, and "Gemini Live", by which users can interact with Gemini via voice.
    In Chrome 137, [Gemini in Chrome](https://support.google.com/chrome/a/answer/16291696?sjid=13521622013667211355-NA) is available for Google AI Pro and Ultra subscribers in the US. A broader rollout will come in future milestones. Admins can turn off this feature (value 1) using the [GeminiSettings](https://chromeenterprise.google/policies/#GeminiSettings) policy or by using the [GenAiDefaultSettings](https://chromeenterprise.google/policies/#GenAiDefaultSettings) (value 2). For more details, see [Gemini in Chrome](https://support.google.com/chrome/a/answer/16291696?sjid=13521622013667211355-NA) in the Help Center.
    - Chrome 137 on macOS, Windows: Feature is available for some Google AI Pro and Ultra subscribers in the US and on pre-Stable (Dev, Canary, Beta) channels in the US.
    - **Chrome 139 on macOS, Windows:** Feature gradually rolls out on Stable for users signed into Chrome in the US.

* **AI Mode for search recommendations in Chrome**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android, iOS)
  • Update: AI Mode is a feature that helps users dive deeper into topics they care about by showing AI Mode for search recommendations in Chrome. A new policy, [AIModeSettings](https://chromeenterprise.google/policies/#AIModeSettings), is available to control search recommendations in the address bar and **New tab** page search box.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Feature starts rollout in the address bar.
    - Chrome 139 on Android, iOS: Feature starts rollout in the address bar.

* **Agentspace recommendations in Chrome search bars**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: To help enterprise users with their internal information needs, you can now add enterprise search results, such as people, file, or query suggestions, from [Agentspace](https://cloud.google.com/products/agentspace) to the Chrome address bar and realbox (search bar on the **New tab** page). Results can be shown by default or only when triggered by a custom keyword.
    With keyword mode in the address bar, users can trigger actions through Agentspace, such as, "help me write an email that summarizes the current project status".
    The enterprise search provider is shown when the user types **@** in the address bar. The organization can customize a keyword or shortcut and the icon shown.
    This can be configured via the [EnterpriseSearchAggregatorSettings](https://chromeenterprise.google/policies/#EnterpriseSearchAggregatorSettings) policy.
    - Chrome 135 on ChromeOS, Linux, macOS, Windows: Trusted Tester
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** General Availability

* **Bookmarks and reading list improvements on Chrome Desktop**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: For Chrome 138 on Desktop, some users who sign in to Chrome upon saving a new bookmark can now use and save bookmarks and reading list items in their Google Account. Relevant enterprise policies controlling bookmarks, as well as [BrowserSignin](https://chromeenterprise.google/policies/#BrowserSignin), [SyncDisabled](https://chromeenterprise.google/policies/#SyncDisabled) or [SyncTypesListDisabled](https://chromeenterprise.google/policies/#SyncTypesListDisabled), continue to work as before, so admins can configure whether or not users can use and save items in their Google Account. Setting [EditBookmarksEnabled](https://chromeenterprise.google/policies/#EditBookmarksEnabled) to false also prevents users from uploading a bookmark saved on their device to their Google Account.
    - **Chrome 138 on Linux, macOS, Windows**

* **Contextual search suggestions in Chrome Address bar**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: With this feature you can ask anything about the page you're on, directly in context. Building on the existing Search habit of the address bar, users can ask a question with Google Lens by selecting anything on screen or asking with words. A Google Lens action in the address bar and contextual suggestions guide people to the feature when it's most helpful. This feature is gated by the existing [LensOverlaySettings](https://chromeenterprise.google/policies/#LensOverlaySettings) policy.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Feature starts rollout
    - Chrome 140 on ChromeOS, Linux, macOS, Windows: If the [LensOverlaySettings](https://chromeenterprise.google/policies/#LensOverlaySettings) policy is not set this feature will respect the [GenAiDefaultSettings](https://chromeenterprise.google/policies/#GenAiDefaultSettings) policy if present.

* **History sync opt-in using the profile pill**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: In Chrome 138, some signed-in users see a new option to opt in to history and tab sync. This change is designed to offer the benefits of history sync in a non-disruptive way by using the profile pill to display a short in-line message. Users who click on the profile pill are taken to their profile menu where they can choose to turn on sync. The goal is to provide users with an intuitive and contextually relevant entry point for syncing data like browsing history, separate from the sign-in flow. For Enterprise users, the expanded profile pill only appears after 4 hours of browser inactivity.
    Relevant enterprise policies controlling History or Tab sync ([SyncDisabled](https://chromeenterprise.google/policies/#SyncDisabled), [SyncTypesListDisabled](https://chromeenterprise.google/policies/#SyncTypesListDisabled) and [SavingBrowserHistoryDisabled](https://chromeenterprise.google/policies/#SavingBrowserHistoryDisabled)) continue to work as before.
    - **Chrome 138 on Linux, macOS, Windows:** Feature starts gradual rollout.

* **Language Detector API**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: Language Detector API is a JavaScript API for detecting the language of text, with confidence levels. An important supplement to translation is language detection. This can be combined with translation, for example, taking user input in an unknown language and translating it to a specific target language. Browsers today often already have language detection capabilities, and we want to offer them to web developers through a JavaScript API, supplementing the translation API. An enterprise policy, [GenAILocalFoundationalModelSettings](https://chromeenterprise.google/policies/#GenAILocalFoundationalModelSettings), is available to disable the underlying model downloading, which would render this API unavailable.
    - **Chrome 138 on Windows, macOS, Linux**

* **Multiple identity support on iOS**
  • Type: Chrome Enterprise Core changes
  • Platform: Mobile (iOS)
  • Update: Chrome on iOS now supports multiple accounts, particularly for managed (work or school) accounts. This update introduces separate browser profiles for each managed account, ensuring strict data separation between work and personal browsing. Regular accounts continue to share a single profile.
    This change aims to improve Chrome's enterprise offering and provide a more secure and organized browsing experience, especially for end users with both personal and work accounts on their device. Users experience a one-time onboarding flow when adding a managed account to the device. They can switch between accounts by tapping on the account particle disk on the **New tab** page.
    Admins who enabled Chrome policies on iOS ([see instructions](https://support.google.com/chrome/a/answer/6304822)) can continue to use existing policies.
    - **Chrome 138 on iOS**

* **New tab page footer**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: An update to the **New tab** page includes a new footer designed to provide users with greater transparency and control over their Chrome experience.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Extension Attribution will begin to show on the NTP. If an extension has changed your default **New tab** page, you'll now see a message in the footer that attributes the change to that specific extension. This message often includes a link directly to the extension in the Chrome Web Store, making it easier to identify and manage unwanted extensions. If you're an administrator, you can disable this attribution using the [NTPFooterExtensionAttributionEnabled](https://chromeenterprise.google/policies/#NTPFooterExtensionAttributionEnabled) policy.
    - Chrome 139 on Linux, macOS, Windows: Browser management disclosure will be shown if one of the policies to customize the footer is set by an enterprise admin. For users whose Chrome browser is managed by a trusted source, the **New tab** page footer will now display a management disclosure notice. This helps you understand how your browser is being managed. Administrators can disable this notice with the **NTPFooterManagementNoticeEnabled** policy. Additionally, organizations can customize the footer's appearance using the **EnterpriseLogoUrlForBrowser** and **EnterpriseCustomLabelForBrowser** policies to display a custom logo and label.
    - Chrome 140 on Linux, macOS, Windows: A default notice (_Managed by <domain name>_) will start to be shown in the **New tab** page footer for all managed browsers. Visibility can be changed with the **NTPFooterManagementNoticeEnabled** policy.

* **Search your screen with Google Lens on iPad**
  • Type: Chrome Browser changes
  • Platform: Mobile (iOS)
  • Update: Expand **Search your screen with Google Lens** on iOS so it is available on iPad devices. iPad is a form factor typically associated with more complex tasks, for example, shopping, and expanding Lens functionality on iPad enables users to perform these tasks easily. Admins can control this feature using the [LensOverlaySettings](https://chromeenterprise.google/policies/#LensOverlaySettings) policy.
    - **Chrome 138 on iOS:** Feature rolls out gradually.

* **Shared tab groups**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android, iOS)
  • Update: Users can now collaborate on tabs using the shared tab groups feature. With this feature, users can create and use a set of tabs on their desktop or mobile device and their collaborative partners can browse the same tabs on their devices. When one person changes a tab in the group, the changes are reflected across all users' browsers in the group. An enterprise policy, TabGroupSharingSettings, is available to control this feature.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:** Rollout of the ability to join and use a shared tab group. Users on Stable Chrome will not be able to create a shared tab group (the entry point will not be available) - this part of the feature will only be available on Beta/Dev/Canary for this phase of rollout.
    - Chrome 139 on iOS: As early as Chrome 139, support for iOS will roll out.

* **Speculation rules prefetch for ServiceWorker**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: This feature enables Service Worker-controlled prefetches, that is, a speculation rules prefetch to URLs controlled by a Service Worker. Previously, the prefetch is cancelled upon detecting a controlling Service Worker, thus subsequent navigation to the prefetch target is served by the non-prefetch path. This feature enables the prefetch request to go through the Service Worker's fetch handler and the response with the Service Worker interception is cached in the prefetch cache, resulting in a subsequent navigation being served by the prefetch cache. Please use the enterprise policy [PrefetchWithServiceWorkerEnabled](https://chromeenterprise.google/policies/#PrefetchWithServiceWorkerEnabled) to control this feature. For more details, see [this](https://docs.google.com/document/d/192ZLkKcaUE_9Qt8bW9OZLViEEbtxOAgq5WYR87m79IE/edit?tab=t.0#heading=h.8i2u299uv5yh) explainer.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows**

* **Summarizer API**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: Summarizer API is a JavaScript API for producing summaries of input text, backed by an AI language model. Browsers and operating systems are increasingly expected to gain access to a language model. By exposing this built-in model, we avoid every website needing to download their own multi-gigabyte language model, or send input text to third-party APIs. The Summarizer API, in particular, exposes a high-level API for interfacing with a language model to summarize inputs for a variety of use cases ([Github](https://github.com/webmachinelearning/writing-assistance-apis/blob/main/README.md#summarizer-api)), in a way that does not depend on a specific language model.
    An enterprise policy ([GenAILocalFoundationalModelSettings](https://chromeenterprise.google/policies/#GenAILocalFoundationalModelSettings)) is available to disable the underlying model downloading, which would render this API unavailable.
    - **Chrome 138 on Windows, macOS, Linux**

* **TLS 1.3 Early Data**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: TLS 1.3 Early Data allows GET requests to be sent during the handshake when resuming a connection to a compatible TLS 1.3 server. The feature is expected to demonstrate performance improvements and will be available in Chrome 138 with a policy ([TLS13EarlyDataEnabled](https://chromeenterprise.google/policies/#TLS13EarlyDataEnabled)) to control this change.
    TLS 1.3 Early Data is an established protocol. Existing TLS servers, middleboxes, and security software are expected to either handle or reject TLS 1.3 Early Data without dropping the connection. However, devices that do not correctly implement the TLS standard (RFC8446) might malfunction and disconnect when TLS 1.3 Early Data is in use. If this occurs, administrators should contact the vendor for a fix.
    The [TLS13EarlyDataEnabled](https://chromeenterprise.google/policies/#TLS13EarlyDataEnabled) policy is a temporary measure to control the feature and will be removed in a future milestone. You can turn on the feature using the policy to allow you to test for issues and turn it off again as issues are resolved.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows**

* **Translator API**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: Translator API is a JavaScript API to provide language translation capabilities to web pages. Browsers are increasingly offering language translation to their users. Such translation capabilities can also be useful to web developers. This is especially the case when the browser's built-in translation abilities cannot help. An enterprise policy, [GenAILocalFoundationalModelSettings](https://chromeenterprise.google/policies/#GenAILocalFoundationalModelSettings), is available to disable the underlying model downloading, which would render this API unavailable.
    - **Chrome 138 on Windows, macOS, Linux**

* **Upcoming Chrome browser changes**
  • Type: Chrome Browser changes
  • Update: 

* **Web serial over Bluetooth on Android**
  • Type: Chrome Browser changes
  • Platform: Mobile (Android)
  • Update: This feature allows web pages and web apps to connect to serial ports over Bluetooth on Android devices. Chrome on Android now supports Web Serial API over Bluetooth RFCOMM. Existing enterprise policies ([DefaultSerialGuardSetting](https://chromeenterprise.google/policies/#DefaultSerialGuardSetting), [SerialAllowAllPortsForUrls](https://chromeenterprise.google/policies/#SerialAllowAllPortsForUrls), [SerialAllowUsbDevicesForUrls](https://chromeenterprise.google/policies/#SerialAllowUsbDevicesForUrls), [SerialAskForUrls](https://chromeenterprise.google/policies/#SerialAskForUrls) and [SerialBlockedForUrls](https://chromeenterprise.google/policies/#SerialBlockedForUrls)) on other platforms are enabled in future_on states for Android. All policies except [SerialAllowUsbDevicesForUrls](https://chromeenterprise.google/policies/#SerialAllowUsbDevicesForUrls) will be enabled after the feature is enabled. [SerialAllowUsbDevicesForUrls](https://chromeenterprise.google/policies/#SerialAllowUsbDevicesForUrls) will be enabled in a future launch after Android provides system level support of wired serial ports.
    - **Chrome 138 on Android**


---

### Security/Privacy

**Current — Chrome 138**

* **# Malicious APK download checks**
  • Type: Chrome Browser changes
  • Platform: Mobile (Android)
  • Update: Chrome on Android will now contact Google servers about APK files downloaded in Chrome, to get a verdict about their safety. If a downloaded APK file is determined to be dangerous, Chrome will show a warning and block the download, to protect users against mobile malware. Such download warnings will be bypassable by the user through the Chrome UI. These malicious APK download checks will be performed for users enrolled in Standard Protection or Enhanced Protection from Google Safe Browsing. This feature can be disabled by setting the Safe Browsing mode to "No Protection" via the [SafeBrowsingProtectionLevel](https://chromeenterprise.google/policies/#SafeBrowsingProtectionLevel) policy.
    - **Chrome 139 on Android**

* **# Migrate extensions to Manifest V3 before June 2025**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: Extensions must be updated to leverage Manifest V3. Chrome extensions are transitioning to a new manifest version, Manifest V3. This will bring improved privacy for your users—for example, by moving to a model where extensions modify requests declaratively, without the ability to see individual requests. This also improves extension security, as remotely hosted code will be disallowed on Manifest V3.
    In June 2024, Chrome began to gradually disable Manifest V2 extensions running in the browser. An Enterprise policy - [ExtensionManifestV2Availability](https://chromeenterprise.google/policies/#ExtensionManifestV2Availability) - can be used to test Manifest V3 in your organization ahead of the migration. Additionally, machines on which the policy is enabled will not be subject to the disabling of Manifest V2 extensions until the following year - June 2025 - at which point the policy will be removed.
    You can see which Manifest version is being used by all Chrome extensions running on your fleet using the Apps & extensions usage page in Chrome Enterprise Core.
    - Chrome 127 on ChromeOS, LaCrOS, Linux, macOS, Windows: Chrome will gradually disable Manifest V2 extensions on user devices. Only those with the [ExtensionManifestV2Availability](https://chromeenterprise.google/policies/#ExtensionManifestV2Availability) enterprise policy enabled would be able to continue using Manifest V2 extensions in their organization.
    - **Chrome 139 on ChromeOS, Linux, macOS, Windows:** Remove [ExtensionManifestV2Availability](https://chromeenterprise.google/policies/#ExtensionManifestV2Availability) policy.
    [Content continues with remaining sections...]

* **# Upcoming change for CA certificates included in the Chrome Root Store**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: In response to sustained compliance failures, Chrome 139 changes how publicly-trusted TLS server authentication, that is, websites or certificates issued by Chunghwa Telecom and Netlock, are trusted by default. This applies to Chrome 139 and later on Windows, macOS, ChromeOS, Android, and Linux; iOS policies do not allow use of the Chrome Root Store in Chrome for iOS.
    Specifically, TLS certificates validating to the Chunghwa Telecom or Netlock root CA certificates included in the Chrome Root Store and issued:
    - after July 31, 2025, will no longer be trusted by default.
    - on or before July 31, 2025, will be unaffected by this change.
    If a Chrome user or an enterprise explicitly trusts any of the affected Chunghwa Telecom or Netlock certificates on a platform and version of Chrome relying on the Chrome Root Store, for example, when explicit trust is conveyed through a Windows Group Policy Object, the Signed Certificate Timestamp (SCT) constraints described above will be overridden and certificates will function as they do today.
    For additional information and testing resources, see [Sustaining Digital Certificate Security - Upcoming Changes to the Chrome Root Store](https://security.googleblog.com/2025/05/sustaining-digital-certificate-security-chrome-root-store-changes.html).
    To learn more about the Chrome Root Store, see this [FAQ](https://chromium.googlesource.com/chromium/src/+/main/net/data/ssl/chrome_root_store/faq.md).
    - **Chrome 139 on Android, ChromeOS, Linux, macOS, Windows:** All versions of Chrome 139 and higher that rely on the Chrome Root Store will honor the blocking action, but the blocking action will only begin for certificates issued after July 31, 2025.

* **Bookmarks and reading list improvements on Chrome Desktop**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: For Chrome 138 on Desktop, some users who sign in to Chrome upon saving a new bookmark can now use and save bookmarks and reading list items in their Google Account. Relevant enterprise policies controlling bookmarks, as well as [BrowserSignin](https://chromeenterprise.google/policies/#BrowserSignin), [SyncDisabled](https://chromeenterprise.google/policies/#SyncDisabled) or [SyncTypesListDisabled](https://chromeenterprise.google/policies/#SyncTypesListDisabled), continue to work as before, so admins can configure whether or not users can use and save items in their Google Account. Setting [EditBookmarksEnabled](https://chromeenterprise.google/policies/#EditBookmarksEnabled) to false also prevents users from uploading a bookmark saved on their device to their Google Account.
    - **Chrome 138 on Linux, macOS, Windows**

* **Client's LLM assistance in mitigating scams**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: Users on the web are facing significant amounts of different kinds of scams a day. To combat these scams, Chrome now uses on-device LLM to identify scam websites for Enhanced Safe Browsing users. Chrome sends the page content to an on-device LLM to infer security-related signals of the page and send these signals to the Safe Browsing server for a final verdict. When enabled, Chrome can consume more bandwidth to download the LLM.
    Enhanced Safe Browsing is an existing feature, controlled by the [SafeBrowsingProtectionLevel](https://chromeenterprise.google/policies/#SafeBrowsingProtectionLevel) policy.
    - Chrome 134 on Linux, macOS, Windows: Gather the brand name and intent summary of the page that triggers keyboard lock to identify scam websites.
    - Chrome 135 on Linux, macOS, Windows: Show the warnings to the user based on the server verdict, which uses the brand and intent summary of the page that triggered keyboard lock.
    - Chrome 137 on Linux, macOS, Windows: Gather brand and intent summary of the page based on server reputation scoring system.
    - **Chrome 138 on Linux, macOS, Windows**: Show the warnings to the user based on the server verdict, which uses the brand and intent of the pages that the server reputation system scored.

* **DLP Download Support for File System Access API (FSA)**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: Data Loss Prevention (DLP) protection now covers files and directories downloaded using the [File System Access (FSA) API](https://developer.chrome.com/docs/capabilities/web-apis/file-system-access). This enhancement ensures that downloads from modern web applications, such as browser-based editors, are scanned according to your organization's DLP rules. Users and websites receive notifications on scan verdicts, strengthening data security and compliance. If a download violates a DLP policy, it is blocked, resulting in an empty file, and the website might indicate a "Blocked by Safe Browsing" error. This change primarily benefits security by preventing data exfiltration through this vector. Administrators should test this with web applications using the FSA API to observe the behavior with their current DLP configurations.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Enables DLP content analysis for downloads initiated via File System Access API on selected platforms, governed by existing enterprise policies.

* **Deprecate asynchronous range removal for Media Source extensions**
  • Type: Chrome Browser changes
  • Platform: Desktop (Linux, Windows, macOS), Mobile (Android)
  • Update: The [Media Source standard](https://www.w3.org/TR/media-source-2/) changed in the past to disallow ambiguously-defined behavior involving asynchronous range removals:
    - `SourceBuffer.abort()` no longer aborts `SourceBuffer.remove()` operations
    - Setting `MediaSource.duration` can no longer truncate currently buffered media
    Exceptions are thrown in both of these cases now. Safari and Firefox have long shipped this behavior; Chromium is the last browser remaining with the old behavior. Use counters show ~0.001%-0.005% of page loads hit the deprecated behavior. If a site hits this issue, playback may now break. Usage of abort() cancelling removals is increasing, so it's prudent to resolve this deprecation before more incompatible usage appears.
    - **Chrome 138 on Windows, macOS, Linux, Android**

* **Enhanced Safe Browsing is a synced setting**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: In Chrome 138, Chrome's Enhanced Safe Browsing is a synced feature. This means that if a user opts into Enhanced Safe Browsing on one device, this protection level automatically applies across all other devices where they are signed into Chrome with the same account. The goal is to provide stronger, more consistent security protection and a standardized user experience.
    Users who enable Enhanced Safe Browsing benefit from its protections, for example, proactive phishing protection, improved detection of malware and malicious extensions consistently across their synced Chrome instances on Desktop (Windows, macOS, Linux, ChromeOS), Android, and iOS. Users receive onscreen notifications when their Enhanced Safe Browsing setting is synced.
    The Safe Browsing protection level is an existing feature, controlled by the [SafeBrowsingProtectionLevel](https://chromeenterprise.google/policies/#SafeBrowsingProtectionLevel) policy.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows**

* **Inactive profile deletion in Chrome Enterprise Core**
  • Type: Chrome Enterprise Core changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: In June 2025, the inactive period for profile deletion setting started to roll out. In July 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. The inactivity period of time has a default value of 90 days. By default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value using this setting. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.
    If you lower the set value, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is re-activated on a device, that profile will reappear in the console.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:** Policy will roll out in June. Deletion will start in July and the initial wave of deletion will complete by the end of August. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

* **New LayerX risk assessment in the Admin console**
  • Type: Chrome Enterprise Core changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: We are adding a new extension risk assessment provider: LayerX Security to the Admin console. This score is available to Admins in the Apps and Extensions Usage report.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** The score would be available to admins as early as Chrome 138.

* **New tab page footer**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: An update to the **New tab** page includes a new footer designed to provide users with greater transparency and control over their Chrome experience.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Extension Attribution will begin to show on the NTP. If an extension has changed your default **New tab** page, you'll now see a message in the footer that attributes the change to that specific extension. This message often includes a link directly to the extension in the Chrome Web Store, making it easier to identify and manage unwanted extensions. If you're an administrator, you can disable this attribution using the [NTPFooterExtensionAttributionEnabled](https://chromeenterprise.google/policies/#NTPFooterExtensionAttributionEnabled) policy.
    - Chrome 139 on Linux, macOS, Windows: Browser management disclosure will be shown if one of the policies to customize the footer is set by an enterprise admin. For users whose Chrome browser is managed by a trusted source, the **New tab** page footer will now display a management disclosure notice. This helps you understand how your browser is being managed. Administrators can disable this notice with the **NTPFooterManagementNoticeEnabled** policy. Additionally, organizations can customize the footer's appearance using the **EnterpriseLogoUrlForBrowser** and **EnterpriseCustomLabelForBrowser** policies to display a custom logo and label.
    - Chrome 140 on Linux, macOS, Windows: A default notice (_Managed by <domain name>_) will start to be shown in the **New tab** page footer for all managed browsers. Visibility can be changed with the **NTPFooterManagementNoticeEnabled** policy.

* **Per-extension user script toggle**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: In Chrome 138, the way that users and administrators control an extension's ability to run user created scripts and use the [userScripts API](https://developer.chrome.com/docs/extensions/reference/api/userScripts) is changing. This change enhances security. Users won't unintentionally grant user script permissions to every extension when enabling **Developer mode** by explicitly deciding which extensions can run these potentially powerful scripts. For more detail on the motivation for the change, see this [Chrome for developers](https://developer.chrome.com/blog/chrome-userscript) blog.
    End users will now toggle this per extension on the `chrome://extensions` page via a **Allow User Scripts** toggle, replacing the global **Developer mode** toggle for more granular control. Existing extensions will have this toggle automatically enabled if **Developer mode** is on and the extension has been granted the User Scripts permission.
    Administrators who currently manage user scripts by disabling developer mode should now use the [blocked_permissions field of the](https://support.google.com/chrome/a/answer/9867568) [ExtensionSettings policy](https://cloud.google.com/docs/chrome-enterprise/policies/?policy=ExtensionSettings) or the [Google Admin console](https://support.google.com/chrome/a/answer/7515036) to independently control the User Scripts permission and extension **Developer mode**.
    Extension developers are advised to update their documentation to reflect the new toggle. See the [Chromium Extensions Google Groups](https://groups.google.com/a/chromium.org/g/chromium-extensions) mailing list for more information and other changes to usage of the API.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Feature rolls out

* **Removal of Private Network Access enterprise policies**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: Private Network Access (PNA 1.0) is an unshipped security feature designed to limit website access to local networks. Due to deployability concerns, PNA 1.0 was never able to ship by default, as it was incompatible with too many existing devices.
    PNA 1.0 required changes to devices on local networks. Instead, Chrome is implementing an updated proposal, Private Network Access 2.0 (PNA 2.0) ([Github](https://github.com/explainers-by-googlers/local-network-access)). PNA 2.0 only requires changes to sites that need to access the local network, rather than requiring changes to devices on the local network. Sites are much easier to update than devices, and so this approach should be much more straightforward to roll out.
    The only way to enforce PNA 1.0 is via enterprise policy. To avoid regressing security for enterprise customers opting-in to PNA 1.0 prior to shipping PNA 2.0, we will maintain the [PrivateNetworkAccessRestrictionsEnabled](https://chromeenterprise.google/policies/#PrivateNetworkAccessRestrictionsEnabled) policy, which causes Chrome to send special preflight messages, until such time that it becomes incompatible with PNA 2.0.
    The [InsecurePrivateNetworkRequestsAllowedForUrls](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowedForUrls) and [InsecurePrivateNetworkRequestsAllowed](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowed) policies, which loosen PNA 1.0 restrictions, will be removed immediately. These policies currently have no effect, since PNA 1.0 is not shipped, and they will have no meaning once PNA 1.0 is removed.
    - Chrome 135 on Android, ChromeOS, Linux, macOS, Windows, Fuchsia: Deprecate [InsecurePrivateNetworkRequestsAllowedForUrls](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowedForUrls), [InsecurePrivateNetworkRequestsAllowed](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowed), and [PrivateNetworkAccessRestrictionsEnabled](https://chromeenterprise.google/policies/#PrivateNetworkAccessRestrictionsEnabled) policies.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows, Fuchsia:** Removal of [PrivateNetworkAccessRestrictionsEnabled](https://chromeenterprise.google/policies/#PrivateNetworkAccessRestrictionsEnabled), [InsecurePrivateNetworkRequestsAllowedForUrls](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowedForUrls) and [InsecurePrivateNetworkRequestsAllowed](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowed). There should be a PNA2 replacement policy available in Chrome 138.

* **SecOps integration**
  • Type: Chrome Enterprise Premium changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: This feature delivers a native integration between Chrome Enterprise Premium (CEP) and Google Security Operations (SecOps), enabling organizations to send a richer set of security events and detailed browser telemetry from Chrome directly to their SecOps instance. The motivation for this change is to use the browser as a primary security sensor for web-based threats like phishing, malware, and data exfiltration. This can significantly improve an organization's ability to:
    - prevent
    - detect
    - investigate
    - and respond to web-based threats.
    For administrators, this integration introduces new, enhanced security event types, including URL navigation telemetry and suspicious URL visits. These events are automatically enriched with Safe Browsing risk scores and other threat intelligence before being sent to SecOps. The launch also includes a new, streamlined "one-click" setup process in the Admin console to replace the previous manual workflow, simplifying the connection to SecOps.
    To use this feature, administrators must have a Chrome Enterprise Premium subscription and will need to enable the integration through the new workflow in the Admin console. The collection of certain high-volume event types, such as URL navigation events, is an opt-in setting within the connector configuration. This feature does not add or modify any enterprise policies.
    - Chrome 137 on Linux, macOS, Windows: Adds referrer data to `URLFilteringInterstitialEvent` and `SafeBrowseInterstitialEvent`
    - **Chrome 138 on Linux, macOS, Windows:** Extends referrer data population to `SafeBrowseDangerousDownloadEvent` and `DlpSensitiveDataEvent`

* **URL Filtering capabilities on iOS**
  • Type: Chrome Enterprise Premium changes
  • Platform: Mobile (iOS)
  • Update: The current WebProtect URL Filtering capabilities on Desktop are being extended to mobile so that organizations can audit, warn, or block certain URLs or categories of URLs from loading on managed Chrome browsers or managed user profiles on mobile devices. This feature is part of Chrome Enterprise Premium and aims to provide secure and safe internet access for enterprise users on any device. Admins can create URL filtering rules to ensure that employees can only access safe and authorized URLs on iOS devices. Chrome reports URL filtering events and unsafe site events via the Reporting Connector on mobile. This feature allows administrators to manage which URLs can be accessed on managed Chrome browsers or profiles on company-owned or BYOD iOS devices.
    Key changes include:
    - Admins can block, warn, or audit users when accessing certain sites or categories.
    - Users see interstitial pages when attempting to visit blocked or warned URLs.
    - Chrome reports URL filtering events.
    - Updates to the `chrome://management` page reflect the new functionality.
    - **Chrome 138 on iOS:** The URL Filtering feature becomes available on iOS.


---

### Management

**Current — Chrome 138**

* **Deprecation of the Chrome browser page on the Chrome Insights report**
  • Type: Chrome Enterprise Core changes
  • Platform: Desktop (Linux, Windows, macOS), Mobile (Android, iOS)
  • Update: As early as July 1st, the Chrome browser page on the Chrome Insights report will be deprecated. This page is replaced by the Chrome **Overview** page that was launched in Chrome 137. The information, which was displayed on the Chrome browser page of the Chrome Insights report, can now be found on the **Overview** page.
    - **Chrome 138 on Android, iOS, Linux, macOS, Windows**

* **Generating insights for Chrome DevTools console warnings and errors**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: A new Generative AI (GenAI) feature is now available for unmanaged users: Generating insights for Chrome [DevTools console warnings and errors](https://developer.chrome.com/docs/devtools/console/understand-messages). These insights provide a personalized description and suggested fixes for the selected errors and warnings. Initially, this feature is available to users (18+) in English only. Admins can control this feature using the [DevToolsGenAiSettings](https://chromeenterprise.google/policies/#DevToolsGenAiSettings) policy.
    - Chrome 131 on ChromeOS, Linux, macOS, Windows: In Chrome 131, a new Generative AI (GenAI) feature becomes available for managed users: a dedicated _AI assistance_ panel in Chrome DevTools which assists the human operator investigating & fixing styling challenges and helps debugging the CSS.
    - Chrome 132 on ChromeOS, Linux, macOS, Windows: The AI assistance panel can now explain resources in the Performance panel, Sources panel, and Network panel, in addition to the previous support for style debugging.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** The AI assistance panel exposes an internal API that simplifies the use of AI assistance panel features by external tools such as Model Context Protocol (MCP) servers.

* **Inactive profile deletion in Chrome Enterprise Core**
  • Type: Chrome Enterprise Core changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
  • Update: In June 2025, the inactive period for profile deletion setting started to roll out. In July 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. The inactivity period of time has a default value of 90 days. By default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value using this setting. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.
    If you lower the set value, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is re-activated on a device, that profile will reappear in the console.
    - **Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:** Policy will roll out in June. Deletion will start in July and the initial wave of deletion will complete by the end of August. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

* **New policies in Chrome browser**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: 新增策略: AIModeSettings, PdfAnnotationsEnabled, TLS13EarlyDataEnabled, NTPFooterExtensionAttributionEnabled, PrefetchWithServiceWorkerEnabled, EnterpriseRealTimeUrlCheckMode, LocalNetworkAccessRestrictionsEnabled, PrivacySandboxIpProtectionEnabled, PasswordManagerBlocklist

* **New tab page footer**
  • Type: Chrome Browser changes
  • Platform: Desktop (ChromeOS, Linux, Windows, macOS)
  • Update: An update to the **New tab** page includes a new footer designed to provide users with greater transparency and control over their Chrome experience.
    - **Chrome 138 on ChromeOS, Linux, macOS, Windows:** Extension Attribution will begin to show on the NTP. If an extension has changed your default **New tab** page, you'll now see a message in the footer that attributes the change to that specific extension. This message often includes a link directly to the extension in the Chrome Web Store, making it easier to identify and manage unwanted extensions. If you're an administrator, you can disable this attribution using the [NTPFooterExtensionAttributionEnabled](https://chromeenterprise.google/policies/#NTPFooterExtensionAttributionEnabled) policy.
    - Chrome 139 on Linux, macOS, Windows: Browser management disclosure will be shown if one of the policies to customize the footer is set by an enterprise admin. For users whose Chrome browser is managed by a trusted source, the **New tab** page footer will now display a management disclosure notice. This helps you understand how your browser is being managed. Administrators can disable this notice with the **NTPFooterManagementNoticeEnabled** policy. Additionally, organizations can customize the footer's appearance using the **EnterpriseLogoUrlForBrowser** and **EnterpriseCustomLabelForBrowser** policies to display a custom logo and label.
    - Chrome 140 on Linux, macOS, Windows: A default notice (_Managed by <domain name>_) will start to be shown in the **New tab** page footer for all managed browsers. Visibility can be changed with the **NTPFooterManagementNoticeEnabled** policy.

* **Removed policies in Chrome browser**
  • Type: Chrome Browser changes
  • Update: | Policy | Description |
    |--------|-------------|
    | [PrivateNetworkAccessRestrictionsEnabled](https://chromeenterprise.google/policies/#PrivateNetworkAccessRestrictionsEnabled) | Apply restrictions to requests to more-private network endpoints. |
    | [InsecurePrivateNetworkRequestsAllowed](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowed) | Allow websites to make requests to more-private network endpoints in an insecure manner. |
    | [InsecurePrivateNetworkRequestsAllowedForUrls](https://chromeenterprise.google/policies/#InsecurePrivateNetworkRequestsAllowedForUrls) | Allow the listed sites to make requests to more-private network endpoints in an insecure manner. |

* **SecOps integration**
  • Type: Chrome Enterprise Premium changes
  • Platform: Desktop (Linux, Windows, macOS)
  • Update: This feature delivers a native integration between Chrome Enterprise Premium (CEP) and Google Security Operations (SecOps), enabling organizations to send a richer set of security events and detailed browser telemetry from Chrome directly to their SecOps instance. The motivation for this change is to use the browser as a primary security sensor for web-based threats like phishing, malware, and data exfiltration. This can significantly improve an organization's ability to:
    - prevent
    - detect
    - investigate
    - and respond to web-based threats.
    For administrators, this integration introduces new, enhanced security event types, including URL navigation telemetry and suspicious URL visits. These events are automatically enriched with Safe Browsing risk scores and other threat intelligence before being sent to SecOps. The launch also includes a new, streamlined "one-click" setup process in the Admin console to replace the previous manual workflow, simplifying the connection to SecOps.
    To use this feature, administrators must have a Chrome Enterprise Premium subscription and will need to enable the integration through the new workflow in the Admin console. The collection of certain high-volume event types, such as URL navigation events, is an opt-in setting within the connector configuration. This feature does not add or modify any enterprise policies.
    - Chrome 137 on Linux, macOS, Windows: Adds referrer data to `URLFilteringInterstitialEvent` and `SafeBrowseInterstitialEvent`
    - **Chrome 138 on Linux, macOS, Windows:** Extends referrer data population to `SafeBrowseDangerousDownloadEvent` and `DlpSensitiveDataEvent`

* **URL Filtering capabilities on iOS**
  • Type: Chrome Enterprise Premium changes
  • Platform: Mobile (iOS)
  • Update: The current WebProtect URL Filtering capabilities on Desktop are being extended to mobile so that organizations can audit, warn, or block certain URLs or categories of URLs from loading on managed Chrome browsers or managed user profiles on mobile devices. This feature is part of Chrome Enterprise Premium and aims to provide secure and safe internet access for enterprise users on any device. Admins can create URL filtering rules to ensure that employees can only access safe and authorized URLs on iOS devices. Chrome reports URL filtering events and unsafe site events via the Reporting Connector on mobile. This feature allows administrators to manage which URLs can be accessed on managed Chrome browsers or profiles on company-owned or BYOD iOS devices.
    Key changes include:
    - Admins can block, warn, or audit users when accessing certain sites or categories.
    - Users see interstitial pages when attempting to visit blocked or warned URLs.
    - Chrome reports URL filtering events.
    - Updates to the `chrome://management` page reflect the new functionality.
    - **Chrome 138 on iOS:** The URL Filtering feature becomes available on iOS.

