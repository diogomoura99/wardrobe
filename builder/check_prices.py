"""Sale watch: price checks for the pieces in watchlist.json.

  python3 check_prices.py auto      check the stores with open product data (Shopify),
                                    then list the pages that need a browser check
  python3 check_prices.py record ID --price 337 [--member 300] [--stock in|low|out] [--note "..."]
                                    save what the browser check found
  python3 check_prices.py summary   what changed, and what hit its target price
"""
import argparse, datetime, json, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WL = os.path.join(HERE, "watchlist.json")
STATE = os.path.join(HERE, ".watch_state.json")   # git-ignored: last run time, changes in this run
TODAY = datetime.date.today().isoformat()
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def load():
    return json.load(open(WL))


def save(wl):
    json.dump(wl, open(WL, "w"), indent=1, ensure_ascii=False)


def state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}


def best(last):
    ps = [p for p in (last.get("price"), last.get("member")) if p]
    return min(ps) if ps else None


def record(wl, iid, price, member=None, stock="in", note=None):
    it = next(i for i in wl["items"] if i["id"] == iid)
    old = dict(it.get("last") or {})
    it["last"] = {"date": TODAY, "price": price, "member": member, "stock": stock}
    if note:
        it["last"]["note"] = note
    changed = (old.get("price"), old.get("member"), old.get("stock")) != (price, member, stock)
    if changed and (not it["history"] or it["history"][-1].get("price") != price or it["history"][-1].get("member") != member):
        it["history"].append({"date": TODAY, "price": price, **({"member": member} if member else {})})
    st = state()
    st.setdefault("changes", {})
    if changed:
        st["changes"][iid] = {"was": old, "now": it["last"]}
    json.dump(st, open(STATE, "w"), indent=1)
    return changed


def fetch(url, cookie=None):
    h = {"User-Agent": UA, "Accept-Language": "en"}
    if cookie:
        h["Cookie"] = cookie
    return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20).read().decode("utf-8", "replace")


def shopify(it):
    c = it["check"]
    d = json.loads(fetch(c.get("js_url") or it["url"].split("?")[0] + ".js", c.get("cookie")))
    v = next(v for v in d["variants"] if v["title"].strip() == c["variant"])
    return v["price"] / 100, v["available"]


def jsonld(it):
    """Product pages that serve schema.org JSON-LD without a browser (e.g. Les Deux): find the offer for one SKU."""
    import re
    html = fetch(it["url"])
    for m in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        try:
            j = json.loads(m)
        except Exception:
            continue
        for n in (j if isinstance(j, list) else [j]):
            for v in [n] + (n.get("hasVariant") or []) if isinstance(n, dict) else []:
                if v.get("sku") == it["check"]["sku"]:
                    o = v["offers"][0] if isinstance(v["offers"], list) else v["offers"]
                    return float(o["price"]), o.get("availability", "").endswith("InStock")
    raise ValueError("SKU not found on the page")


def cmd_auto(_):
    wl = load()
    st = state()
    st["changes"] = {}
    st["started"] = datetime.datetime.now().isoformat(timespec="minutes")
    json.dump(st, open(STATE, "w"), indent=1)
    browser = []
    for it in wl["items"]:
        c = it["check"]
        if c["type"] in ("shopify", "jsonld"):
            try:
                price, avail = (shopify if c["type"] == "shopify" else jsonld)(it)
                ch = record(wl, it["id"], price, None, "in" if avail else "out")
                print(f"checked {it['id']}: €{price:g}, {'in stock' if avail else 'SOLD OUT'} in {it['size']}{' (changed)' if ch else ''}")
            except Exception as ex:
                print(f"FAILED {it['id']}: {ex}; check it in the browser instead")
                browser.append(it)
        else:
            browser.append(it)
    save(wl)
    if browser:
        print("\nCheck these in the browser, then run `record`:")
        for it in browser:
            c = it["check"]
            how = f"read JSON-LD offers, SKU {c['sku']}" if c.get("how") == "jsonld" else "read the price on the page"
            print(f"- {it['id']}: {it['url']}  size {it['size']}; {how}. {c.get('note', '')}".rstrip())


def cmd_record(a):
    wl = load()
    ch = record(wl, a.id, a.price, a.member, a.stock, a.note)
    save(wl)
    print("recorded" + (" (changed)" if ch else " (no change)"))


def cmd_summary(_):
    wl = load()
    st = state()
    st["last_full_run"] = datetime.datetime.now().isoformat(timespec="minutes")
    json.dump(st, open(STATE, "w"), indent=1)
    news = []
    for it in wl["items"]:
        b = best(it["last"])
        tag = None
        if b is not None and b <= it["great"]:
            tag = "GREAT PRICE"
        elif b is not None and b <= it["target"]:
            tag = "AT TARGET"
        elif b is not None and b < it["full"] and it["last"].get("price", it["full"]) < it["full"]:
            tag = "ON SALE"
        if it["last"].get("stock") in ("low", "out"):
            tag = (tag + ", " if tag else "") + ("LOW STOCK" if it["last"]["stock"] == "low" else "SOLD OUT") + f" in {it['size']}"
        ch = st.get("changes", {}).get(it["id"])
        if tag or ch:
            was = ch["was"].get("price") if ch else None
            news.append(f"{it['brand']} {it['name']} ({it['size']}): €{b:g} now (full €{it['full']:g}, target €{it['target']:g})"
                        + (f" [{tag}]" if tag else "") + (f" changed from €{was:g}" if ch and was and was != it['last'].get('price') else ""))
    print("\n".join(news) if news else "No news: nothing changed and nothing is at its target.")
    print("CHANGED" if st.get("changes") else "UNCHANGED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("auto").set_defaults(f=cmd_auto)
    r = sp.add_parser("record")
    r.add_argument("id")
    r.add_argument("--price", type=float, required=True)
    r.add_argument("--member", type=float)
    r.add_argument("--stock", choices=["in", "low", "out"], default="in")
    r.add_argument("--note")
    r.set_defaults(f=cmd_record)
    sp.add_parser("summary").set_defaults(f=cmd_summary)
    a = ap.parse_args()
    a.f(a)
