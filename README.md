# akal-vps — VPS gratis tanpa CC (GitHub Actions + tmate)

Runner GitHub = mesin beneran: **4 vCPU / 16 GB RAM (public repo)**, Ubuntu 24.04,
git + python3 + node20 preinstalled, **no credit card**, public repo = menit unlimited.

Sesi hidup maksimal **6 jam** per run (job timeout). Habis? klik Run workflow lagi —
selama gak dihapus, repo ini = VPS lo on-demand 24/7 (cron juga bisa, lihat bawah).

## setup (5 menit, sekali seumur hidup)

1. bikin akun github.com (email doang, no CC)
2. bikin repo baru **Public** → nama bebas (`vps`)
3. upload isi folder ini ke repo (Add file → Upload files → drag seluruh isi `akal-vps/`,
   termasuk folder `.github/`)
4. tab **Actions** → pilih workflow **vps** → **Run workflow**
5. tunggu ~30 detik → buka log job → muncul baris:
   ```
   SSH COMMAND (copy-paste di Termux):
   ssh session=...,fingerprint=... @fr1.tmate.io ...
   ```
6. paste di Termux → lo udah masuk shell Ubuntu 16GB, root-nya `runner`, sudo available

## bawa tools lo masuk

Folder repo ke-load otomatis pas checkout. Supaya `cuan/` + `nhbot/` ikut:

```bash
# di repo lo, drag-upload juga folder cuan/ dan nhbot/ (atau push via git)
# habis SSH masuk:
python3 nhbot/nh.py search "yuri" --limit 5     # jalan langsung
node cuan/spread.mjs --test
./cuan/short.sh https://tujuan.com
```

atau clone repo lain: `git clone https://github.com/LO/REPO.git`

## mode cron (gak perlu SSH)

Actions jalan tanpa login — tambah workflow sendiri, contoh spread harian:

```yaml
# .github/workflows/daily-spread.yml
name: daily-spread
on:
  schedule: [{cron: "0 9,15,21 * * *"}]   # UTC = WIB-7 → 16:00,22:00,04:00
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: {node-version: 20}
      - run: node cuan/spread.mjs "pesan di sini {link}" "$SHORTLINK"
        env:
          TG_TOKEN: ${{ secrets.TG_TOKEN }}
```

## alternatif persistent (no CC)

- **vpswala.org** — 2GB ARM selamanya, verifikasi pakai akun GitHub (no card),
  SSH root masuk email. Kecil tapi 24/7 beneran.
- **glitch.com** — 512MB, web terminal, no CC.
- **serv00.com** — shell FreeBSD always-on, tapi butuh invite code.

## catatan

- jangan dipake mining / abuse → repo kena ban.
- public repo = menit unlimited; private = 2000 menit/bulan (cukup ~5 sesi/bulan).
- file yang lo taruh di repo (`cuan/`, `nhbot/`) kelihatan publik — API key jangan
  commit, taruh di GitHub **Settings → Secrets** (`${{ secrets.KEY }}`).
