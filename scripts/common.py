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
    r = None
    for attempt in range(3):   # transient connection drops: retry up to 2 more times with a pause (never retries a 403/429)
        try:
            r = S.get(url, params=params, timeout=60, **kw)
            break
        except requests.RequestException as e:
            with open(LOG, "a") as f:
                f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "url": url, "status": f"exception {type(e).__name__}", "bytes": 0}) + "\n")
            if attempt == 2: raise
            time.sleep(15)
        finally:
            _last[0] = time.time()
    with open(LOG, "a") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "url": r.url, "status": r.status_code, "bytes": len(r.content)}) + "\n")
    if r.status_code in (403, 429):
        raise Blocked(f"{r.status_code} for {r.url}")
    return r
