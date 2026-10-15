#!/usr/bin/env python3
"""nhbot — nhentai mirror scraper (nhentai.to / nhentai.wtf)
usage:
  nh.py search "yuri" [--sort popular|recent] [--pages 2] [--limit 10]
  nh.py tag yuri [--sort popular] [--limit 5] [--download]
  nh.py info 2896933
  nh.py download 2896933 [--max-pages 10] [--workers 4] [--cbz] [--out DIR]
  nh.py batch "yuri school" --limit 3 [--cbz]
"""
import argparse, json, os, re, sys, time, zipfile
from urllib.parse import quote
import requests

MIRRORS = ["https://nhentai.to", "https://nhentai.wtf"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
DL = os.path.expanduser("~/storage/downloads/nhentai")
S = requests.Session()
S.headers.update({"User-Agent": UA, "Referer": "https://nhentai.to/"})

def get(url, tries=3):
    for i in range(tries):
        try:
            r = S.get(url, timeout=25)
            if r.status_code == 200:
                return r
            if r.status_code in (404,):
                return r
        except requests.RequestException:
            pass
        time.sleep(1.5 * (i + 1))
    return None

def base_for(path):
    for m in MIRRORS:
        r = get(m + path)
        if r and r.status_code == 200 and "<html" in r.text[:200].lower():
            return m, r
    sys.exit("mirror mati semua / network block")

def parse_gal(html):
    title = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else "?"
    srcs = re.findall(r'data-src="https://supercdn\.site/galleries/(\d+)/(\d+)t\.jpg"', html)
    if not srcs:
        srcs = re.findall(r'"https://supercdn\.site/galleries/(\d+)/(\d+)t\.jpg"', html.replace("\\/", "/"))
    from collections import Counter
    media = Counter(m for m, _ in srcs).most_common(1)[0][0] if srcs else None
    pages = sorted({int(p) for m, p in srcs if m == media}) if media else []
    tags = {}
    for kind in ("tag", "artist", "parody", "character", "group", "language", "category"):
        found = sorted(set(re.findall(rf'href="/{kind}/([^"/]+)/"', html)))
        if found:
            tags[kind] = found
    fav = re.search(r'(\d[\d,]*)\s*</span>\s*favorites|favorites?[^0-9]{0,40}(\d[\d,]*)', html, re.I)
    return {"title": title, "media_id": media, "pages": pages, "tags": tags,
            "favorites": (fav.group(1) or fav.group(2)).replace(",", "") if fav else None}

def cmd_info(gid):
    m, r = base_for(f"/g/{gid}/")
    g = parse_gal(r.text)
    g.update({"id": gid, "url": f"{m}/g/{gid}/"})
    print(json.dumps(g, indent=2, ensure_ascii=False))
    return g

def cmd_search(q, sort, pages_n, limit):
    out = []
    for p in range(1, pages_n + 1):
        path = f"/search?q={quote(q)}" + (f"&sort={sort}" if sort else "") + (f"&page={p}" if p > 1 else "")
        m, r = base_for(path)
        ids = re.findall(r'href="/g/(\d+)/"', r.text)
        seen = set()
        for gid in ids:
            if gid in seen:
                continue
            seen.add(gid)
            out.append({"id": gid, "site": m})
        if len(seen) == 0:
            break
        time.sleep(0.5)
    out = out[:limit]
    for o in out:
        print(o["id"], o["site"] + "/g/" + o["id"] + "/")
    return out

def download(gid, out_root, max_pages, workers, cbz):
    m, r = base_for(f"/g/{gid}/")
    g = parse_gal(r.text)
    if not g["media_id"]:
        sys.exit(f"gallery {gid}: media_id ga ketemu")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", g["title"])[:60].strip("_")
    folder = os.path.join(out_root, f"{gid}_{slug}")
    os.makedirs(folder, exist_ok=True)
    pages = g["pages"][:max_pages] if max_pages else g["pages"]
    print(f"[dl] {g['title']}\n     media={g['media_id']} pages={len(pages)} → {folder}")
    ok, fail = 0, 0
    from concurrent.futures import ThreadPoolExecutor
    def fetch(n):
        ext = "jpg"
        url = f"https://supercdn.site/galleries/{g['media_id']}/{n}.{ext}"
        dst = os.path.join(folder, f"{n:04d}.{ext}")
        if os.path.exists(dst) and os.path.getsize(dst) > 1000:
            return True
        try:
            rr = S.get(url, timeout=30)
            if rr.status_code == 200 and rr.content[:2] == b"\xff\xd8":
                open(dst, "wb").write(rr.content)
                time.sleep(0.15)
                return True
            if rr.status_code == 200 and rr.content[:4] == b"RIFF":
                dst = dst[:-3] + "webp"; open(dst, "wb").write(rr.content); time.sleep(0.15); return True
        except requests.RequestException:
            pass
        return False
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, res in enumerate(ex.map(fetch, pages), 1):
            if res:
                ok += 1
            else:
                fail += 1
            if i % 20 == 0:
                print(f"  {i}/{len(pages)}")
    info = {k: g[k] for k in g}; info.update({"id": gid, "url": f"{m}/g/{gid}/", "downloaded": ok, "failed": fail})
    json.dump(info, open(os.path.join(folder, "info.json"), "w"), indent=2, ensure_ascii=False)
    if cbz and ok:
        cz = folder + ".cbz"
        with zipfile.ZipFile(cz, "w", zipfile.ZIP_STORED) as z:
            for f in sorted(os.listdir(folder)):
                if f.endswith((".jpg", ".webp")):
                    z.write(os.path.join(folder, f), f)
        print(f"[cbz] {cz}")
    print(f"[done] ok={ok} fail={fail}")
    return ok

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--sort", default="", choices=["", "popular", "recent"]); s.add_argument("--pages", type=int, default=1); s.add_argument("--limit", type=int, default=20)
    t = sub.add_parser("tag"); t.add_argument("name"); t.add_argument("--sort", default="popular", choices=["", "popular", "recent"]); t.add_argument("--pages", type=int, default=1); t.add_argument("--limit", type=int, default=20); t.add_argument("--download", action="store_true")
    i = sub.add_parser("info"); i.add_argument("id")
    d = sub.add_parser("download"); d.add_argument("id"); d.add_argument("--out", default=DL); d.add_argument("--max-pages", type=int, default=0); d.add_argument("--workers", type=int, default=4); d.add_argument("--cbz", action="store_true")
    b = sub.add_parser("batch"); b.add_argument("query"); b.add_argument("--limit", type=int, default=3); b.add_argument("--sort", default="popular", choices=["", "popular", "recent"]); b.add_argument("--out", default=DL); b.add_argument("--max-pages", type=int, default=0); b.add_argument("--cbz", action="store_true")
    a = ap.parse_args()
    if a.cmd == "search":
        cmd_search(a.query, a.sort, a.pages, a.limit)
    elif a.cmd == "tag":
        res = cmd_search(f'tag:"{a.name}"', a.sort, a.pages, a.limit)
        if a.download:
            for o in res:
                download(o["id"], DL, 0, 4, False); time.sleep(1)
    elif a.cmd == "info":
        cmd_info(a.id)
    elif a.cmd == "download":
        download(a.id, a.out, a.max_pages, a.workers, a.cbz)
    elif a.cmd == "batch":
        res = cmd_search(a.query, a.sort, 1, a.limit)
        for o in res:
            try:
                download(o["id"], a.out, a.max_pages, 4, a.cbz)
            except SystemExit as e:
                print(f"skip {o['id']}: {e}")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
