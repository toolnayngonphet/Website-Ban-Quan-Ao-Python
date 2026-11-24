import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_simple_report():
    doc = docx.Document()
    
    # Canh lề chuẩn A4: Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Style chuẩn: Times New Roman, 13pt, cách dòng 1.3 - 1.5, màu đen
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    def p(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=13, space_after=6, space_before=0):
        para = doc.add_paragraph()
        para.alignment = align
        para.paragraph_format.space_after = Pt(space_after)
        para.paragraph_format.space_before = Pt(space_before)
        para.paragraph_format.line_spacing = 1.3
        if text:
            run = para.add_run(text)
            run.bold = bold
            run.italic = italic
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.font.color.rgb = RGBColor(0, 0, 0)
        return para

    def h1(text):
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(14)
        para.paragraph_format.space_after = Pt(6)
        para.paragraph_format.keep_with_next = True
        run = para.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return para

    def h2(text):
        para = doc.add_paragraph()
        para.paragraph_format.space_before = Pt(10)
        para.paragraph_format.space_after = Pt(4)
        para.paragraph_format.keep_with_next = True
        run = para.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return para

    def add_image(image_path, caption_text):
        if os.path.exists(image_path):
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_before = Pt(6)
            para.paragraph_format.space_after = Pt(2)
            run = para.add_run()
            run.add_picture(image_path, width=Inches(5.4))
            
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.paragraph_format.space_before = Pt(2)
            cap.paragraph_format.space_after = Pt(8)
            run_cap = cap.add_run(caption_text)
            run_cap.italic = True
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(11)

    def set_table_borders(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(r'''
            <w:tblBorders %s>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            </w:tblBorders>
        ''' % nsdecls('w'))
        tblPr.append(borders)

    def set_header_bg(cell):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(r'<w:shd %s w:fill="F2F2F2"/>' % nsdecls('w'))
        tcPr.append(shd)

    # ==================== TRANG BÌA ====================
    p("TRƯỜNG ĐẠI HỌC VĂN LANG", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=2)
    p("KHOA CÔNG NGHỆ THÔNG TIN", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=30)

    p("BÁO CÁO ĐỒ ÁN MÔN HỌC", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=15, space_after=4)
    p("LẬP TRÌNH PYTHON NÂNG CAO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, space_after=4)
    p("Mã học phần: 71ITSE31003 – Nhóm lớp: 253_71ITSE31003_01", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=36)

    p("ĐỀ TÀI: XÂY DỰNG WEBSITE BÁN QUẦN ÁO THỜI TRANG BẰNG FLASK", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=40)

    p("Giảng viên hướng dẫn: ThS. Nguyễn Thị Mỹ Linh", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, size=13, space_after=6)
    p("Nhóm thực hiện: Nhóm 03 Sinh viên", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, size=13, space_after=8)

    # Bảng thành viên nhóm
    table0 = doc.add_table(rows=4, cols=4)
    table0.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table0)
    headers0 = ["STT", "MSSV", "Họ và tên", "Nhiệm vụ chính"]
    col_w0 = [Inches(0.6), Inches(1.3), Inches(2.1), Inches(2.5)]

    for i, h in enumerate(headers0):
        cell = table0.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_header_bg(cell)

    members_data = [
        ("1", "", "", "Cấu trúc dự án, thiết kế CSDL, chức năng Admin, upload ảnh (35%)"),
        ("2", "", "", "Giao diện Jinja2, Bootstrap 5, FlaskForm, tìm kiếm & phân trang (33%)"),
        ("3", "", "", "Giỏ hàng, đặt hàng, API VietQR (CLO3), REST API, gửi email (32%)")
    ]

    for r_idx, row in enumerate(members_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table0.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 1):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row in table0.rows:
        for c_idx, w in enumerate(col_w0):
            row.cells[c_idx].width = w

    p("", space_after=40)
    p("TP. Hồ Chí Minh, tháng 11 năm 2026", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)

    doc.add_page_break()

    # ==================== NHẬN XÉT CỦA GIẢNG VIÊN & RUBRIC ====================
    p("NHẬN XÉT VÀ ĐÁNH GIÁ CỦA GIẢNG VIÊN", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=12)
    p("................................................................................................................................................", space_after=6)
    p("................................................................................................................................................", space_after=6)
    p("................................................................................................................................................", space_after=6)
    p("................................................................................................................................................", space_after=14)

    p("Bảng đánh giá theo Rubric của học phần", bold=True, size=13, space_after=8)

    table1 = doc.add_table(rows=7, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)
    headers1 = ["CLO", "Nội dung đánh giá", "Trọng số", "Điểm"]
    col_w1 = [Inches(0.9), Inches(3.9), Inches(0.9), Inches(0.8)]

    for i, h in enumerate(headers1):
        cell = table1.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_header_bg(cell)

    rubric_rows = [
        ("CLO2", "Thiết kế và xây dựng ứng dụng web Flask: template, form, database, email", "50%", ""),
        ("CLO3", "Lập trình mạng: urllib, API key, JSON/XML, lập trình mạng Internet", "10%", ""),
        ("CLO4", "Sử dụng thành thạo thư viện Python (Flask, flask-wtf, urllib, requests, Pillow...)", "20%", ""),
        ("CLO5", "Kỹ năng viết báo cáo, module hóa code, cấu trúc rõ ràng, dễ bảo trì", "10%", ""),
        ("CLO6", "Thái độ nghiêm túc, chủ động trong thực hiện và trình bày đồ án", "10%", ""),
        ("Tổng", "Tổng điểm", "100%", "")
    ]

    for r_idx, row in enumerate(rubric_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = table1.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 2, 3):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if r_idx == 6:
                cell.paragraphs[0].runs[0].bold = True

    for row in table1.rows:
        for c_idx, w in enumerate(col_w1):
            row.cells[c_idx].width = w

    p("", space_after=16)

    # ==================== MỤC LỤC TỰ ĐỘNG CHUẨN WORD ====================
    p("MỤC LỤC", bold=True, size=13, space_after=8)

    # Chèn trường TOC chuẩn của Word (sẽ có nút Update Field khi nhấp chuột phải)
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.space_after = Pt(12)
    run_toc = toc_p.add_run()
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run_toc._r.append(fldChar1)
    run_toc._r.append(instrText)
    run_toc._r.append(fldChar2)
    run_toc._r.append(fldChar3)

    # Hiển thị nội dung mục lục tĩnh sẵn sàng để xem ngay
    toc_static = [
        ("1. GIỚI THIỆU ĐỀ TÀI", 3),
        ("  1.1. Mô tả bài toán", 3),
        ("  1.2. Mục tiêu và phạm vi", 3),
        ("  1.3. Công nghệ sử dụng", 3),
        ("  1.4. Phân công công việc trong nhóm", 4),
        ("2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", 4),
        ("  2.1. Chức năng của hệ thống", 4),
        ("  2.2. Thiết kế cơ sở dữ liệu", 5),
        ("  2.3. Thiết kế giao diện", 5),
        ("3. XÂY DỰNG ỨNG DỤNG VỚI FLASK", 6),
        ("  3.1. Môi trường và cấu trúc dự án", 6),
        ("  3.2. Routes và xử lý nghiệp vụ", 6),
        ("  3.3. Templates với Jinja2", 7),
        ("  3.4. Web Forms với Flask-WTF", 7),
        ("  3.5. Cơ sở dữ liệu với Flask-SQLAlchemy", 7),
        ("  3.6. Gửi email với Flask-Mail", 8),
        ("  3.7. Lập trình mạng và tích hợp API (CLO3)", 8),
        ("  3.8. Chức năng mở rộng của nhóm", 9),
        ("4. KẾT QUẢ VÀ KIỂM THỬ", 9),
        ("  4.1. Kết quả giao diện", 9),
        ("  4.2. Kiểm thử chức năng", 11),
        ("5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 11),
        ("TÀI LIỆU THAM KHẢO", 12),
        ("PHỤ LỤC", 12)
    ]
    for item, pg in toc_static:
        para_toc = doc.add_paragraph()
        para_toc.paragraph_format.space_after = Pt(2)
        para_toc.paragraph_format.line_spacing = 1.15
        para_toc.add_run(item)
        dots_count = max(5, 75 - len(item) * 2)
        para_toc.add_run(" " + "." * dots_count + " ").font.color.rgb = RGBColor(128, 128, 128)
        para_toc.add_run(str(pg))

    doc.add_page_break()

    # ==================== NỘI DUNG CHÍNH (ĐƠN GIẢN, RÕ RÀNG) ====================

    # CHƯƠNG 1
    h1("1. GIỚI THIỆU ĐỀ TÀI")
    
    h2("1.1. Mô tả bài toán")
    p("Hiện nay, việc mua bán quần áo qua mạng rất phổ biến. Tuy nhiên, nhiều cửa hàng nhỏ vẫn nhận đơn thủ công qua tin nhắn và yêu cầu khách chuyển khoản rồi chụp màn hình gửi lại, vừa mất thời gian đối soát vừa dễ nhầm lẫn số tiền hoặc nội dung.")
    p("Đề tài của nhóm là xây dựng một website bán quần áo thời trang hoàn chỉnh. Người mua có thể xem sản phẩm, chọn size, màu sắc, thêm vào giỏ và đặt hàng. Hệ thống hỗ trợ thanh toán COD hoặc tự động tạo mã QR VietQR có sẵn số tiền và mã đơn để người mua quét thanh toán trên app ngân hàng. Về phía quản lý, chủ shop có trang admin để theo dõi đơn hàng, cập nhật trạng thái và quản lý hàng trong kho.")

    h2("1.2. Mục tiêu và phạm vi")
    p("Mục tiêu của đề tài:")
    p("• Xây dựng website bằng Flask theo đúng mô hình Large Application Structure.")
    p("• Đầy đủ các chức năng: đăng ký, đăng nhập (Flask-Login), xem danh sách, chi tiết, giỏ hàng, đặt hàng, quản lý sản phẩm (CRUD), tìm kiếm và phân trang.")
    p("• Đáp ứng chuẩn CLO3 (Lập trình mạng): Dùng thư viện requests đọc dữ liệu JSON từ API VietQR để lấy danh sách ngân hàng; tự sinh link ảnh mã QR thanh toán theo từng đơn; tự xây dựng REST API trả về JSON cho các sản phẩm.")
    p("• Gửi email xác nhận đơn hàng qua Flask-Mail và dùng thư viện Pillow để xử lý ảnh khi admin upload.")
    p("Phạm vi: Ứng dụng tập trung vào nghiệp vụ bán lẻ các mặt hàng quần áo (áo thun, sơ mi, quần jean, áo khoác, váy...). Cơ sở dữ liệu dùng SQLite để dễ dàng chạy thử và nộp bài.")

    h2("1.3. Công nghệ sử dụng")
    p("• Python 3.11, Flask 3.1.0.")
    p("• Giao diện: Jinja2, Bootstrap 5.3, Bootstrap Icons.")
    p("• CSDL: SQLite, thư viện Flask-SQLAlchemy 3.1.1.")
    p("• Biểu mẫu & Xác thực: Flask-WTF 1.2.2, Flask-Login 0.6.3.")
    p("• Lập trình mạng & API: requests 2.32, urllib.parse, json.")
    p("• Xử lý ảnh: Pillow 11.1.")
    p("• Gửi mail: Flask-Mail 0.10.0.")
    p("• Quản lý mã nguồn & Deploy: Git, GitHub, Gunicorn, Render.")

    h2("1.4. Phân công công việc trong nhóm")
    p("• Thành viên 1 (35%): Cấu hình dự án (create_app, config.py), viết các model CSDL, làm chức năng Admin (CRUD sản phẩm, danh mục, upload ảnh bằng Pillow).")
    p("• Thành viên 2 (33%): Làm giao diện Jinja2 kế thừa base.html, Bootstrap 5, tạo các Form Flask-WTF, làm chức năng tìm kiếm sản phẩm và phân trang.")
    p("• Thành viên 3 (32%): Làm giỏ hàng Session, quy trình đặt hàng Checkout, tích hợp API VietQR (CLO3), viết REST API và cấu hình gửi email Flask-Mail.")

    # CHƯƠNG 2
    h1("2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    h2("2.1. Chức năng của hệ thống")
    p("Hệ thống chia làm 3 nhóm đối tượng sử dụng:")
    p("1. Khách hàng: Xem danh sách sản phẩm, lọc theo danh mục hoặc khoảng giá, tìm kiếm sản phẩm theo tên, xem chi tiết sản phẩm (chọn size, màu, số lượng), thêm vào giỏ hàng, đặt hàng và chọn thanh toán (COD hoặc VietQR), xem thông tin mã QR chuyển khoản.")
    p("2. Thành viên: Đăng ký tài khoản, đăng nhập, tự động điền sẵn địa chỉ khi mua hàng, xem lại lịch sử các đơn hàng đã đặt.")
    p("3. Quản trị viên (Admin): Đăng nhập tài khoản admin, xem thống kê doanh thu và đơn hàng, thêm/sửa/xóa sản phẩm và danh mục, cập nhật trạng thái đơn hàng (chờ xử lý, đã xác nhận, đang giao, hoàn thành, hủy).")

    h2("2.2. Thiết kế cơ sở dữ liệu")
    p("CSDL gồm 5 bảng chính được khai báo bằng Flask-SQLAlchemy:")
    p("Bảng 2.1. Mô tả các bảng dữ liệu (model SQLAlchemy)", bold=True, size=12)

    table2 = doc.add_table(rows=6, cols=4)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)
    headers2 = ["Tên Model", "Các cột chính", "Khóa", "Quan hệ / Ghi chú"]
    col_w2 = [Inches(1.1), Inches(2.7), Inches(0.9), Inches(1.8)]

    for i, h in enumerate(headers2):
        cell = table2.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_header_bg(cell)

    models_data = [
        ("User", "id, username, email, password_hash, full_name, phone, address, role, created_at", "id (PK)", "Quan hệ 1-n với Order. Phân quyền role='admin' hoặc 'customer'."),
        ("Category", "id, name, slug, description", "id (PK)", "Quan hệ 1-n với Product. Danh mục: Áo thun, Sơ mi, Quần jeans..."),
        ("Product", "id, name, slug, price, promotional_price, stock, image_url, sizes, colors, description, category_id", "id (PK), category_id (FK)", "Quan hệ n-1 với Category, 1-n với OrderItem."),
        ("Order", "id, order_code, user_id, customer_name, customer_email, customer_phone, shipping_address, total_amount, payment_method, payment_status, order_status", "id (PK), user_id (FK)", "Quan hệ n-1 với User, 1-n với OrderItem. Lưu thông tin người nhận và đơn hàng."),
        ("OrderItem", "id, order_id, product_id, product_name, price, quantity, size, color, subtotal", "id (PK), order_id (FK), product_id (FK)", "Quan hệ n-1 với Order. Lưu chi tiết từng món đồ khách mua.")
    ]

    for r_idx, row in enumerate(models_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table2.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 2):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row in table2.rows:
        for c_idx, w in enumerate(col_w2):
            row.cells[c_idx].width = w

    p("", space_after=8)

    h2("2.3. Thiết kế giao diện")
    p("Giao diện được thiết kế bằng Bootstrap 5 theo nguyên tắc kế thừa template Jinja2:")
    p("• base.html: Chứa thanh điều hướng (navbar), ô tìm kiếm, giỏ hàng, vùng hiển thị thông báo flash message, và chân trang (footer).")
    p("• Các trang con (index.html, shop.html, product_detail.html, cart.html, checkout.html, admin/...) kế thừa từ base.html giúp code gọn gàng, không bị lặp lại phần khung.")

    # CHƯƠNG 3
    h1("3. XÂY DỰNG ỨNG DỤNG VỚI FLASK")

    h2("3.1. Môi trường và cấu trúc dự án")
    p("Nhóm cài đặt môi trường ảo (venv) và các thư viện trong requirements.txt:")
    p("pip install -r requirements.txt", italic=True)
    p("Cấu trúc dự án theo mô hình Large Application Structure như sau:")
    p("• app/__init__.py: Hàm create_app(), đăng ký các blueprint, bộ lọc tiền VNĐ (currency).")
    p("• app/models/: Chứa các file user.py, category.py, product.py, order.py.")
    p("• app/routes/: Tách thành 5 blueprint: main.py, auth.py, cart.py, admin.py, api.py.")
    p("• app/forms/: Các form Flask-WTF xử lý đăng ký, đăng nhập, đặt hàng, thêm sản phẩm.")
    p("• app/services/: vietqr_service.py (xử lý gọi API VietQR) và mail_service.py (gửi email).")
    p("• app/templates/ & app/static/: Chứa file HTML và CSS, JS, ảnh upload.")
    p("• run.py: Khởi chạy ứng dụng.")

    h2("3.2. Routes và xử lý nghiệp vụ")
    p("Ứng dụng chia làm các route chính:")
    p("• main_bp: Route '/' (trang chủ), '/shop' (danh sách có tìm kiếm, lọc giá, phân trang), '/product/<slug>' (chi tiết sản phẩm).")
    p("• auth_bp: Route '/login', '/register', '/logout', '/profile'. Dùng Flask-Login để quản lý đăng nhập và current_user.")
    p("• cart_bp: Route '/cart' (xem giỏ), '/cart/add/<id>' (thêm vào giỏ), '/checkout' (đặt hàng), '/order/success/<order_code>' (trang hiển thị mã QR thanh toán).")
    p("• admin_bp: Bắt đầu bằng tiền tố /admin. Sử dụng hook @before_request kiểm tra nếu không phải admin (current_user.is_admin) thì chặn không cho vào.")

    h2("3.3. Templates với Jinja2")
    p("• Kế thừa: Các trang con sử dụng cú pháp {% extends 'base.html' %} và {% block content %}.")
    p("• Định dạng tiền VNĐ: Viết custom filter currency trong app/__init__.py để hiển thị số tiền dễ đọc (ví dụ: {{ product.price | currency }} -> 250.000 đ).")
    p("• Phân trang: Dùng đối tượng pagination của Flask-SQLAlchemy kết hợp vòng lặp {% for page_num in pagination.iter_pages() %} để tạo nút chuyển trang.")

    h2("3.4. Web Forms với Flask-WTF")
    p("Các form được tạo bằng Flask-WTF giúp tự động chống tấn công CSRF (csrf_token) và kiểm tra dữ liệu hợp lệ:")
    p("• LoginForm, RegisterForm: Kiểm tra bắt buộc nhập (DataRequired), đúng định dạng email (Email), mật khẩu tối thiểu 6 ký tự, mật khẩu nhập lại phải khớp (EqualTo).")
    p("• CheckoutForm: Kiểm tra họ tên, email, số điện thoại người nhận và địa chỉ giao hàng.")
    p("• ProductForm: Kiểm tra tên sản phẩm, giá bán, số lượng tồn kho và đuôi file ảnh upload (FileAllowed: jpg, jpeg, png, webp).")

    h2("3.5. Cơ sở dữ liệu với Flask-SQLAlchemy")
    p("Khai báo các model kế thừa db.Model. Thao tác CRUD thực hiện qua db.session:")
    p("• Thêm mới: db.session.add(obj) -> db.session.commit().")
    p("• Truy vấn và lọc: Product.query.filter_by(...).order_by(...).paginate(page=page, per_page=8).")
    p("• Cập nhật và xóa: Thay đổi thuộc tính đối tượng rồi commit, hoặc db.session.delete(obj).")

    h2("3.6. Gửi email với Flask-Mail")
    p("Cấu hình SMTP trong config.py (MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD).")
    p("Khi khách đặt hàng thành công, hàm send_order_confirmation(order) sẽ render file HTML email/order_confirmation.html chứa chi tiết các món đồ và tổng tiền, sau đó gửi đến email của khách. Quá trình gửi mail được cho chạy ngầm bằng threading.Thread để người dùng không phải chờ lâu.")

    h2("3.7. Lập trình mạng và tích hợp API (CLO3)")
    p("Để đáp ứng yêu cầu CLO3, nhóm thực hiện 3 nội dung kỹ thuật:")
    p("1. Dùng thư viện requests gọi API ngoài:")
    p("Hàm get_supported_banks() gửi request GET đến https://api.vietqr.io/v2/banks để lấy danh sách các ngân hàng tại Việt Nam dạng JSON và hiển thị tên/logo ngân hàng cho người mua tham khảo.")
    p("2. Tự động sinh mã VietQR theo đơn hàng:")
    p("Dùng module urllib.parse để nối các tham số số tiền, số tài khoản, mã đơn hàng vào đường dẫn:")
    p("https://img.vietqr.io/image/MB-0388999888-compact2.png?amount=...&addInfo=DH...&accountName=...", italic=True)
    p("Khi khách chọn thanh toán chuyển khoản, hệ thống hiển thị mã QR này để khách dùng app ngân hàng quét là tự điền đúng số tiền và nội dung đơn.")
    p("3. Xây dựng REST API nội bộ trả về JSON:")
    p("Tạo blueprint api_bp cung cấp các endpoint:")
    p("• GET /api/v1/products: Trả về JSON danh sách sản phẩm (có hỗ trợ lọc theo danh mục, tìm kiếm).")
    p("• GET /api/v1/orders/<order_code>: Trả về JSON thông tin đơn hàng.")
    p("• GET /api/v1/banks: Trả về JSON danh sách ngân hàng.")

    h2("3.8. Chức năng mở rộng của nhóm")
    p("• Xử lý ảnh bằng Pillow: Khi admin upload ảnh sản phẩm, hệ thống tự động đổi hệ màu sang RGB, resize ảnh về kích thước vuông chuẩn 600x600 px và nén chất lượng để web tải nhanh hơn.")
    p("• Giỏ hàng lưu trong Session: Cho phép lưu nhiều sản phẩm với các lựa chọn size và màu sắc khác nhau.")
    p("• Triển khai lên Cloud: Đã đưa mã nguồn lên GitHub và triển khai thử nghiệm trên Render.com với server Gunicorn.")

    # CHƯƠNG 4
    h1("4. KẾT QUẢ VÀ KIỂM THỬ")

    h2("4.1. Kết quả giao diện")
    p("Dưới đây là hình ảnh chụp thực tế các màn hình chức năng chính của website:")

    add_image('screenshots/hinh4_1_trang_chu.png', 'Hình 4.1. Giao diện Trang chủ (Banner, danh mục và sản phẩm nổi bật)')
    add_image('screenshots/hinh4_2_cua_hang.png', 'Hình 4.2. Giao diện Cửa hàng (Bộ lọc danh mục, lọc giá và phân trang)')
    add_image('screenshots/hinh4_3_chi_tiet_san_pham.png', 'Hình 4.3. Giao diện Chi tiết sản phẩm (Chọn size, màu, số lượng và thêm vào giỏ)')
    add_image('screenshots/hinh4_4_gio_hang.png', 'Hình 4.4. Giao diện Giỏ hàng (Cập nhật số lượng, xóa món và tính tổng tiền)')
    add_image('screenshots/hinh4_5_thanh_toan_vietqr.png', 'Hình 4.5. Đặt hàng thành công và mã QR VietQR tự động sinh cho đơn hàng')
    add_image('screenshots/hinh4_6_admin_dashboard.png', 'Hình 4.6. Bảng điều khiển Quản trị viên (Thống kê doanh thu, đơn hàng, hàng sắp hết)')
    add_image('screenshots/hinh4_7_admin_products.png', 'Hình 4.7. Trang quản lý danh sách sản phẩm của Quản trị viên (Thêm, sửa, xóa)')

    h2("4.2. Kiểm thử chức năng")
    p("Nhóm đã viết script kiểm thử tự động trong file test_app.py và kiểm tra trực tiếp trên giao diện:")
    p("Bảng 4.1. Kết quả kiểm thử chức năng", bold=True, size=12)

    table3 = doc.add_table(rows=11, cols=5)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)
    headers3 = ["TT", "Chức năng kiểm thử", "Dữ liệu thử", "Kết quả mong đợi", "Đánh giá"]
    col_w3 = [Inches(0.5), Inches(1.8), Inches(1.8), Inches(1.8), Inches(0.8)]

    for i, h in enumerate(headers3):
        cell = table3.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_header_bg(cell)

    test_rows = [
        ("1", "Tải trang chủ", "GET /", "Mã 200 OK, hiển thị danh mục và sản phẩm nổi bật", "Đạt"),
        ("2", "Lọc sản phẩm theo danh mục", "GET /shop?category=ao-thun-polo", "Mã 200 OK, chỉ hiện các sản phẩm áo thun", "Đạt"),
        ("3", "Tìm kiếm và sắp xếp giá", "GET /shop?q=áo&sort=price_asc", "Tìm ra đúng sản phẩm, giá xếp từ thấp đến cao", "Đạt"),
        ("4", "Xem chi tiết sản phẩm", "GET /product/ao-thun-cotton-oversize-basic", "Mã 200 OK, đủ nút chọn size, màu và giá", "Đạt"),
        ("5", "Thêm hàng vào giỏ", "POST /cart/add/1 (size: L, color: Đen)", "Giỏ hàng tăng thêm 1 món, cập nhật badge giỏ hàng", "Đạt"),
        ("6", "Đặt hàng và sinh mã VietQR", "POST /checkout (Tên, SĐT, chọn VIETQR)", "Tạo đơn hàng trong CSDL, sinh mã QR đúng số tiền", "Đạt"),
        ("7", "REST API danh sách sản phẩm", "GET /api/v1/products", "Trả về JSON chứa status: success và danh sách sản phẩm", "Đạt"),
        ("8", "API danh sách ngân hàng", "GET /api/v1/banks", "Gọi API VietQR thành công, trả về JSON ngân hàng", "Đạt"),
        ("9", "Đăng nhập tài khoản", "POST /login (admin / admin123)", "Đăng nhập thành công, điều hướng vào trang quản trị", "Đạt"),
        ("10", "Xem Dashboard Admin", "GET /admin/", "Mã 200 OK, hiện đúng doanh thu và đơn hàng", "Đạt")
    ]

    for r_idx, row in enumerate(test_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = table3.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 4):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if c_idx == 4:
                    cell.paragraphs[0].runs[0].bold = True

    for row in table3.rows:
        for c_idx, w in enumerate(col_w3):
            row.cells[c_idx].width = w

    p("", space_after=8)

    # CHƯƠNG 5
    h1("5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    p("5.1. Kết luận")
    p("Sau thời gian thực hiện đồ án, nhóm đã hoàn thành được các nội dung theo yêu cầu:")
    p("• Xây dựng website bán quần áo chạy ổn định bằng Flask, cấu trúc code rõ ràng theo blueprint.")
    p("• Hoàn thành các tính năng cơ bản: đăng ký/đăng nhập, xem sản phẩm, tìm kiếm, lọc giá, phân trang, giỏ hàng, đặt hàng và trang quản trị admin.")
    p("• Đáp ứng yêu cầu lập trình mạng CLO3: gọi API ngoài lấy dữ liệu JSON, sinh mã VietQR tự động và viết REST API nội bộ.")
    p("• Rèn luyện được kỹ năng lập trình web với Python, làm việc với CSDL quan hệ SQLAlchemy, thiết kế form và làm việc nhóm bằng Git/GitHub.")
    
    p("5.2. Hạn chế và hướng phát triển")
    p("• Hạn chế: Việc xác nhận đơn hàng sau khi quét mã VietQR hiện tại vẫn cần admin kiểm tra và bấm đổi trạng thái sang 'Đã thanh toán'.")
    p("• Hướng phát triển: Trong tương lai có thể tích hợp thêm Webhook ngân hàng để tự động xác nhận đơn hàng ngay khi tiền về tài khoản; bổ sung tính năng đánh giá sản phẩm sau khi mua.")

    # TÀI LIỆU THAM KHẢO
    h1("TÀI LIỆU THAM KHẢO")
    p("[1] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. O'Reilly Media, 2018.")
    p("[2] Pallets Projects, \"Flask Documentation (v3.1.x),\" https://flask.palletsprojects.com.")
    p("[3] SQLAlchemy Authors, \"SQLAlchemy Documentation,\" https://docs.sqlalchemy.org.")
    p("[4] VietQR, \"VietQR Open API Documentation,\" https://api.vietqr.io.")
    p("[5] Bootstrap Team, \"Bootstrap 5 Documentation,\" https://getbootstrap.com.")

    # PHỤ LỤC
    h1("PHỤ LỤC")
    p("Phụ lục A. Mã nguồn và hướng dẫn chạy chương trình", bold=True)
    p("• Link GitHub của nhóm: https://github.com/toolnayngonphet/Website-Ban-Quan-Ao-Python")
    p("• Hướng dẫn chạy:")
    p("  1. Clone code: git clone https://github.com/toolnayngonphet/Website-Ban-Quan-Ao-Python.git")
    p("  2. Tạo venv: python -m venv venv và kích hoạt môi trường ảo.")
    p("  3. Cài thư viện: pip install -r requirements.txt")
    p("  4. Nạp CSDL mẫu: python seed_data.py")
    p("  5. Chạy server: python run.py (mở trình duyệt http://127.0.0.1:5000)")
    p("• Tài khoản thử nghiệm cho giảng viên:")
    p("  - Admin: username: admin | mật khẩu: admin123")
    p("  - Khách hàng: username: khachhang | mật khẩu: 123456")

    p("Phụ lục B. Dữ liệu mẫu (Database Seed)", bold=True)
    p("File seed_data.py có sẵn 6 danh mục và 13 sản phẩm thời trang mẫu kèm ảnh và giá để giảng viên kiểm tra nhanh.")

    output_file = "Bao_Cao_DoAn_LapTrinhPythonNangCao_HoanChinh.docx"
    doc.save(output_file)
    print(f"Báo cáo đơn giản hoàn thành và lưu tại: {output_file}")

if __name__ == '__main__':
    create_simple_report()
