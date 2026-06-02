# Blog API System (DRF)

Bu loyiha Django Rest Framework yordamida yaratilgan Blog API tizimi hisoblanadi.  
Foydalanuvchilar ro'yxatdan o'tadi, login qiladi, post yaratadi, comment yozadi va like bosadi.

---

## Texnologiyalar

- Python
- Django
- Django REST Framework
- Token Authentication
- SQLite

---

## O'rnatish

### 1. Repository clone qilish

```bash
git clone https://github.com/username/blog-api.git
cd blog-api
```

### 2. Virtual muhit yaratish va faollashtirish

```bash
# Yaratish
python -m venv venv

# Faollashtirish — Windows
venv\Scripts\activate

# Faollashtirish — macOS / Linux
source venv/bin/activate
```

### 3. Kerakli paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Migratsiyalarni bajarish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yaratish (ixtiyoriy)

```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish

```bash
python manage.py runserver
```
