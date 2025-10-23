# Meeting Planner

Meeting Planner, şirket çalışanlarının toplantılarını yönetebileceğiniz bir **FastAPI** tabanlı uygulamadır. Projede kullanıcılar, departmanlar ve toplantılar yönetilebilir, toplantı çakışmaları kontrol edilir ve API üzerinden sorgulanabilir.

---

## 🛠️ Teknolojiler

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL (Docker container)
- Pydantic
- Uvicorn
- Docker & Docker Compose (opsiyonel)
- Swagger ve Redoc dokümantasyonu (otomatik)

---

## ⚡ Özellikler

- Çalışan (Employee) yönetimi: ekleme, silme, listeleme
- Departman yönetimi: ekleme, silme, listeleme, güncelleme
- Toplantı yönetimi: oluşturma, güncelleme, silme
- Katılımcılara göre toplantı çakışma kontrolü
- Çalışan müsaitlik sorgulama (availability)
- Rol bazlı erişim (ADMIN, EMPLOYEE)
- API dokümantasyonu: Swagger ve Redoc ile otomatik

---

## 🚀 Kurulum

1. **Repo klonlama ve sanal ortam oluşturma**
```bash
git clone <repo-url>
cd meeting-planner
python -m venv .venv
Sanal ortamı aktifleştir

Windows:

powershell
Kodu kopyala
.venv\Scripts\activate
Linux / Mac:

bash
Kodu kopyala
source .venv/bin/activate
Gerekli paketleri yükle

bash
Kodu kopyala
pip install -r requirements.txt
PostgreSQL’i Docker ile başlat

bash
Kodu kopyala
docker run --name postgres_db -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -d postgres:17
.env dosyası oluştur ve bağlantı bilgisini ekle

bash
Kodu kopyala
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/postgres
Uygulamayı çalıştır

bash
Kodu kopyala
uvicorn app.main:app --reload
📄 API Dokümantasyonu
Uygulama çalıştıktan sonra API dokümantasyonu otomatik olarak hazır:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

🔑 Kullanım
Çalışan ekleme: /employees/ (POST)

Departman ekleme: /departments/ (POST)

Toplantı ekleme: /meetings/ (POST)

Toplantı çakışma kontrolü: /meetings/availability/ (POST, body ile)

Yetki kontrolü: ADMIN ve EMPLOYEE rolüne göre erişim

Tüm CRUD işlemleri için gerekli endpointler ve body parametreleri Swagger veya Redoc üzerinden detaylı görülebilir.

📦 Gereksinimler
Python 3.10+

Docker (opsiyonel)

PostgreSQL

pip ile yüklenmiş Python paketleri (requirements.txt)

📌 Notlar
Departman silindiğinde o departmana ait çalışanların department_id alanı otomatik olarak None yapılır.

Toplantı güncelleme veya ekleme sırasında, katılımcıların diğer toplantı çakışmaları kontrol edilir.

Ortam değişkenleri için .env dosyası kullanılır (python-dotenv ile yüklenir).