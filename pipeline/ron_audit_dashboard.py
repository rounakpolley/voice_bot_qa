#!/usr/bin/env python3
"""Rolling Ron / VANI audit dashboard.

Merges one audit run into the dashboard's embedded history and writes a new,
self-contained HTML file. Runs are keyed by their `id` (use the run timestamp,
e.g. "2026-10-10T09:00"); re-running with the same id replaces that run.

  python3 scripts/ron_audit_dashboard.py --data run.json --html existing.html --out dashboard.html

--data  JSON for one run (an object with "id") or {"params": [...], "runs": [...]}.
--html  Previous dashboard. Its history and layout are kept. If omitted, the
        template.html next to this script is used and history starts empty.
"""
import argparse, json, os, re, sys

MARK_RE = re.compile(r'(<script type="application/json" id="audit-data">)(.*?)(</script>)', re.S)
PLACEHOLDER = "/*__AUDIT_DATA__*/"

def load_page(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def existing_data(page):
    m = MARK_RE.search(page)
    if not m or m.group(2).strip() in ("", PLACEHOLDER):
        return {"params": None, "runs": []}
    return json.loads(m.group(2).replace("<\\/", "</"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--html")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    page = load_page(a.html) if a.html and os.path.exists(a.html) else load_page(os.path.join(here, "template.html"))
    data = existing_data(page)

    with open(a.data, encoding="utf-8") as f:
        new = json.load(f)
    new_runs = new["runs"] if "runs" in new else [new]
    if new.get("params"):
        data["params"] = new["params"]
    if not data.get("params"):
        sys.exit("No parameter list: pass {'params': [...], 'runs': [...]} the first time.")

    by_id = {r["id"]: r for r in data["runs"]}
    for r in new_runs:
        for key in ("id", "generated_at", "label", "calls"):
            if key not in r:
                sys.exit(f"Run is missing '{key}'")
        by_id[r["id"]] = r                      # same id -> replace
    data["runs"] = sorted(by_id.values(), key=lambda r: r["generated_at"], reverse=True)

    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    if MARK_RE.search(page):
        page = MARK_RE.sub(lambda m: m.group(1) + blob + m.group(3), page, count=1)
    else:
        sys.exit("Template has no audit-data block.")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Wrote {a.out}: {len(data['runs'])} runs, newest {data['runs'][0]['generated_at']}")

if __name__ == "__main__":
    main()
