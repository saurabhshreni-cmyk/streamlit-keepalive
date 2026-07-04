# Streamlit Keep-Alive

Keeps Streamlit Community Cloud apps awake so their links load instantly for anyone who opens them.

[![Keep Streamlit apps awake](https://github.com/saurabhshreni-cmyk/streamlit-keepalive/actions/workflows/keepalive.yml/badge.svg)](https://github.com/saurabhshreni-cmyk/streamlit-keepalive/actions/workflows/keepalive.yml)

## Overview

Streamlit Community Cloud apps go to sleep after a period of inactivity, which makes demo and portfolio links slow or broken the first time someone clicks them. This project runs a scheduled GitHub Actions job that visits each app in a headless browser and wakes it if it has gone to sleep, keeping every link warm and instantly loadable.

## Why a headless browser (not a simple ping)

A plain HTTP request to a sleeping app returns `200 OK` with only a static HTML shell — it never starts the underlying Python process, so the app stays asleep. Waking the app requires a real browser visit that renders the page and clicks the "Yes, get this app back up!" button. Playwright driving headless Chromium provides exactly that.

## How it works

1. A cron schedule triggers the workflow every 4 hours (and it can be run manually on demand).
2. GitHub spins up a fresh Ubuntu runner.
3. The runner installs Python 3.12 and Playwright with headless Chromium.
4. It runs `wake.py`, which visits each app URL.
5. If the wake button is present, the script clicks it and waits for the app to come back up.

```
cron → Ubuntu runner → Playwright (headless Chromium) → visit each app → wake if asleep
```

## Tech stack

- Python
- Playwright (headless Chromium)
- GitHub Actions

## Configuration

To add or remove an app, edit the `APPS` list in `wake.py` and push. The next scheduled run picks up the change automatically.

```python
APPS = [
    "https://turboquant-vit.streamlit.app",
    "https://skin-cancer-detection-saurabh.streamlit.app",
    # "https://your-new-app.streamlit.app",
]
```

## Local usage (optional)

The automation runs in the cloud on a schedule regardless, but the script can also be run locally:

```bash
pip install playwright
python -m playwright install chromium
python wake.py
```

## Notes

- Scheduled runs can be delayed during GitHub's peak times; the 4-hour interval absorbs this while staying well within the app sleep window.
- GitHub disables scheduled workflows after 60 days of no repository activity; any push re-enables them.
- No secrets or credentials are stored in this repository.
