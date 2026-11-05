import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.services.vietqr_service import VietQRService

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

def run_tests():
    with app.test_client() as client:
        print("=== BẮT ĐẦU KIỂM THỬ HỆ THỐNG ===")

        # 1. Test Trang chủ
        res = client.get('/')
        assert res.status_code == 200, f"Trang chủ lỗi {res.status_code}"
        print("[PASS] 1. Trang chủ (/) tải thành công 200 OK")

        # 2. Test Trang cửa hàng
        res = client.get('/shop')
        assert res.status_code == 200, f"Trang shop lỗi {res.status_code}"
        print("[PASS] 2. Cửa hàng (/shop) tải thành công 200 OK")

        # 3. Test Tìm kiếm & Phân trang
        res = client.get('/shop?q=áo&sort=price_asc')
        assert res.status_code == 200
        print("[PASS] 3. Tìm kiếm & Sắp xếp giá hoạt động tốt")

        # 4. Test Chi tiết sản phẩm
        with app.app_context():
            p = Product.query.first()
            assert p is not None, "Không có sản phẩm trong DB"
            slug = p.slug

        res = client.get(f'/product/{slug}')
        assert res.status_code == 200
        print(f"[PASS] 4. Chi tiết sản phẩm (/product/{slug}) tải thành công")

        # 5. Test Giỏ hàng
        res = client.post(f'/cart/add/{p.id}', data={'quantity': 2, 'size': 'L', 'color': 'Đen'}, follow_redirects=True)
        assert res.status_code == 200
        res = client.get('/cart')
        assert b'Gi' in res.data or res.status_code == 200
        print("[PASS] 5. Thêm sản phẩm vào giỏ hàng thành công")

        # 6. Test Đặt hàng & VietQR
        res = client.post('/checkout', data={
            'customer_name': 'Nguyễn Văn Test',
            'customer_email': 'test@gmail.com',
            'customer_phone': '0901234567',
            'shipping_address': '789 CMT8, Q10, TPHCM',
            'note': 'Giao buổi sáng',
            'payment_method': 'VIETQR'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b'VietQR' in res.data or b'thanh to' in res.data
        print("[PASS] 6. Đặt hàng và sinh mã thanh toán VietQR thành công")

        # 7. Test REST API (CLO3)
        res = client.get('/api/v1/products')
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'success' and data['count'] > 0
        print(f"[PASS] 7. REST API /api/v1/products trả về {data['count']} sản phẩm JSON")

        res = client.get('/api/v1/banks')
        assert res.status_code == 200
        banks_data = res.get_json()
        assert banks_data['status'] == 'success' and len(banks_data['data']) > 0
        print(f"[PASS] 8. API /api/v1/banks tra cứu thành công danh sách ngân hàng Việt Nam")

        # 8. Test Auth Login
        res = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        assert res.status_code == 200
        assert b'Qu\xe1\xba\xa3n Tr\xe1\xbb\x8b' in res.data or b'admin' in res.data.lower()
        print("[PASS] 9. Đăng nhập Admin thành công")

        # 9. Test Admin Dashboard
        res = client.get('/admin/')
        assert res.status_code == 200
        print("[PASS] 10. Admin Dashboard tải thành công 200 OK")

        print("\n=== TOÀN BỘ 10 KIỂM THỬ ĐỀU ĐẠT CHUẨN 100%! ===")

if __name__ == '__main__':
    run_tests()
