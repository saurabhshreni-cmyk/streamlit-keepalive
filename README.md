# streamlit-keepalive

Keeps my [Streamlit Community Cloud](https://streamlit.io/cloud) apps from going to
sleep, so their links always load instantly for anyone who clicks them.

## How it works

Free-tier Streamlit apps go to sleep after a period of inactivity. A plain HTTP
"ping" does **not** wake them — the server returns `200 OK` with a static HTML
shell without actually starting the Python app. So this repo drives a **real
headless browser** (Playwright + Chromium) that:

1. Visits each app URL.
2. Detects the **"Yes, get this app back up!"** button (it only appears when an
   app is asleep).
3. Clicks it to wake the app if needed.

A [GitHub Actions](.github/workflows/keepalive.yml) workflow runs this on a
schedule — **every 4 hours** — and can also be triggered manually from the
**Actions** tab ("Run workflow"). Because the repo is **public**, GitHub Actions
minutes are free and unlimited.

## Currently keeping awake

- https://turboquant-vit.streamlit.app
- https://skin-cancer-detection-saurabh.streamlit.app

## Add or remove an app

1. Edit the `APPS` list in [`wake.py`](wake.py).
2. Commit and push. That's it — the next scheduled run picks up the change.

```python
APPS = [
    "https://turboquant-vit.streamlit.app",
    "https://skin-cancer-detection-saurabh.streamlit.app",
    # "https://your-new-app.streamlit.app",
]
```

## Notes

- **No secrets.** There are no passwords, tokens, or API keys in this repo —
  nothing sensitive is committed.
- **Scheduled workflows auto-disable** after 60 days of no repo activity. Any
  push re-enables them.
- Free-tier scheduled runs can be delayed at GitHub's peak times; the 4-hour
  interval absorbs that.
