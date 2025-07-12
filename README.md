Backlink Index Checker

Halo teman-teman SEO!

Tools sederhana ini saya buat untuk bantu kamu yang sering cek apakah backlink yang kamu pasang sudah terindex Google atau belum. Kadang, pasang backlink udah capek-capek tapi ternyata belum terindex sama Google, kan sayang banget. Tools ini simple tapi cukup powerful untuk cek banyak URL sekaligus.

Kenapa saya buat tools ini?

Sebagai SEO specialist, saya juga sering harus cek ribuan backlink. Kalau manual, makan waktu banget. Tools yang ada kadang mahal dan terlalu kompleks. Makanya saya bikin ini: gampang, gratis, dan bisa dipakai sendiri kapan aja.

Apa yang tools ini bisa lakukan?

- Cek apakah backlink kamu sudah terindex di Google secara real-time
- Pakai multi-threading biar proses lebih cepat tapi tetep aman, maksimal 5 thread
- Random User-Agent biar request gak gampang ketahuan bot
- Ada delay random antara 30 sampai 90 detik supaya Google gak curiga
- Bisa pakai proxy gratis (proxy aktif penting banget kalau mau cek banyak backlink)
- Hasilnya langsung dipisah: yang sudah terindex dan yang belum

Cara pakai?

1. Siapkan file url.txt berisi URL backlink, satu baris satu URL. Contoh:

https://contohsitus.com/backlink1  
https://contohsitus.com/backlink2

2. Siapkan file User-agent.txt berisi daftar user-agent yang cukup banyak (minimal 100 user-agent). Bisa cari di internet banyak list user-agent gratis.

3. Siapkan file proxy.txt berisi daftar proxy publik gratis (kalau kamu mau cek banyak backlink). Proxy aktif dan banyak itu penting supaya gak kena blok Google.

4. Pastikan Python sudah terinstall dan module requests + beautifulsoup4 sudah siap:

pip install requests beautifulsoup4

5. Jalankan scriptnya:

python cek_index.py -i url.txt -o hasil -t 3

-t itu jumlah thread, maksimal 5 (default 3)

Nanti hasilnya di folder 'hasil' (atau folder yang kamu pilih) akan ada dua file:

Indexed.txt : backlink yang sudah Google kenal  
Non-Indexed.txt : backlink yang belum terindex

Catatan penting:

- Google cukup sensitif dengan request yang terlalu cepat atau banyak, makanya harus pakai delay dan batasi jumlah thread.  
- Proxy publik kadang gak stabil, jadi harus pakai banyak dan cek secara berkala.  
- Tools ini gratis dan bukan API resmi Google, jadi wajar kalau ada batasan dan kadang kena blok.  
- Pakailah dengan bijak supaya gak merugikan pihak lain dan akun kamu tetap aman.

Semoga tools ini bisa membantu pekerjaan SEO kamu sehari-hari. Kalau ada pertanyaan atau mau request fitur, silakan hubungi saya di Telegram: [@forbidden220222](https://t.me/forbidden220222)

Terima kasih sudah memakai tools ini, semoga backlink kamu cepat terindex dan ranking di Google makin naik!

Salam optimasi,  
forbidden403-lt
