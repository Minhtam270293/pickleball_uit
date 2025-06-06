# UIT Pickleball API

This project is a Django REST Framework backend for managing users, courts, reviews, and guides for pickleball at UIT.

## Getting Started

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd UIT_pickleball
```

### 2. Install dependencies

It’s recommended to use a virtual environment:

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

### 3. Run migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (for admin access)

```sh
python manage.py createsuperuser
```

### 5. Start the development server

```sh
python manage.py runserver
```

---

## API Endpoints

- **Người dùng:** `/api/users/`
- **Sân:** `/api/courts/`
- **Đánh giá sân:** `/api/reviews/`
- **Hướng dẫn:** `/api/guides/`

You can access the browsable API at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

---

## Testing the API

You can use the browsable API in your browser, or tools like [Postman](https://www.postman.com/) or `curl`.

### Example: Create a new court

```json
POST /api/courts/
{
  "ten_san": "Sân A",
  "dia_diem": "UIT Campus",
  "gia_thue_theo_gio": "100000.00",
  "mo_ta": "Sân ngoài trời",
  "so_san_con": 2,
  "gio_mo_cua": "08:00",
  "gio_dong_cua": "22:00"
}
```

### Example: Create a new review

```json
POST /api/reviews/
{
  "diem": 4.5,
  "noi_dung": "Sân đẹp, rộng rãi.",
  "san_id": 1,
  "nguoi_dung_id": 1
}
```

### Example: Create a new guide

```json
POST /api/guides/
{
  "tieu_de": "Cách chơi cơ bản",
  "noi_dung": "Hướng dẫn chi tiết...",
  "nguoi_tao_id": 1,
  "cap_do": "de"
}
```

---

## Admin Panel

Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials to manage all data.

---

## Notes

- All times should be in 24-hour format, e.g., `"08:00"`.
- For `cap_do` in guides, valid choices are: `"de"`, `"trung binh"`, `"kho"`.
- If you get validation errors, check the error message for required fields or invalid choices.

---

Happy coding!
