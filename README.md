# Sistem Informasi Seleksi Asisten Praktikum Laboratorium UMS
GIF demo ada di bawah
## Techstack
- Django
- Sveltekit (built to static files)
- PDFKit

## Fitur
### Roles
- Admin
- Asisten
- Koordinator
- User (pendaftar)
### Autentikasi
- Login
- Register
- Verify Email
### Persyaratan (Pengumuman Pendaftaran)
- Batas waktu pendaftaran
- Upload gambar pengumuman
- Create, Read, Update, Delete
### Pendaftaran
- Verifikasi IPK, semester, batas waktu, file
- Create, Read, Update, Delete
### Berkas Pendaftaran
- History file untuk masing-masing berkas
- Revisi / Komentar untuk setiap file berkas
- Download file berkas
- Upload file berkas
- Tracking jumlah berkas yang butuh revisi dan telah direvisi
### User Dashboard
- Edit pendaftaran dan berkas
- Berkas pendaftaran
- Pagination dan filter
- Download PDF
### Admin Django Dashboard
- CRUD untuk Persyaran, Pendaftaran, Asisten
- Pagination dan filter
- Download PDF
### Admin/Koordinator/Asisten Dashbaord
- CRUD untuk Pendaftaran
- Berkas pendaftaran
- Email untuk setiap step pendaftaran
- Memasukkan dan meninjau nilai ujian-ujian pendaftaran
- Melanjutkan step pendaftaran
- Mengirim LOA (Letter of Acceptance)
- Pagination dan filter
- Download PDF
### Asisten Dashboard
- Pagination dan filter
- DOwnload PDF
## Demo GIF
Demo flow atau setiap fitur web untuk role User dan Admin
### User
(demo gif maybe still loading (3 MB))

![demo gif User](https://github.com/user-attachments/assets/d07254ea-bb80-4bb9-b1a9-e30524f4706c)
- Register
- Verify Email
- Login
- Persyaratan (pengumuman pendaftaran)
- Buat Pendaftaran
- User Dashboard
### Admin
(demo gif maybe still loading (5 MB))

![demo GIF Admin](https://github.com/user-attachments/assets/7d84c407-d8c8-4833-9629-ca24457f537d)
- Admin Django Dashboard
- Admin Dashboard
- Revisi Berkas Pendaftaran
- Progress Step Pendaftaran
- Email Step Pendaftaran dan LOA
- Download PDF
- Asisten Dashboard
- Download PDF
- CRUD Persyaratan (pengumuman pendaftaran)
