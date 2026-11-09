"""Re-fetch documents whose first download looks damaged (poppler error in manifest, or size exactly a multiple of 1 MiB), compare bytes/Content-Length/SHA with the first fetch.
Writes data/bad_doc_recheck.json. Does not overwrite the originals."""
import csv, glob, json, os, hashlib
from common import *
bad = []
for f in sorted(glob.glob("../data/*_document_manifest.csv")):
    t = os.path.basename(f)[:7]
    for r in csv.DictReader(open(f)):
        if r["note"].startswith("DOWNLOAD FAILED") or "error" in r["note"] or (r["size_bytes"] and int(r["size_bytes"]) % 1048576 == 0):
            bad.append((t, r))
out = []
for t, r in bad:
    did = r["document_id"]
    resp = get(BASE + "/public/do/eoDownloadDocument", params={"pubId": "", "eodoc": "true", "documentID": did})
    sha = hashlib.sha256(resp.content).hexdigest()
    out.append(dict(month=t, document_id=did, meeting_id=r["meeting_id"], file_name=r["file_name"], first_size=r["size_bytes"], first_sha=r["sha256"], second_status=resp.status_code, second_size=len(resp.content),
                    second_content_length_header=resp.headers.get("Content-Length"), second_sha=sha, identical=sha == r["sha256"], first_note=r["note"][:150]))
    print(out[-1], flush=True)
json.dump(out, open("../data/bad_doc_recheck.json", "w"), indent=1)
