Backlink Index Checker

Halo teman-teman SEO!  

Ini adalah tools sederhana tapi powerful buat ngecek apakah backlink atau URL yang kamu pasang sudah terindex Google atau belum. Karena kita tahu, backlink tanpa index itu kayak beli tiket konser tapi gak jadi nonton — sia-sia kan?

---

Kenapa tools ini dibuat?

Sebagai SEO specialist, saya sering butuh cek ribuan backlink sekaligus. Manual? Bisa pingsan. Pakai tools mahal? Belum tentu sesuai kebutuhan. Jadi saya buat tools ini, simple, gratis, dan bisa kamu pakai sendiri kapan saja.

---

Apa yang bisa tools ini?

- Cek index backlink di Google secara real-time  
- Pakai multi-threading supaya lebih cepat, tapi tetep aman dengan maksimal 5 thread  
- Random User-Agent dari daftar lengkap supaya request kita gak gampang ketahuan bot  
- Ada delay random antara 3-7 detik, supaya Google gak curiga  
- Hasilnya langsung terpisah jadi dua file: yang sudah terindex, dan yang belum  

---

Cara pakai gampang banget:

1. Siapkan file `url.txt` (atau nama lain)  
   Isikan URL backlink yang mau dicek, satu URL per baris. Contoh:

   https://situscontoh.com/backlink1  
   https://situscontoh.com/backlink2

2. Pastikan Python sudah terinstall, dan module `requests` + `beautifulsoup4` sudah siap:

   pip install requests beautifulsoup4

3. Jalankan script dengan perintah:

   python cek_index.py -i url.txt -o hasil -t 3

   - `-i` = file input URL  
   - `-o` = folder untuk simpan hasil (bisa folder baru atau `.`)  
   - `-t` = jumlah thread, maksimal 5 (default 3)  

4. Tunggu prosesnya selesai, kamu bakal dapet dua file:  
   - `Indexed.txt` — backlink yang sudah Google kenal dan index  
   - `Non-Indexed.txt` — backlink yang belum terindex, bisa kamu follow-up  

---

Catatan kecil

- Google agak sensitif kalau request terlalu cepat, makanya saya kasih delay dan batasi thread.  
- Tools ini gratis, jadi jangan berharap seperti API resmi Google ya. Tapi buat cek backlink skala kecil-sedang ini sudah sangat membantu!  
- Gunakan dengan bijak dan jangan spam request ke Google.  

---

Penutup

Semoga tools ini bermanfaat buat kamu yang sedang serius bangun backlink. Kalau ada request fitur atau butuh bantuan, jangan ragu kontak saya via Telegram: [@forbidden220222](https://t.me/forbidden220222)  

Salam SEO dan tetap semangat optimasi!  

— forbidden403-lt  
