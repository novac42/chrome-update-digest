# Inactive profile deletion in Chrome Enterprise Core

**Relevance Score**: 60.0

**Type**: Chrome Browser changes
**Platform**: Desktop (ChromeOS, Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: User productivity/Apps
**Matched Keywords**: profile, account

**Description**:
In June 2025, the inactive period for profile deletion setting started to roll out. In July 2025, the setting will begin to automatically delete managed profiles in the Admin console that have been inactive for more than the defined inactivity period. When releasing the setting, the inactivity period of time has a default value of 90 days. Meaning that by default, all managed profiles that have been inactive for more than 90 days are deleted from your account. Administrators can change the inactive period value using this setting. The maximum value to determine the profile inactivity period is 730 days and the minimum value is 28 days.If you lower the set value, it might have a global impact on any currently managed profiles. All impacted profiles will be considered inactive and, therefore, be deleted. This does not delete the user account. If an inactive profile is re-activated on a device, that profile will reappear in the console.Chrome 138 on Android, ChromeOS, Linux, macOS, Windows:Policy will roll out in June. Deletion will start in July and the initial wave of deletion will complete by the end of August. After the initial deletion rollout, inactive profiles will continue to be deleted once they have reached their inactivity period.

**Key Context**: Inactive **profile** deletion in Chrome Enterprise Core In June 2025, the inactive period for **profile** deletion setting s | y default, all managed profiles that have been inactive for more than 90 days are deleted from your **account**. Administrators can change the inactive period value using this setting. The maximum value to deter
