# Scheduled Release Check Workflow

## Overview
- Use GitHub Actions to poll a release endpoint on a recurring schedule.
- Scheduled runs rely on cron expressions; outbound HTTP is available on hosted runners.

## Suggested Workflow YAML
```yaml
name: Scheduled Release Check

on:
  schedule:
    - cron: '0 9 */2 * *'   # every other day at 09:00 UTC
  workflow_dispatch:

jobs:
  check-release:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch latest release
        uses: actions/github-script@v7
        with:
          script: |
            const url = 'https://api.github.com/repos/OWNER/REPO/releases/latest';
            const res = await fetch(url, { headers: { 'User-Agent': 'actions' } });
            if (!res.ok) core.setFailed(`HTTP ${res.status}`);
            const latest = await res.json();
            core.info(`Latest tag: ${latest.tag_name}`);
            // TODO: add any custom comparison + notification logic here
```

## Additional Notes
- Cron cannot run exactly every 48 hours across month boundaries; this expression fires roughly every two days.
- Store tokens or webhook URLs in repository secrets if the endpoint needs authentication or you plan to notify external services.
- Extend the script section to compare against persisted state or trigger alerts (issues, PRs, chat hooks) when a new tag appears.
