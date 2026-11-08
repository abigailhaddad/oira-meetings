"""Step 3: download every document listed on the meeting pages (one GET per distinct documentID), hash, save untrusted files under downloads/."""
import sys, csv, json, os, hashlib, re, urllib.parse
from common import *
TAG = sys.argv[1]
DL = f"../downloads/{TAG}"; os.makedirs(DL, exist_ok=True)
docs = list(csv.DictReader(open(f"../data/{TAG}_documents_listed.csv")))
meta_path = f"../data/{TAG}_downloads.json"
done = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
ids = sorted({d["document_id"] for d in docs}, key=int)
print("distinct documentIDs", len(ids), "listing rows", len(docs))
for n, did in enumerate(ids):
    if did in done and done[did].get("status") == 200: continue
    try:
        r = get(BASE + "/public/do/eoDownloadDocument", params={"pubId": "", "eodoc": "true", "documentID": did})
    except Blocked as e:
        print("BLOCKED", e); json.dump(done, open(meta_path, "w"), indent=1); sys.exit(2)
    cd = r.headers.get("Content-Disposition", "")
    m = re.search(r'filename="(.*)"\s*$', cd) or re.search(r"filename\*?=(?:UTF-8'')?([^;]+)", cd)   # quoted names may contain ';'
    
    fname = urllib.parse.unquote(m.group(1)) if m else None
    rec = dict(status=r.status_code, content_type=r.headers.get("Content-Type"), content_disposition=cd, filename=fname, size=len(r.content))
    if r.status_code == 200:
        rec["sha256"] = hashlib.sha256(r.content).hexdigest()
        open(f"{DL}/{did}.bin", "wb").write(r.content)
    done[did] = rec
    if n % 25 == 0: print(n, flush=True); json.dump(done, open(meta_path, "w"), indent=1)
json.dump(done, open(meta_path, "w"), indent=1)
print("done", len(done), "non-200:", [k for k, v in done.items() if v["status"] != 200])
