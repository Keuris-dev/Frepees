# cuan — shortlink operation

## akun (shrink.pe)

- login: https://shrink.pe/auth/signin
- akun + api key: lihat `.cuan/` lokal (jangan commit)
- min payout: **$5** · daily · PayPal / USDT / Payoneer · rate ID ≈ $4/1000, tier-1 s/d $20-30/1000

## tools

```bash
./short.sh https://tujuan.com            # buat link
./short.sh https://tujuan.com custom-alias
node spread.mjs "<pesan {link}>" <link>  # sebar ke semua target
node spread.mjs --test                   # tes koneksi target
node spread.mjs "<msg>" <link> --dry     # preview
```

## targets.json (`~/.cuan/targets.json`)

```json
[
  {"type":"telegram","token":"BOT_TOKEN","chat":"@channelku","name":"tg-channel"},
  {"type":"discord","webhook":"https://discord.com/api/webhooks/xx/yy","name":"dc-grup"},
  {"type":"webhook","url":"https://...","body":{"content":"{link}"},"name":"lain"}
]
```

- telegram bot: @BotFather → /newbot → token; channel: add bot as admin
- discord: channel settings → Integrations → Webhooks → New → copy URL

## strategi (yang bikin klik = MANUSIA)

1. **Telegram channel** — niche jelas (tool gratis, download, tutorial, gallery).
   Post 2-5x sehari, jangan cuma link — kasih konten + link "lanjut/disini".
2. **Discord** — server besar niche lo, share di thread yang relevan.
3. **Konten drip** — `~/nsfw.sh "prompt"` → 3 gambar/hari → upload preview →
   link "full gallery" = shortlink. Fresh content = klik berulang.
4. **Reddit/Forum** — subreddit + kaskus/vgx yang relevant; 1 post natural per hari
   per akun. Spam = ban permanen, akun mati.
5. **YouTube description / SEO blog** — link tahan lama, klik jangka panjang.

## aturan main (biar gak di-ban + dibayar)

- klik bot / exchange / forced = $0 + blacklist. Traffic harus orang beneran.
- 1000 klik ID ≈ $4 · 1000 klik US ≈ $10 → fokus niche yang pembacanya tier-1/ID.
- jangan spam 1 tempat — sebar wajar, 1 link beberapa tujuan.
- cek balance harian: `/member/dashboard` atau cookie session `.cdp/ck.txt`.
- ganti password + email akun ke punya lo setelah pertama login.

## earnings math

| klik/hari | RPM ID ($4) | RPM US ($10) | per bulan |
|---|---|---|---|
| 100 | $0.40 | $1.00 | $12–30 |
| 500 | $2.00 | $5.00 | $60–150 |
| 1000 | $4.00 | $10.00 | $120–300 |

payout pertama $5 ≈ 1250 klik ID — target realistis minggu 1-2 dengan konsisten.
