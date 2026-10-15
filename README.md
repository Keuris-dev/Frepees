# Frepees — VPS Gratis Tanpa CC (GitHub Actions)

Runner GitHub = mesin beneran: **4 vCPU / 16 GB RAM**, Ubuntu 24.04,
git + python3 + node20 preinstalled. **No credit card.** Public repo = menit unlimited.

Sesi hidup maksimal **6 jam** per run. Habis? Klik Run workflow lagi —
selama gak dihapus, repo ini = VPS lo on-demand 24/7.

## Cara Pakai (3 langkah)

### 1. Fork repo ini

Klik tombol **Fork** di pojok kanan atas halaman ini.

### 2. Run workflow

- Buka tab **Actions** di repo fork lo
- Klik workflow **vps** di menu kiri
- Klik tombol **Run workflow** (hijau) → pilih branch `main` → klik **Run workflow**

### 3. Ambil kredensial

Tunggu ~40 detik. Buka halaman **Summary** run-nya. Muncul:

```
### Terminus (HP):
| Kolom | Isi |
|---|---|
| Host | qoako-132-196-20-107.run.pinggy-free.link |
| Port | 38255 |
| User | runzz01 |
| Pass | vpsXXXX-XXXX |
```

**Copy 4 kolom itu.**

### 4. Masuk via Terminus

Buka **Terminus** → session baru → isi Host/Port/User/Pass dari Summary → Connect.

⚠️ **URL Terminus berganti tiap 60 menit** (layanan gratis). Kalau putus:
refresh halaman Summary → copy **URL TERBARU** di bagian paling bawah (`🔁 URL Terminus BARU`).

---

## Alternatif: Browser (gak pernah putus)

Di Summary yang sama ada juga link browser:
```
Link: https://xxxx.trycloudflare.com
User: runzz01
Pass: vpsXXXX-XXXX
```
Buka di browser → terminal langsung muncul. **Tahan full 6 jam**, gak ganti-ganti.

---

## Tools yang udah terpasang

- git, python3, node20, pip
- sudo (passwordless)

```bash
git clone https://github.com/LO/REPO.git
pip install requests beautifulsoup4
npm install -g ts-node typescript
```

---

## Yang ada di repo ini

- `.github/workflows/vps.yml` — workflow utama
- `cuan/` — toolkit shortlink + auto-poster
- `nhbot/` — scraper nhentai (Python)

---

## Catatan Penting

- **Jangan mining / abuse** → repo kena ban.
- Public repo = menit unlimited. Private = 2000 menit/bulan.
- Password **random tiap run** — lupa? lihat lagi di Summary.
- Sesi max **6 jam**. Butuh lebih? run lagi.
- File di repo ini **publik** — API key jangan commit, pakai **Settings → Secrets**.

---

## FAQ

**Q: Terminus connection failed?**
A: Tunggu Summary muncul (~40 detik) dulu sebelum connect. Kalau tetep gagal: URL mungkin udah lewat 60 menit → refresh Summary, pakai URL terbaru. Alternatif: pakai link Browser.

**Q: Password-nya mana?**
A: Di **Summary** run (bukan di log). Random tiap run.

**Q: Bisa akses dari laptop?**
A: Boleh. Host/port/user/password sama, masuk via SSH client biasa.

**Q: Run-nya error?**
A: Cek tab **Summary** — kalau kosong, cancel → run lagi.

**Q: Gua mau setup sendiri di repo gua?**
A: Fork → Settings → Secrets and variables → Actions → **New repository secret** → Name: `TS_AUTHKEY`, Value: authkey dari tailscale.com. Abis itu run → tailscale IP muncul di Summary (direct IP, tanpa tunnel).
