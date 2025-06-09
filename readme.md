# UIT Pickleball API

Dự án này là một backend Django REST Framework để quản lý người dùng, sân, đánh giá và hướng dẫn của website liên quan đến pickleball.

## Bắt đầu

### 1. Clone repository

```sh
git clone <your-repo-url>
cd UIT_pickleball
```

### 2. Cài đặt phụ thuộc

Nên sử dụng môi trường ảo:

```sh
python -m venv venv
venv\Scripts\activate  # Trên Windows
# source venv/bin/activate  # Trên Mac/Linux

pip install -r requirements.txt
```

### 3. Chạy migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Tạo superuser (quản trị viên)

```sh
python manage.py createsuperuser
```

### 5. Khởi động server

```sh
python manage.py runserver
```

---

## Các endpoint API

- **Người dùng:** `/api/users/`
- **Sân:** `/api/courts/`
- **Đánh giá sân:** `/api/reviews/`
- **Hướng dẫn:** `/api/guides/`
- **Đặt sân:** `/api/bookings/`
- **Tính doanh thu tất cả sân:** `/api/courts/revenue/`

Bạn có thể truy cập API giao diện web tại [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

---

## Kiểm thử API

Bạn có thể sử dụng giao diện web, hoặc các công cụ như [Postman](https://www.postman.com/) hoặc `curl`.

### Ví dụ: Tạo sân mới

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

### Ví dụ: Tạo đánh giá mới

```json
POST /api/reviews/
{
  "diem": 4.5,
  "noi_dung": "Sân đẹp, rộng rãi.",
  "san_id": 1,
  "nguoi_dung_id": 1
}
```

### Ví dụ: Tạo hướng dẫn mới

```json
POST /api/guides/
{
  "tieu_de": "Cách chơi cơ bản",
  "noi_dung": "Hướng dẫn chi tiết...",
  "nguoi_tao_id": 1,
  "cap_do": "de"
}
```

### Ví dụ: Đặt sân mới

```json
POST /api/bookings/
{
  "thoi_gian_bat_dau": "09:00",
  "thoi_gian_ket_thuc": "11:00",
  "san_id": 1,
  "nguoi_dung_id": 1,
  "so_luong_san": 1
}
```

### Ví dụ: Tính doanh thu tất cả sân

```json
GET /api/courts/revenue/
```

_Phản hồi:_

```json
[
  {
    "id": 1,
    "ten_san": "Sân A",
    "doanh_thu": "200000.00"
  },
  ...
]
```

---

## Trang quản trị

Truy cập [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) và đăng nhập bằng tài khoản superuser để quản lý dữ liệu.

---

## Ghi chú

- Tất cả thời gian nên ở định dạng 24h, ví dụ: `"08:00"`.
- Đối với `cap_do` trong hướng dẫn, các lựa chọn hợp lệ là: `"de"`, `"trung binh"`, `"kho"`.
- Nếu gặp lỗi xác thực, hãy kiểm tra thông báo lỗi để biết trường nào thiếu hoặc giá trị không hợp lệ.

---

## Quy tắc & Ràng buộc nghiệp vụ

- Người dùng chỉ được đánh giá sân mà họ đã từng đặt.
- Thời gian đặt phải nằm trong giờ mở cửa và đóng cửa của sân.
- Số lượng sân đặt không được vượt quá số sân còn lại.
- Tổng tiền được tính toán tự động khi đặt sân.
- Doanh thu các sân chỉ được cập nhật lại khi truy cập `/api/courts/revenue/`.
- Số điện thoại phải là duy nhất và bắt đầu bằng 0, gồm 10–11 chữ số.
- Độ khó hướng dẫn (`cap_do`) phải là `"de"`, `"trung binh"`, `"kho"` hoặc để trống.

---
