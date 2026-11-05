# Website Bán Quần Áo Thời Trang (Fashion Store)
> **Đồ Án Môn Học: Lập Trình Python Nâng Cao**  
> **Trường Đại Học Văn Lang - Khoa Công Nghệ Thông Tin**  
> **Giảng viên hướng dẫn:** ThS. Nguyễn Thị Mỹ Linh  

---

## 1. Công Nghệ Sử Dụng & Chuẩn Đầu Ra (CLO)
- **CLO2 (50%) - Web Framework:** Flask 3.1, Jinja2, Bootstrap 5, Flask-WTF, Flask-SQLAlchemy (SQLite), Flask-Login, Flask-Mail.
- **CLO3 (10%) - Lập trình mạng & API:** 
  - Tích hợp gọi API VietQR (`https://api.vietqr.io/v2/banks`) bằng `requests` & JSON để tải danh sách các ngân hàng Việt Nam.
  - Tự động sinh mã VietQR chuyển khoản ngân hàng chính xác số tiền & nội dung đơn hàng.
  - Cung cấp REST API nội bộ: `/api/v1/products`, `/api/v1/categories`, `/api/v1/orders/<code_order>`, `/api/v1/banks`.
- **CLO4 (20%) - Thư viện Python nâng cao:** `Pillow` (tự động tối ưu và resize ảnh upload vuông 600x600), `python-dotenv`, `requests`.
- **CLO5 (10%) - Cấu trúc Large Application:** Phân chia rõ ràng `models/`, `routes/` (Blueprints), `forms/`, `services/`, `templates/`.
- **CLO6 (10%) - Đóng góp & Vấn đáp nhóm 3 thành viên.**

---

## 2. Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### Bước 1: Kích hoạt Virtual Environment (nếu đã tạo sẵn) hoặc tạo mới:
```bash
# Tạo venv nếu chưa có
python -m venv venv

# Kích hoạt trên Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Hoặc Windows CMD:
.\venv\Scripts\activate.bat
```

### Bước 2: Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi tạo CSDL & Nạp dữ liệu mẫu (Sản phẩm quần áo, tài khoản demo):
```bash
python seed_data.py
```

### Bước 4: Chạy ứng dụng:
```bash
python run.py
```
Truy cập trình duyệt: **`http://127.0.0.1:5000`**

---

## 3. Tài Khoản Demo Để Giảng Viên Chấm Điểm
| Vai trò | Tên đăng nhập | Mật khẩu | Chức năng nổi bật |
| :--- | :--- | :--- | :--- |
| **Quản trị (Admin)** | `admin` | `admin123` | Dashboard doanh thu, CRUD sản phẩm, upload ảnh bằng Pillow, duyệt đơn hàng. |
| **Khách hàng** | `khachhang` | `123456` | Xem giỏ hàng, đặt hàng thanh toán VietQR, xem lịch sử mua sắm. |

---

## 4. Chạy Kiểm Thử Tự Động (Automated Testing)
```bash
python test_app.py
```
Kiểm thử tự động 10 kịch bản cốt lõi: Trang chủ, Danh mục, Chi tiết, Giỏ hàng, Đặt hàng VietQR, REST API, Đăng nhập, Admin Dashboard.
