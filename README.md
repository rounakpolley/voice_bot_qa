# voice_bot_qa

QA pipeline and dashboards for the **Vani_buyer_bot** voice agent (VANI Call Quality Matrix).

## Layout
- `dashboard/vani-buyer-bot-dashboard.html` — the latest audit dashboard (self-contained; open in a browser). Written by the daily audit job.
- `pipeline/template.html` — the dashboard template.
- `pipeline/audit_dashboard.py` — merges a run JSON into the dashboard.
- `pipeline/run.json` — the run data behind the committed dashboard.
- `README.md` — this file.

## How the dashboard is produced
1. The agent audits Vani_buyer_bot's calls (Sarvam Voice Agents, app id `Vani-buyer--d5064c4c-fb6a`) and writes a run JSON (schema in the `call-log-issue-analysis` skill, `references/run-schema.md`).
2. Merge it:
   `python3 pipeline/audit_dashboard.py --data run.json --html dashboard/vani-buyer-bot-dashboard.html --out dashboard/vani-buyer-bot-dashboard.html`
3. Commit the refreshed `dashboard/vani-buyer-bot-dashboard.html` to `main`.

## Keeping it synced
The daily "Audit" job commits the refreshed dashboard to this repo after every run, so
`dashboard/vani-buyer-bot-dashboard.html` on `main` is always the latest version.
