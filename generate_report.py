import sys
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()
    
    # Thiết lập lề trang chuẩn A4 (Top=2cm, Bottom=2cm, Left=3cm, Right=2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.79)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Style mặc định: Times New Roman, 13pt, 1.5 line spacing
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=13, space_after=6, space_before=0, color=RGBColor(0, 0, 0)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.3
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 51, 102)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.right_indent = Inches(0.2)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(40, 40, 40)
        # Background box
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="18" w:space="8" w:color="003366"/></w:pBdr>')
        pPr.append(pBdr)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F6F8"/>')
        pPr.append(shd)
        return p

    # ==================== TRANG BÌA ====================
    add_p("TRƯỜNG ĐẠI HỌC VĂN LANG", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=24)
    
    add_p("----------***----------", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    add_p("BÁO CÁO ĐỒ ÁN MÔN HỌC", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, space_after=4, color=RGBColor(0, 51, 102))
    add_p("LẬP TRÌNH PYTHON NÂNG CAO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=18, space_after=4, color=RGBColor(180, 0, 0))
    add_p("Mã học phần: 71ITSE31003 – Nhóm lớp: 253_71ITSE31003_01", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=36)

    add_p("ĐỀ TÀI: XÂY DỰNG WEBSITE BÁN QUẦN ÁO THỜI TRANG (FASHION STORE) TÍCH HỢP THANH TOÁN TỰ ĐỘNG VIETQR VÀ REST API", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=36, color=RGBColor(0, 51, 102))

    add_p("Giảng viên hướng dẫn: ThS. Nguyễn Thị Mỹ Linh", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, size=13, space_after=6)
    add_p("Nhóm thực hiện: Nhóm 03 Sinh viên", bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, size=13, space_after=8)

    # Bảng thành viên nhóm
    table0 = doc.add_table(rows=4, cols=4)
    table0.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers0 = ["STT", "MSSV", "Họ và tên", "Nhiệm vụ chính"]
    col_widths0 = [Inches(0.6), Inches(1.3), Inches(2.0), Inches(2.6)]

    for i, h in enumerate(headers0):
        cell = table0.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E2E8F0")

    members_data = [
        ("1", "[Điền MSSV 1]", "[Điền Họ tên SV 1]", "Nhóm trưởng: Kiến trúc Large App, Models CSDL, Quản trị Admin CRUD, upload tối ưu ảnh Pillow (35%)"),
        ("2", "[Điền MSSV 2]", "[Điền Họ tên SV 2]", "Giao diện Jinja2 kế thừa, Bootstrap 5 UI/UX, Web Forms Flask-WTF, tìm kiếm & phân trang (33%)"),
        ("3", "[Điền MSSV 3]", "[Điền Họ tên SV 3]", "Giỏ hàng Cart session, Checkout, lập trình mạng API VietQR (CLO3), REST API JSON, Flask-Mail (32%)")
    ]

    for r_idx, row_data in enumerate(members_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = table0.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 1):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row in table0.rows:
        for c_idx, w in enumerate(col_widths0):
            row.cells[c_idx].width = w
            set_cell_margins(row.cells[c_idx], 80, 80, 100, 100)

    add_p("", space_after=36)
    add_p("TP. Hồ Chí Minh, tháng 11 năm 2026", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)

    doc.add_page_break()

    # ==================== NHẬN XÉT CỦA GIẢNG VIÊN & RUBRIC ====================
    add_p("NHẬN XÉT VÀ ĐÁNH GIÁ CỦA GIẢNG VIÊN", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=12)
    add_p("." * 110, space_after=6)
    add_p("." * 110, space_after=6)
    add_p("." * 110, space_after=6)
    add_p("." * 110, space_after=14)

    add_p("Bảng đánh giá theo Rubric của học phần", bold=True, size=13, space_after=8)

    table1 = doc.add_table(rows=7, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers1 = ["CLO", "Nội dung đánh giá", "Trọng số", "Điểm"]
    col_widths1 = [Inches(1.0), Inches(3.8), Inches(1.0), Inches(0.8)]

    for i, h in enumerate(headers1):
        cell = table1.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E2E8F0")

    rubric_data = [
        ("CLO2", "Thiết kế và xây dựng ứng dụng web Flask: template, form, database, email", "50%", ""),
        ("CLO3", "Lập trình mạng: urllib, API key, JSON/XML, lập trình mạng Internet (VietQR & REST API)", "10%", ""),
        ("CLO4", "Sử dụng thành thạo thư viện Python (Flask, flask-wtf, urllib, requests, Pillow, json...)", "20%", ""),
        ("CLO5", "Kỹ năng viết báo cáo, module hóa code, cấu trúc rõ ràng, dễ bảo trì", "10%", ""),
        ("CLO6", "Thái độ nghiêm túc, chủ động trong thực hiện và trình bày đồ án", "10%", ""),
        ("Tổng", "Tổng điểm toàn phần", "100%", "")
    ]

    for r_idx, row_data in enumerate(rubric_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = table1.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 2, 3):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if r_idx == 6:
                cell.paragraphs[0].runs[0].bold = True

    for row in table1.rows:
        for c_idx, w in enumerate(col_widths1):
            row.cells[c_idx].width = w
            set_cell_margins(row.cells[c_idx], 80, 80, 100, 100)

    add_p("", space_after=14)

    # MỤC LỤC
    add_p("MỤC LỤC", bold=True, size=14, space_after=8, color=RGBColor(0, 51, 102))
    add_p("[Lưu ý: Nhấp chuột phải vào đây và chọn Update Field để cập nhật số trang tự động sau khi hoàn thiện]", italic=True, size=11, space_after=12)

    toc_items = [
        ("1. GIỚI THIỆU ĐỀ TÀI", "3"),
        ("  1.1. Mô tả bài toán", "3"),
        ("  1.2. Mục tiêu và phạm vi", "3"),
        ("  1.3. Công nghệ sử dụng", "4"),
        ("  1.4. Phân công công việc trong nhóm", "4"),
        ("2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", "4"),
        ("  2.1. Chức năng của hệ thống", "4"),
        ("  2.2. Thiết kế cơ sở dữ liệu", "5"),
        ("  2.3. Thiết kế giao diện", "6"),
        ("3. XÂY DỰNG ỨNG DỤNG VỚI FLASK", "6"),
        ("  3.1. Môi trường và cấu trúc dự án", "6"),
        ("  3.2. Routes và xử lý nghiệp vụ", "7"),
        ("  3.3. Templates với Jinja2", "7"),
        ("  3.4. Web Forms với Flask-WTF", "8"),
        ("  3.5. Cơ sở dữ liệu với Flask-SQLAlchemy", "8"),
        ("  3.6. Gửi email với Flask-Mail", "8"),
        ("  3.7. Lập trình mạng và tích hợp API (CLO3)", "9"),
        ("  3.8. Chức năng mở rộng của nhóm", "9"),
        ("4. KẾT QUẢ VÀ KIỂM THỬ", "9"),
        ("  4.1. Kết quả giao diện", "9"),
        ("  4.2. Kiểm thử chức năng", "10"),
        ("5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "10"),
        ("TÀI LIỆU THAM KHẢO", "11"),
        ("PHỤ LỤC", "11")
    ]
    for title, pg in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(title)
        p.add_run(" " + "." * (80 - len(title) * 2) + " ").font.color.rgb = RGBColor(160, 160, 160)
        p.add_run(pg).bold = True

    doc.add_page_break()

    # ==================== NỘI DUNG CHÍNH ====================

    # CHƯƠNG 1
    add_h1("1. GIỚI THIỆU ĐỀ TÀI")
    
    add_h2("1.1. Mô tả bài toán")
    add_p("Trong kỷ nguyên số hiện nay, thương mại điện tử ngành thời trang may mặc phát triển với tốc độ vượt bậc. Khách hàng ngày càng ưu tiên trải nghiệm mua sắm tiện lợi: dễ dàng tìm kiếm mẫu mã, lọc theo mức giá/danh mục, xem chi tiết kích cỡ (size) và màu sắc, cùng quy trình đặt hàng tinh gọn. Đặc biệt, phương thức thanh toán chuyển khoản truyền thống đòi hỏi khách hàng phải sao chép số tài khoản, nhập chính xác số tiền và cú pháp ghi chú, rất dễ dẫn đến sai sót hoặc nhầm lẫn giao dịch. Về phía người quản trị cửa hàng, việc quản lý danh mục, biến động số lượng tồn kho và cập nhật trạng thái đơn hàng một cách thủ công thường tốn nhiều thời gian và dễ thất thoát dữ liệu.")
    add_p("Để giải quyết bài toán thực tế đó, nhóm thực hiện đề tài xây dựng Website bán quần áo thời trang (Fashion Store) trên nền tảng Flask Framework. Ứng dụng cung cấp đầy đủ các tính năng duyệt hàng, giỏ hàng, đặt hàng, quản trị kho hàng, đồng thời tích hợp lập trình mạng tự động sinh mã VietQR chuẩn ngân hàng và xây dựng hệ thống REST API phục vụ kết nối dữ liệu.")

    add_h2("1.2. Mục tiêu và phạm vi")
    add_p("Mục tiêu của đồ án bao gồm:")
    add_p("• Xây dựng hoàn chỉnh ứng dụng web theo kiến trúc Large Application Structure với đầy đủ chức năng bắt buộc: xác thực phân quyền tài khoản (Khách/Thành viên/Quản trị), CRUD sản phẩm và danh mục, tìm kiếm theo tên, lọc đa tiêu chí và phân trang (Pagination).")
    add_p("• Tích hợp lập trình mạng Internet theo chuẩn đầu ra CLO3: sử dụng thư viện requests/urllib gọi API VietQR đọc dữ liệu JSON danh sách ngân hàng Việt Nam, đồng thời tự động sinh mã QR thanh toán tức thì theo từng đơn hàng cụ thể; xây dựng REST API nội bộ trả về JSON.")
    add_p("• Tích hợp dịch vụ gửi email tự động với Flask-Mail gửi hóa đơn xác nhận đơn hàng; ứng dụng thư viện Pillow để tối ưu hóa và nén ảnh sản phẩm upload.")
    add_p("Phạm vi đề tài: Giới hạn nghiệp vụ ở quy trình mua bán trực tuyến các sản phẩm thời trang (áo thun, sơ mi, quần jean, áo khoác, váy đầm, phụ kiện) với 2 vai trò chính: Khách hàng mua sắm và Quản trị viên cửa hàng.")

    add_h2("1.3. Công nghệ sử dụng")
    add_p("Dự án được xây dựng trên nền tảng các công nghệ và thư viện chuẩn mực:")
    add_p("• Ngôn ngữ & Framework: Python 3.11, Flask 3.1.0.")
    add_p("• Giao diện (Frontend): Template engine Jinja2, Framework Bootstrap 5.3.3, Bootstrap Icons, Font chữ Plus Jakarta Sans.")
    add_p("• Cơ sở dữ liệu: SQLite, thao tác ORM thông qua Flask-SQLAlchemy 3.1.1.")
    add_p("• Quản lý Form & Bảo mật: Flask-WTF 1.2.2, Flask-Login 0.6.3, Werkzeug Security (băm mật khẩu pbkdf2:sha256, chống tấn công CSRF).")
    add_p("• Lập trình mạng & API (CLO3): Thư viện requests 2.32, urllib.parse, json, tích hợp VietQR Open API.")
    add_p("• Xử lý ảnh (CLO4): Thư viện Pillow 11.1 (PIL) tự động nắn kích thước chuẩn 600x600 và tối ưu chất lượng ảnh sản phẩm.")
    add_p("• Dịch vụ Email: Flask-Mail 0.10.0 kết hợp luồng xử lý bất đồng bộ (threading.Thread).")
    add_p("• Triển khai & Quản lý: Git, GitHub repository, Web Server Gunicorn 23.0.0, Cloud Hosting Render.")

    add_h2("1.4. Phân công công việc trong nhóm")
    add_p("Nhóm gồm 3 thành viên, khối lượng công việc được phân bổ cụ thể theo từng module nghiệp vụ:")
    add_p("• Thành viên 1 (Nhóm trưởng - 35%): Thiết kế kiến trúc dự án (Application Factory, config.py); mô hình hóa CSDL SQLAlchemy; xây dựng phân hệ Admin Blueprint (CRUD sản phẩm, danh mục); tích hợp module xử lý upload và resize ảnh vuông chuẩn bằng Pillow.")
    add_p("• Thành viên 2 (33%): Xây dựng hệ thống giao diện người dùng Jinja2 kế thừa base.html; thiết kế responsive UI/UX với Bootstrap 5; xây dựng các lớp Flask-WTF Forms (đăng nhập, đăng ký, cập nhật hồ sơ, checkout); thực hiện chức năng tìm kiếm, bộ lọc khoảng giá và phân trang.")
    add_p("• Thành viên 3 (32%): Lập trình nghiệp vụ Giỏ hàng (Cart Session) và Checkout; thực hiện phần Lập trình mạng CLO3 (tích hợp API VietQR tự động sinh mã QR thanh toán ngân hàng, tải danh sách ngân hàng qua requests JSON); xây dựng các endpoint REST API nội bộ; cấu hình dịch vụ gửi email hóa đơn Flask-Mail.")

    # CHƯƠNG 2
    add_h1("2. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    add_h2("2.1. Chức năng của hệ thống")
    add_p("Hệ thống phân định rõ ràng các nhóm chức năng theo tác nhân (Actor):")
    add_p("1. Khách vãng lai (Guest): Xem danh sách sản phẩm, lọc theo danh mục, khoảng giá, sắp xếp giá; tìm kiếm sản phẩm theo từ khóa; xem chi tiết sản phẩm; chọn size, màu sắc và thêm vào giỏ hàng; đặt hàng nhanh không cần tài khoản; đăng ký tài khoản mới.")
    add_p("2. Khách hàng đã đăng nhập (Customer): Tự động điền thông tin người nhận khi đặt hàng; theo dõi lịch sử và trạng thái các đơn hàng cá nhân; cập nhật thông tin hồ sơ (họ tên, số điện thoại, địa chỉ nhận hàng).")
    add_p("3. Quản trị viên (Admin): Bảng điều khiển (Dashboard) thống kê tổng doanh thu đơn hoàn thành, số lượng đơn, sản phẩm đang bán và cảnh báo sản phẩm sắp hết hàng (<10 chiếc); quản lý CRUD danh mục; quản lý CRUD sản phẩm kèm upload ảnh tối ưu qua Pillow; xem chi tiết và cập nhật trạng thái đơn hàng (Chờ xử lý -> Đã xác nhận -> Đang giao -> Hoàn thành -> Đã hủy) và trạng thái thanh toán.")
    add_p("4. Hệ thống API (CLO3): Cung cấp các endpoint JSON phục vụ truy xuất dữ liệu sản phẩm, danh mục, tra cứu đơn hàng và gọi API lấy danh sách ngân hàng ngoài.")

    add_h2("2.2. Thiết kế cơ sở dữ liệu")
    add_p("Cơ sở dữ liệu SQLite được thiết kế theo chuẩn quan hệ gồm 5 bảng (Model) chính:")
    add_p("Bảng 2.1. Mô tả các bảng dữ liệu (model SQLAlchemy)", bold=True, size=12)

    table2 = doc.add_table(rows=6, cols=4)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers2 = ["Model/Bảng", "Cột chính", "Khóa", "Quan hệ / Ghi chú"]
    col_widths2 = [Inches(1.2), Inches(2.7), Inches(1.0), Inches(1.7)]

    for i, h in enumerate(headers2):
        cell = table2.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E2E8F0")

    models_data = [
        ("User", "id, username, email, password_hash, full_name, phone, address, role, created_at", "id (PK)", "Quan hệ 1-N với Order. Lưu vai trò 'admin' hoặc 'customer'."),
        ("Category", "id, name, slug, description", "id (PK)", "Quan hệ 1-N với Product. Phân loại trang phục (áo thun, sơ mi, quần...)."),
        ("Product", "id, name, slug, price, promotional_price, stock, image_url, sizes, colors, description, is_featured, created_at, category_id", "id (PK), category_id (FK)", "Quan hệ N-1 với Category, 1-N với OrderItem. Chứa thông tin size, màu và giá KM."),
        ("Order", "id, order_code, user_id, customer_name, customer_email, customer_phone, shipping_address, note, total_amount, payment_method, payment_status, order_status, created_at", "id (PK), user_id (FK)", "Quan hệ N-1 với User (nullable), 1-N với OrderItem. Phương thức 'COD' hoặc 'VIETQR'."),
        ("OrderItem", "id, order_id, product_id, product_name, price, quantity, size, color, subtotal", "id (PK), order_id (FK), product_id (FK)", "Quan hệ N-1 với Order, N-1 với Product. Lưu trữ chi tiết từng món đồ đã mua.")
    ]

    for r_idx, row_data in enumerate(models_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = table2.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 2):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row in table2.rows:
        for c_idx, w in enumerate(col_widths2):
            row.cells[c_idx].width = w
            set_cell_margins(row.cells[c_idx], 80, 80, 100, 100)

    add_p("", space_after=8)

    add_h2("2.3. Thiết kế giao diện")
    add_p("Hệ thống giao diện được thiết kế theo cấu trúc kế thừa phân cấp chặt chẽ trong Jinja2:")
    add_p("• Template gốc base.html: Chứa TopBar ưu đãi, Navigation Bar (Logo thương hiệu, thanh tìm kiếm tức thì, dropdown danh mục, biểu tượng giỏ hàng kèm huy hiệu số lượng động, menu đăng nhập/tài khoản), vùng hiển thị Flash Message tự động ẩn sau 5 giây, khối {% block content %} và Footer.")
    add_p("• Luồng người dùng chính: Trang chủ (main/index.html) -> Cửa hàng (main/shop.html) lọc sản phẩm và phân trang -> Chi tiết sản phẩm (main/product_detail.html) chọn size, màu, số lượng -> Giỏ hàng (cart/cart.html) cập nhật số lượng -> Đặt hàng (cart/checkout.html) -> Hoàn tất thanh toán (cart/order_success.html) hiển thị mã VietQR động.")
    add_p("• Luồng quản trị: Bảng điều khiển (admin/dashboard.html) -> Quản lý sản phẩm (admin/products.html) -> Thêm/Sửa (admin/product_form.html) -> Quản lý danh mục (admin/categories.html) -> Quản lý và xử lý đơn hàng (admin/orders.html, admin/order_detail.html).")

    # CHƯƠNG 3
    add_h1("3. XÂY DỰNG ỨNG DỤNG VỚI FLASK")

    add_h2("3.1. Môi trường và cấu trúc dự án")
    add_p("Dự án áp dụng mô hình chuẩn Large Application Structure, chia tách trách nhiệm thành các package độc lập giúp dễ bảo trì và mở rộng:")
    
    add_code_block("""DACK/
├── app/
│   ├── __init__.py           # Application Factory create_app(), filter VND, inject data
│   ├── extensions.py         # Khởi tạo db, login_manager, mail, csrf
│   ├── models/               # SQLAlchemy Models: User, Category, Product, Order, OrderItem
│   ├── forms/                # Flask-WTF Forms: LoginForm, RegisterForm, ProductForm, CheckoutForm
│   ├── services/             # VietQRService (CLO3 API), MailService (Flask-Mail)
│   ├── routes/               # Blueprints: main, auth, cart, admin, api
│   ├── templates/            # Jinja2 templates (base.html, main/, auth/, cart/, admin/, email/)
│   └── static/               # File tĩnh: css/, js/, uploads/products/
├── instance/                 # Thư mục chứa CSDL SQLite (clothing_shop.db)
├── config.py                 # File cấu hình tập trung (Secret Key, DB URI, Mail, VietQR)
├── seed_data.py              # Script nạp dữ liệu khởi tạo 13+ sản phẩm và tài khoản mẫu
├── test_app.py               # Kịch bản kiểm thử tự động toàn bộ 10 chức năng
└── run.py                    # Điểm khởi chạy ứng dụng chính""")

    add_h2("3.2. Routes và xử lý nghiệp vụ")
    add_p("Ứng dụng phân chia 5 Blueprints rõ ràng:")
    add_p("• main_bp: Điều hướng trang chủ, danh sách cửa hàng kèm bộ lọc, chi tiết sản phẩm, giới thiệu.")
    add_p("• auth_bp: Xử lý đăng ký, đăng nhập với login_user(), ghi nhớ phiên, đăng xuất và hồ sơ cá nhân.")
    add_p("• cart_bp: Quản lý giỏ hàng session, tính toán tổng tiền, xử lý đơn hàng checkout và hiển thị trang thanh toán.")
    add_p("• admin_bp: Yêu cầu phân quyền Admin thông qua before_request kiểm tra current_user.is_admin, cung cấp các thao tác CRUD danh mục, sản phẩm và duyệt đơn.")
    add_p("• api_bp: Cung cấp các endpoint REST API trả về dữ liệu JSON, được miễn trừ kiểm tra CSRF token (csrf.exempt) để cho phép client bên ngoài gọi truy vấn.")

    add_h2("3.3. Templates với Jinja2")
    add_p("Ứng dụng tận dụng triệt để sức mạnh của Jinja2:")
    add_p("• Kế thừa giao diện: Tất cả các view con đều kế thừa {% extends 'base.html' %} và ghi đè {% block content %}.")
    add_p("• Bộ lọc tùy biến (Custom Filter): Định nghĩa bộ lọc currency trong app/__init__.py để tự động format số tiền sang định dạng tiền Việt Nam (ví dụ: 250000 -> 250.000 đ).")
    add_p("• Context Processor: Sử dụng @app.context_processor để truyền dữ liệu giỏ hàng (cart_count) và danh mục (header_categories) vào tất cả các template mà không cần truyền thủ công ở từng route.")
    add_p("• Phân trang: Sử dụng thuộc tính pagination.iter_pages(), pagination.has_prev, pagination.has_next để render thanh phân trang linh hoạt.")

    add_h2("3.4. Web Forms với Flask-WTF")
    add_p("Toàn bộ các biểu mẫu nhập liệu đều được xây dựng qua Flask-WTF kế thừa FlaskForm, tích hợp bảo vệ CSRF (Cross-Site Request Forgery) và bộ kiểm tra (Validators):")
    add_p("• LoginForm, RegisterForm: Kiểm tra định dạng Email, độ dài chuỗi, xác nhận mật khẩu khớp nhau (EqualTo) và kiểm tra tính duy nhất (Unique) của tên đăng nhập trong CSDL.")
    add_p("• ProductForm: Kiểm tra nhập liệu giá bán, giá khuyến mãi hợp lệ, số lượng tồn kho (NumberRange min=0), lựa chọn danh mục từ SelectField, và xác thực file ảnh upload hợp lệ (FileAllowed: jpg, jpeg, png, webp).")
    add_p("• CheckoutForm: Xác thực thông tin người nhận hàng, số điện thoại hợp lệ và phương thức thanh toán.")

    add_h2("3.5. Cơ sở dữ liệu với Flask-SQLAlchemy")
    add_p("Thao tác dữ liệu được thực hiện thông qua SQLAlchemy ORM:")
    add_p("• Khai báo quan hệ: Quan hệ 1-N giữa Category và Product sử dụng db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan').")
    add_p("• Truy vấn nâng cao: Thực hiện tìm kiếm không phân biệt hoa thường với ilike(), lọc kết hợp nhiều điều kiện (filter), sắp xếp (order_by) và phân trang tối ưu thông qua paginate(page=page, per_page=8).")
    add_p("• Thao tác CRUD: Sử dụng db.session.add(), db.session.commit(), db.session.delete() đảm bảo tính toàn vẹn giao dịch.")

    add_h2("3.6. Gửi email với Flask-Mail")
    add_p("Dịch vụ gửi email được thiết lập qua Flask-Mail kết nối SMTP Server:")
    add_p("• Ngay sau khi khách hàng bấm xác nhận đặt hàng tại /checkout, hệ thống tự động render mẫu email HTML (email/order_confirmation.html) chứa bảng kê chi tiết các món đồ, số lượng, đơn giá và tổng thanh toán.")
    add_p("• Để đảm bảo trải nghiệm người dùng không bị gián đoạn hay chờ đợi lâu do độ trễ mạng khi gửi thư, quá trình gửi mail được tách sang một tiến trình chạy ngầm độc lập sử dụng module threading.Thread.")

    add_h2("3.7. Lập trình mạng và tích hợp API (CLO3)")
    add_p("Đây là nội dung trọng tâm thể hiện chuẩn đầu ra CLO3 về lập trình mạng Internet và xử lý dữ liệu JSON:")
    add_p("1. Gọi API bên ngoài bằng thư viện requests:")
    add_p("Dịch vụ VietQRService thực hiện gửi yêu cầu HTTP GET tới địa chỉ https://api.vietqr.io/v2/banks, giải mã chuỗi phản hồi JSON (response.json()) để trích xuất danh sách tất cả các ngân hàng thương mại tại Việt Nam kèm tên viết tắt, mã BIN và đường dẫn logo ngân hàng. Hệ thống cũng xây dựng cơ chế dự phòng (Fallback) danh sách các ngân hàng lớn (MB, VCB, CTG, TCB, VPB, ACB...) trong trường hợp mất kết nối mạng.")
    add_p("2. Tự động sinh mã thanh toán VietQR động:")
    add_p("Dựa trên mã đơn hàng duy nhất và tổng tiền đơn hàng, dịch vụ sử dụng module urllib.parse để mã hóa tham số truy vấn (amount, addInfo, accountName) và sinh đường dẫn ảnh mã QR chuẩn Quốc gia:")
    add_code_block("https://img.vietqr.io/image/<BANK_ID>-<ACCOUNT_NO>-compact2.png?amount=<TIEN>&addInfo=<MA_DON>&accountName=<TEN>")
    add_p("Khi khách hàng mở ứng dụng Mobile Banking của bất kỳ ngân hàng nào quét mã này, ứng dụng ngân hàng sẽ tự động điền chính xác 100% số tài khoản, số tiền và nội dung chuyển khoản, loại bỏ hoàn toàn sai sót.")
    add_p("3. Xây dựng REST API nội bộ trả về JSON:")
    add_p("Hệ thống cung cấp các endpoint JSON chuẩn RESTful:")
    add_p("• GET /api/v1/products: Trả về danh sách sản phẩm (hỗ trợ tham số lọc category_id, search, limit).")
    add_p("• GET /api/v1/products/<id>: Trả về chi tiết 1 sản phẩm.")
    add_p("• GET /api/v1/categories: Trả về danh sách danh mục và số lượng sản phẩm.")
    add_p("• GET /api/v1/orders/<order_code>: Tra cứu thông tin chi tiết đơn hàng dạng JSON.")
    add_p("• GET /api/v1/banks: Trả về danh sách các ngân hàng hỗ trợ VietQR.")

    add_h2("3.8. Chức năng mở rộng của nhóm")
    add_p("Để tạo điểm nhấn sáng tạo và tối ưu ứng dụng, nhóm đã triển khai thêm các module nâng cao:")
    add_p("• Tối ưu và nén ảnh tự động với Pillow: Trong trang thêm/sửa sản phẩm của Admin, ảnh upload được tự động kiểm tra định dạng, chuyển đổi hệ màu sang RGB, cắt tỉ lệ vuông và nén kích thước 600x600 px với quality=88. Nhờ đó, trang web tải nhanh và hình ảnh sản phẩm luôn đồng nhất, không bị méo mó.")
    add_p("• Quản lý Giỏ hàng linh hoạt trong Session: Lưu trữ sản phẩm theo tổ hợp phân loại riêng biệt (f\"{product_id}_{size}_{color}\"), cho phép khách hàng chọn cùng 1 mẫu áo nhưng khác size hoặc màu sắc.")
    add_p("• Triển khai thực tế trên Cloud Hosting: Mã nguồn được cấu hình với Gunicorn Server và triển khai online 24/7 trên nền tảng Render.com.")

    # CHƯƠNG 4
    add_h1("4. KẾT QUẢ VÀ KIỂM THỬ")

    add_h2("4.1. Kết quả giao diện")
    add_p("Ứng dụng đã hoàn thiện đầy đủ các màn hình giao diện chính và hoạt động ổn định trên cả máy tính và thiết bị di động:")
    add_p("• Hình 4.1: Trang chủ (Hero Banner, Danh mục nổi bật, Sản phẩm bán chạy, Banner giới thiệu tính năng VietQR và cam kết dịch vụ).")
    add_p("• Hình 4.2: Trang Cửa hàng (Sidebar bộ lọc danh mục và khoảng giá, sắp xếp theo giá tăng/giảm, lưới hiển thị sản phẩm và phân trang).")
    add_p("• Hình 4.3: Trang Chi tiết sản phẩm (Ảnh lớn sắc nét, thông tin giá gốc và giá khuyến mãi, bộ chọn kích cỡ Size S/M/L/XL, chọn màu sắc, số lượng, kiểm tra số lượng tồn kho).")
    add_p("• Hình 4.4: Trang Giỏ hàng và Thanh toán (Quản lý tăng/giảm số lượng món đồ, tính tạm tính và phí vận chuyển, form điền địa chỉ giao hàng và tùy chọn thanh toán VietQR / COD).")
    add_p("• Hình 4.5: Trang Xác nhận đặt hàng thành công & Thanh toán VietQR (Hiển thị mã QR động được sinh chuẩn VietQR kèm số tài khoản MB Bank, số tiền và nội dung đơn hàng để khách hàng quét trả tiền ngay trên điện thoại).")
    add_p("• Hình 4.6: Bảng điều khiển Quản trị viên - Admin Dashboard (Thống kê số liệu doanh thu, tổng số đơn, quản lý CRUD kho hàng, duyệt đơn hàng và cập nhật trạng thái thanh toán).")
    add_p("• Hình 4.7: Kết quả truy vấn REST API trả về dữ liệu JSON trên trình duyệt / Postman.")

    add_h2("4.2. Kiểm thử chức năng")
    add_p("Nhóm đã xây dựng bộ kiểm thử tự động (test_app.py) bao quát toàn bộ 10 kịch bản cốt lõi của hệ thống:")
    add_p("Bảng 4.1. Kết quả kiểm thử chức năng", bold=True, size=12)

    table3 = doc.add_table(rows=11, cols=5)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers3 = ["TT", "Chức năng / Kịch bản", "Dữ liệu thử", "Kết quả mong đợi", "Đánh giá"]
    col_widths3 = [Inches(0.5), Inches(1.8), Inches(1.8), Inches(1.8), Inches(0.8)]

    for i, h in enumerate(headers3):
        cell = table3.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E2E8F0")

    test_data = [
        ("1", "Tải Trang chủ", "GET /", "Mã trạng thái 200 OK, hiển thị đầy đủ danh mục và sản phẩm nổi bật", "Đạt"),
        ("2", "Xem Cửa hàng & Danh mục", "GET /shop?category=ao-thun-polo", "Mã trạng thái 200 OK, chỉ lọc các sản phẩm thuộc danh mục Áo thun", "Đạt"),
        ("3", "Tìm kiếm & Sắp xếp giá", "GET /shop?q=áo&sort=price_asc", "Trả về các sản phẩm có chữ 'áo', sắp xếp thứ tự giá tăng dần", "Đạt"),
        ("4", "Xem Chi tiết sản phẩm", "GET /product/ao-thun-cotton-oversize-basic", "Mã trạng thái 200 OK, hiển thị đầy đủ giá, size, màu sắc, nút mua hàng", "Đạt"),
        ("5", "Thêm sản phẩm vào giỏ", "POST /cart/add/1 (size: L, color: Đen, qty: 2)", "Giỏ hàng Session ghi nhận 2 sản phẩm, cập nhật huy hiệu số lượng trên Navbar", "Đạt"),
        ("6", "Đặt hàng & Sinh mã VietQR", "POST /checkout (Tên, SĐT, Địa chỉ, Method: VIETQR)", "Tạo thành công Order và OrderItem trong CSDL, sinh mã VietQR hợp lệ", "Đạt"),
        ("7", "REST API danh sách sản phẩm", "GET /api/v1/products", "Trả về JSON chứa status: 'success', count: 13 và mảng dữ liệu sản phẩm", "Đạt"),
        ("8", "API tra cứu danh sách ngân hàng", "GET /api/v1/banks", "Kết nối Internet thành công, trả về danh sách ngân hàng Việt Nam dạng JSON", "Đạt"),
        ("9", "Đăng nhập người dùng", "POST /login (admin / admin123)", "Đăng nhập thành công, phân quyền Admin truy cập Control Panel", "Đạt"),
        ("10", "Quản trị Admin Dashboard", "GET /admin/", "Mã trạng thái 200 OK, hiển thị số liệu doanh thu, sản phẩm và đơn hàng", "Đạt")
    ]

    for r_idx, row_data in enumerate(test_data, start=1):
        for c_idx, val in enumerate(row_data):
            cell = table3.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].paragraph_format.line_spacing = 1.15
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if c_idx in (0, 4):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if c_idx == 4:
                    cell.paragraphs[0].runs[0].bold = True

    for row in table3.rows:
        for c_idx, w in enumerate(col_widths3):
            row.cells[c_idx].width = w
            set_cell_margins(row.cells[c_idx], 80, 80, 100, 100)

    add_p("", space_after=8)

    # CHƯƠNG 5
    add_h1("5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    add_p("5.1. Kết luận và thành quả đạt được")
    add_p("Sau quá trình nghiên cứu và thực hiện, nhóm đã hoàn thành toàn diện các mục tiêu đề ra:")
    add_p("• Ứng dụng web Flask hoạt động ổn định, mượt mà, cấu trúc module hóa phân tầng rõ ràng (Large Application Structure) tuân thủ tiêu chuẩn lập trình Python chuyên nghiệp.")
    add_p("• Đáp ứng 100% các tiêu chí trong Rubric đánh giá: Xác thực phân quyền tài khoản (CLO2), Quản lý CSDL quan hệ với Flask-SQLAlchemy (CLO2), Thiết kế form chống CSRF với Flask-WTF (CLO2), Gửi email hóa đơn tự động (CLO2), Lập trình mạng tích hợp VietQR API và REST API JSON (CLO3), Sử dụng thành thạo các thư viện Python nâng cao như Pillow, requests, dotenv (CLO4).")
    add_p("• Kỹ năng đạt được: Nắm vững kiến trúc phát triển ứng dụng Web với Python; hiểu sâu về giao thức HTTP, phương thức xác thực phiên người dùng; thành thạo kỹ thuật gọi API và bóc tách dữ liệu JSON; tích lũy kinh nghiệm làm việc nhóm qua Git/GitHub.")
    
    add_p("5.2. Hạn chế và hướng phát triển")
    add_p("• Hạn chế: Cơ chế thanh toán VietQR hiện tại dựa trên mã QR động chuẩn xác thông tin; việc tự động xác nhận đơn hàng khi tiền về tài khoản ngân hàng còn cần tích hợp thêm Webhook biến động số dư (Open Banking API).")
    add_p("• Hướng phát triển trong tương lai:")
    add_p("1. Tích hợp Webhook đồng bộ trạng thái thanh toán theo thời gian thực (Real-time Payment Confirmation).")
    add_p("2. Ứng dụng thuật toán gợi ý sản phẩm thông minh (Recommendation System) dựa trên lịch sử xem hàng và thời tiết thực tế tại vị trí của khách hàng.")
    add_p("3. Mở rộng tính năng đánh giá, bình luận sản phẩm kèm hình ảnh feedback từ khách hàng.")

    # TÀI LIỆU THAM KHẢO
    add_h1("TÀI LIỆU THAM KHẢO")
    add_p("[1] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.")
    add_p("[2] M. Grinberg, \"The Flask Mega-Tutorial,\" blog.miguelgrinberg.com. [Truy cập: 11/2026].")
    add_p("[3] Pallets Projects, \"Flask Documentation (v3.1.x),\" flask.palletsprojects.com. [Truy cập: 11/2026].")
    add_p("[4] SQLAlchemy Authors, \"SQLAlchemy 2.0 Documentation,\" docs.sqlalchemy.org. [Truy cập: 11/2026].")
    add_p("[5] VietQR, \"VietQR Open API Specification & Quicklink Guidelines,\" api.vietqr.io. [Truy cập: 11/2026].")
    add_p("[6] Bootstrap Team, \"Bootstrap 5.3 Documentation,\" getbootstrap.com. [Truy cập: 11/2026].")

    # PHỤ LỤC
    add_h1("PHỤ LỤC")
    add_p("Phụ lục A. Mã nguồn và hướng dẫn chạy chương trình", bold=True)
    add_p("• Đường dẫn kho mã nguồn GitHub: https://github.com/toolnayngonphet/Website-Ban-Quan-Ao-Python")
    add_p("• Các bước chạy ứng dụng từ mã nguồn:")
    add_p("  Bước 1: Clone mã nguồn: git clone https://github.com/toolnayngonphet/Website-Ban-Quan-Ao-Python.git")
    add_p("  Bước 2: Tạo môi trường ảo: python -m venv venv và kích hoạt (.\\venv\\Scripts\\activate)")
    add_p("  Bước 3: Cài đặt thư viện: pip install -r requirements.txt")
    add_p("  Bước 4: Nạp CSDL mẫu: python seed_data.py")
    add_p("  Bước 5: Khởi chạy: python run.py (Truy cập trình duyệt tại http://127.0.0.1:5000)")
    add_p("• Tài khoản thử nghiệm dành cho Giảng viên kiểm tra:")
    add_p("  - Tài khoản Quản trị (Admin): username: admin | mật khẩu: admin123")
    add_p("  - Tài khoản Khách hàng (Customer): username: khachhang | mật khẩu: 123456")

    add_p("Phụ lục B. Dữ liệu mẫu (Database Seed)", bold=True)
    add_p("Toàn bộ dữ liệu mẫu gồm 6 danh mục chính và 13 sản phẩm quần áo thời trang phong phú đã được lập trình sẵn trong file seed_data.py, có thể tái lập CSDL tự động bất kỳ lúc nào chỉ bằng lệnh: python seed_data.py.")

    output_path = "Bao_Cao_DoAn_LapTrinhPythonNangCao_HoanChinh.docx"
    doc.save(output_path)
    print(f"Báo cáo Word đã được tạo thành công tại: {output_path}")

if __name__ == '__main__':
    create_report()
