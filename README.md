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

Tunggu **±1 menit** (job `display` harus selesai dulu). Buka halaman **Summary** run-nya → muncul:

```
| Kolom | Isi |
|---|---|
| Host | qoako-132-196-20-107.run.pinggy-free.link |
| Port | 38255 |
| User | runzz01 |
| Pass | vpsXXXX-XXXX |
```

**Copy 4 kolom itu.** (Kosong? tunggu sebentar → refresh.)

### 4. Masuk via Terminus

Buka **Terminus** → session baru → isi Host/Port/User/Pass dari Summary → Connect.

⚠️ **URL Terminus berganti tiap ±60 menit** (layanan gratis). Kalau putus:
buka **log job `ssh`** (klik job `ssh` di run) → tarik ke paling bawah →
copy `TERMINUS=` / baris `🔁` **terbaru**.

…atau **skip masalah ini selamanya** → setup **Tailscale** sekali (bagian bawah) →
IP `100.x` stabil — atau **Portwarp** → host `xxx.free.pwrp.cc` tetap, HP gak
perlu install apa-apa.

---

## Alternatif: Browser (gak pernah putus)

Di Summary yang sama ada juga link browser:
```
Terminal web: https://xxxx.trycloudflare.com
User: runzz01
Pass: vpsXXXX-XXXX
```
Buka di browser → terminal langsung muncul. **Tahan full 6 jam**, gak ganti-ganti.

---

## Koneksi stabil tanpa putus (Tailscale) — setup sekali

Host pinggy (`xxx.run.pinggy-free.link`) **berganti tiap ±60 menit** (limit gratis).
Biar gak pernah putus lagi: pakai **Tailscale** — VPN pribadi gratis, tanpa kartu
kredit, IP `100.x` tetap selama sesi. **Setup sekali, 5 menit:**

1. Daftar **https://tailscale.com** (bisa login Google) → buka **Admin Console**
2. **Settings → Keys → Generate auth key** → centang **Reusable** ✅ dan
   **Pre-approved** ✅ → TTL `90 hari` → **Generate** → copy `tskey-auth-...`
3. Di fork lo: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `TS_AUTHKEY`
   - Value: key tadi
4. HP: install app **Tailscale** (Play Store) → **login akun yang sama**
5. **Run workflow** lagi → Summary muncul baris **Tailscale IP** → di Terminus isi:
   Host = `100.x.x.x`, Port `22`, User/Pass tetap.

Catatan:

- Fork **gak bawa secret** → tiap orang isi `TS_AUTHKEY` sendiri (akun masing-masing,
  gak nyambung ke akun siapa pun). Tanpa secret juga tetap jalan (pinggy + browser).
- Key berlaku **90 hari** → generate lagi setelah itu.
- Tiap run bikin node baru (`runzz...`) di console lo → sesekali hapus yang
  disconnected biar rapi.

---

## SSH alamat tetap tanpa install apa-apa di HP (Portwarp) — setup sekali

Alternatif Tailscale: **HP lo gak perlu install app apa pun.** Terminus langsung
SSH ke host `xxxx.free.pwrp.cc:PORT` yang **gak pernah ganti** antar run (beda sama
pinggy). Akun gratis, tanpa kartu kredit — limit: 1 tunnel, TCP beneran. Setup sekali:

1. Daftar **https://portwarp.com/register** → login
2. Tab **Tunnels → Create Tunnel** → Protocol **TCP** → Local port **22** → Create
   → tunggu **±90 detik** (antrian akun gratis) → copy endpoint `xxxx.free.pwrp.cc:PORT`
3. Install CLI di PC: `curl -fsSL https://portwarp.com/install | bash` (Linux/macOS;
   Windows: [download ZIP](https://portwarp.com/downloads)) → jalankan `pwrp login`
   → approve di browser
4. Copy isi file `~/.portwarp/credentials.json`
   (Windows: `C:\Users\NAMA\.portwarp\credentials.json`)
5. Di fork lo: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `PWRP_CRED`
   - Value: isi file tadi (JSON utuh)
6. **Run workflow** → Summary muncul baris **🌐 Portwarp SSH** → di Terminus isi
   Host = `xxxx.free.pwrp.cc`, Port = `PORT`, User/Pass tetap

Catatan:

- Host+port **tetap sama di tiap run** — masuk sekali di Terminus, besok tinggal
  klik Run workflow lagi (kredensial user/pass tetap, host juga tetap).
- Fork gak bawa secret → tiap orang isi `PWRP_CRED` sendiri (akun masing-masing).
- Endpoint baru muncul ±1-2 menit setelah run mulai.
- **Tailscale** tetap lebih kuat buat uptime permanen (bisa diakses walau gak di-run);
  Portwarp unggul di kemudahan — gak ada install apa-apa di HP. Mau dua-duanya juga boleh.

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

**Q: Kenapa koneksi putus tiap ±1 jam?**
A: Host pinggy berganti tiap ±60 menit (limit plan gratis). Solusi permanen: setup **Tailscale** sekali → bagian **"Koneksi stabil tanpa putus"** di atas → IP `100.x` gak pernah ganti. Alternatif tanpa install app di HP: **Portwarp** → bagian **"SSH alamat tetap"** → host `xxxx.free.pwrp.cc` tetap tiap run. Males semua? pakai link Browser (juga gak pernah putus).

**Q: Terminus connection failed?**
A: Tunggu Summary muncul (~1 menit) dulu sebelum connect. Kalau tetep gagal: URL mungkin udah lewat 60 menit → buka **log job `ssh`**, pakai `TERMINUS=` terbaru. Alternatif: link Browser (gak pernah putus).

**Q: Summary kosong / belum muncul?**
A: Job `display` masih jalan (±1 menit). Refresh. Kalau 5 menit tetep kosong: cancel → run lagi.

**Q: Password-nya mana?**
A: Di **Summary** run. Random tiap run.

**Q: Bisa akses dari laptop?**
A: Boleh. Host/port/user/password sama, masuk via SSH client biasa.

**Q: Run-nya error?**
A: Cek job `ssh` di run itu — log-nya nunjukin step mana yang gagal.

**Q: Gua mau setup sendiri di repo gua?**
A: Ikutin langkah 1–5 di bagian **"Koneksi stabil tanpa putus (Tailscale)"** di atas — intinya: authkey sendiri → secret `TS_AUTHKEY` di fork lo → login Tailscale di HP → run.
