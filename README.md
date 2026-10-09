# voice_bot_qa

QA pipeline and dashboards for the **Ron** voice bot (VANI Call Quality Matrix).

## Layout
- `dashboard/ron-audit-dashboard.html` — the latest audit dashboard (self-contained; open in a browser).
- `dashboard/ron-recordings-transcripts.txt` — ASR transcripts for the recordings sample.
- `pipeline/template.html` — the dashboard template.
- `pipeline/ron_audit_dashboard.py` — merges a run JSON into the dashboard.
- `pipeline/run.json` — the run data behind the committed dashboard.
- `README.md` — this file.

## How the dashboard is produced
1. The agent audits the calls and writes a run JSON (schema in the `call-log-issue-analysis` skill, `references/run-schema.md`).
2. Merge it:
   `python3 pipeline/ron_audit_dashboard.py --data run.json --html dashboard/ron-audit-dashboard.html --out dashboard/ron-audit-dashboard.html`
3. Commit the refreshed `dashboard/ron-audit-dashboard.html` to `main`.

## Keeping it synced
The agent commits the refreshed dashboard to this repo after every audit run, so
`dashboard/ron-audit-dashboard.html` on `main` is always the latest version.
