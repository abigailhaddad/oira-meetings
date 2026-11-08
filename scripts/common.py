import time, json, os, sys, requests
UA = "abigailhaddad-research (github.com/abigailhaddad)"
BASE = "https://www.reginfo.gov"
MIN_GAP = 1.6
_last = [0.0]
LOG = os.path.join(os.path.dirname(__file__), "..", "data", "request_log.jsonl")
S = requests.Session(); S.headers["User-Agent"] = UA

class Blocked(Exception): pass

def get(url, params=None, **kw):
    wait = MIN_GAP - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    try:
        r = S.get(url, params=params, timeout=60, **kw)
    finally:
        _last[0] = time.time()
    with open(LOG, "a") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "url": r.url, "status": r.status_code, "bytes": len(r.content)}) + "\n")
    if r.status_code in (403, 429):
        raise Blocked(f"{r.status_code} for {r.url}")
    return r
