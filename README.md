# Hodo.id - RESTful API Katalog Restoran & Menu

API untuk mengelola restoran dan menu makanan serta minuman dengan sistem autentikasi JWT, relasi database, serta filter menu berdasarkan kategori.

---

## Tentang Proyek

Hodo.id adalah backend service yang menyediakan:

- Manajemen restoran (CRUD)
- Manajemen menu makanan dan minuman (CRUD)
- Autentikasi pengguna dengan JWT
- Filter menu berdasarkan kategori (Makanan / Minuman)
- Proteksi endpoint berdasarkan role (user / admin)

Proyek ini dikembangkan sebagai pemenuhan Ujian Tengah Semester (UTS) mata kuliah Pemrograman Web Lanjutan.

---

## Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Autentikasi | JWT + bcrypt |
| Dokumentasi | Swagger UI |

---

## Struktur Proyek

```
hodo-id-backend/
│
├── auth/                 # Autentikasi JWT
│   └── security.py
│
├── models/               # Model database (SQLAlchemy)
│   ├── user.py
│   ├── restaurant.py
│   └── menu.py
│
├── schemas/              # Validasi data (Pydantic)
│   ├── user.py
│   ├── restaurant.py
│   └── menu.py
│
├── routers/              # Endpoint API
│   ├── restaurants.py
│   └── menus.py
│
├── postman/              # Koleksi Postman
├── screenshots/          # Dokumentasi tampilan
│
├── database.py           # Koneksi database
├── main.py               # Entry point
├── requirements.txt
└── .gitignore
```

---

## Menjalankan Proyek

Prasyarat
- Python 3.12+
- Git

Langkah-langkah

```bash
git clone https://github.com/ishmahsalter/hodo-id-backend.git
cd hodo-id-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Server berjalan di: `http://127.0.0.1:8000`

Dokumentasi API (Swagger): `http://127.0.0.1:8000/docs`

---

## API Reference

### Autentikasi

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| POST | /register | Registrasi pengguna baru |
| POST | /login | Login, mendapat token JWT |
| GET | /users/me | Profil pengguna yang login |
| GET | /users | Semua user (hanya admin) |

### Restoran

| Method | Endpoint | Fungsi | Auth |
|--------|----------|--------|------|
| GET | /restaurants | Semua restoran | Tidak |
| GET | /restaurants/{id} | Detail restoran | Tidak |
| POST | /restaurants | Tambah restoran | Ya |
| PUT | /restaurants/{id} | Update restoran | Ya (pemilik) |
| DELETE | /restaurants/{id} | Hapus restoran | Ya (pemilik) |

### Menu

| Method | Endpoint | Fungsi | Auth |
|--------|----------|--------|------|
| GET | /menus | Semua menu (bisa filter category) | Tidak |
| GET | /menus/{id} | Detail menu | Tidak |
| POST | /menus | Tambah menu | Ya (pemilik restoran) |
| PUT | /menus/{id} | Update menu | Ya (pemilik restoran) |
| DELETE | /menus/{id} | Hapus menu | Ya (pemilik restoran) |
| GET | /menus/restaurant/{id} | Menu berdasarkan restoran | Tidak |

---

## Testing

Gunakan Postman untuk menguji endpoint.

Koleksi Postman: `/postman/Hodo.id API - UTS PWL.postman_collection.json`

### Contoh Request

Register
```
POST /register
Content-Type: application/json

{
  "name": "Ishmah",
  "email": "ishmah@hodo.com",
  "password": "rahasiaya123",
  "role": "user"
}
```

Login
```
POST /login
Content-Type: application/x-www-form-urlencoded

username: ishmah@hodo.com
password: rahasiaya123
```

Buat Restoran
```
POST /restaurants
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Hodo House Cafe",
  "address": "Jl. Sultan Alauddin No. 45, Makassar",
  "phone": "081234567891",
  "image_url": "https://i.imgur.com/ho7l3KN.png"
}
```

Buat Menu Makanan
```
POST /menus
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Beef Blackpepper Ricebowl",
  "price": 35000,
  "category": "Makanan",
  "restaurant_id": 1
}
```

Buat Menu Minuman
```
POST /menus
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Greentea",
  "price": 15000,
  "category": "Minuman",
  "restaurant_id": 1
}
```

---

## Entity Relationship Diagram (ERD)

Relasi:
- users (1) --> restaurants (M) : satu user dapat memiliki banyak restoran
- restaurants (1) --> menus (M) : satu restoran dapat memiliki banyak menu

Tabel users:
- id (integer, primary key)
- name (string)
- email (string, unique)
- hashed_password (string)
- role (string, default: 'user')

Tabel restaurants:
- id (integer, primary key)
- name (string)
- description (string, nullable)
- address (string)
- phone (string)
- image_url (string, nullable)
- owner_id (integer, foreign key ke users.id)

Tabel menus:
- id (integer, primary key)
- name (string)
- description (string, nullable)
- price (float)
- category (string)
- image_url (string, nullable)
- restaurant_id (integer, foreign key ke restaurants.id)

---

## Dokumentasi

Folder `screenshots/` berisi:
- Tampilan Swagger UI
- Hasil pengujian dengan Postman
- Bukti server running

---

## Link Penting

| Item | Link |
|------|------|
| Repository GitHub | https://github.com/ishmahsalter/hodo-id-backend |
| Dokumentasi API (Swagger) | http://127.0.0.1:8000/docs |
| Koleksi Postman | /postman/Hodo.id API - UTS PWL.postman_collection.json |

---

## Author

Ishmah Nurwasilah  
NIM: H071241019  
Mata Kuliah: Pemrograman Web Lanjutan  
Semester 4 (Genap)  
Universitas Hasanuddin

---

## Lisensi

Proyek ini dikembangkan untuk keperluan akademik UTS.
```

---

**README sudah tanpa emoji dan formatnya berbeda dari milik Alan. Ada yang mau disesuaikan lagi?** 😊
