# KitaLabel × SapaGo demo

[Buka demo Vercel](https://demo-sapago-kitalabel.vercel.app/).

![Preview landing page dan widget demo](preview.jpg)

Landing page duplikat https://marketz.kitalabel.com/ dengan aset, warna, konten dan video dari referensi publik. Runtime WordPress dan tracking dilepas. Interaksi material, galeri dan FAQ berjalan dengan JavaScript lokal.

Preview: `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`

Chat menggunakan embed resmi SapaGo dengan public widget key khusus Kitalabel. UI, bootstrap, dan percakapan ditangani oleh SapaGo. Tombol konsultasi mengarahkan fokus dan sorotan ke widget; klik ikon widget untuk membuka percakapan.

Embed berada di `dist/index.html` dan `widget.html`. `data-api-key` merupakan identifier publik untuk browser, bukan private API token.

`mirror.py` adalah helper rekonstruksi dari HTML referensi lokal di `/tmp/kitalabel-reference.html`. File hasil yang siap hosting ada di `dist/`; pengubahan desain dilakukan di situ.
