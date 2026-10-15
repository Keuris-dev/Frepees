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
- Klik tombol **Run workflow** (warna hijau) → pilih branch `main` → klik **Run workflow**

### 3. Ambil kredensial

Tunggu ~40 detik. Buka halaman **Summary** run yang baru selesai. Muncul tabel:

```
## VPS Siap!

### Terminus (HP):
| Kolom | Isi |
|---|---|
| Host | bore.pub |
| Port | 12345 |
| User | runzz01 |
| Pass | Az9.xxxxxxxx |
```

**Copy 4 kolom itu.**

### 4. Masuk via Terminus

Buka app **Terminus** di HP → buka session baru → isi:

| Kolom | Isi |
|---|---|
| Host | `bore.pub` |
| Port | (angka dari Summary) |
| User | `runzz01` |
| Password | (dari Summary) |

Klik connect. **Lo udah masuk VPS Ubuntu 16GB.** sudo tersedia.

---

## Alternatif: Browser (gak perlu Terminus)

Dari Summary, ada juga link browser:
```
https://xxxx.trycloudflare.com  (user runzz01 / pass Az9.xxxx)
```
Buka di browser → langsung masuk terminal di HP/laptop.

---

## Tools yang udah terpasang

- git, python3, node20, pip
- sudo (passwordless)

Clone repo lo sendiri atau install tools:
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
- Password **random tiap run** — kalau lupa, lihat lagi di Summary.
- Sesi max **6 jam**. Kalau butuh lebih lama, run lagi.
- File di repo ini **publik** — API key jangan commit, pakai **Settings → Secrets**.

---

## FAQ

**Q: Kok gak bisa connect?**
A: Tunggu sampe Summary muncul (bore butuh ~30-40 detik). Kalau udah lewat 1 menit dan gak muncul, cancel run → run lagi.

**Q: Password-nya mana?**
A: Di **Summary** run (bukan di log). Random tiap run.

**Q: Bisa akses dari laptop?**
A: Boleh. Host `bore.pub`, port sama, user & password sama.

**Q: Kok run-nya aneh / error?**
A: Cek tab **Summary** — biasanya ada info error di situ. Kalau kosong, run lagi.

**Q: Gua mau setup sendiri di repo gua?**
A: Fork → Settings → Secrets and variables → Actions → **New repository secret** → Name: `TS_AUTHKEY`, Value: authkey dari tailscale.com. Abis itu run → tailscale IP muncul di Summary.
