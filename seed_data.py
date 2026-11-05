import sys
sys.stdout.reconfigure(encoding='utf-8')
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderItem

app = create_app()

def seed():
    with app.app_context():
        # Xóa và tạo mới bảng
        db.drop_all()
        db.create_all()
        print("-> Đã làm mới các bảng trong CSDL SQLite.")

        # 1. Tạo tài khoản Admin & Khách hàng
        admin = User(
            username='admin',
            email='admin@fashionstore.vn',
            full_name='Quản Trị Viên Shop',
            phone='0988777666',
            address='123 Nguyễn Văn Cừ, Quận 5, TP. Hồ Chí Minh',
            role='admin'
        )
        admin.set_password('admin123')

        customer = User(
            username='khachhang',
            email='khachhang@gmail.com',
            full_name='Nguyễn Văn Khách',
            phone='0912345678',
            address='456 Lê Duẩn, Quận 1, TP. Hồ Chí Minh',
            role='customer'
        )
        customer.set_password('123456')

        db.session.add_all([admin, customer])
        db.session.commit()
        print("-> Đã tạo tài khoản: admin / admin123 và khachhang / 123456")

        # 2. Tạo Danh mục
        cat1 = Category(name='Áo Thun & Polo', slug='ao-thun-polo', description='Áo thun cotton co giãn, thoáng mát và polo phong cách lịch lãm.')
        cat2 = Category(name='Áo Sơ Mi', slug='ao-so-mi', description='Sơ mi công sở cao cấp, sơ mi họa tiết đi biển, dạo phố.')
        cat3 = Category(name='Quần Jeans & Kaki', slug='quan-jeans-kaki', description='Quần jeans baggy, slimfit và quần kaki thời thượng.')
        cat4 = Category(name='Áo Khoác & Hoodie', slug='ao-khoac-hoodie', description='Áo khoác bomber, jacket dù kháng nước và áo nỉ hoodie trẻ trung.')
        cat5 = Category(name='Váy & Đầm Nữ', slug='vay-dam-nu', description='Váy hoa nhí, đầm dạ hội và chân váy phong cách Hàn Quốc.')
        cat6 = Category(name='Phụ Kiện Thời Trang', slug='phu-kien', description='Nón lưỡi trai, túi đeo chéo canvas, thắt lưng da bò.')

        db.session.add_all([cat1, cat2, cat3, cat4, cat5, cat6])
        db.session.commit()
        print("-> Đã tạo 6 danh mục sản phẩm.")

        # 3. Tạo Danh sách Sản phẩm mẫu (Hình ảnh thời trang Unsplash chất lượng cao)
        sample_products = [
            # Áo Thun & Polo
            Product(
                name='Áo Thun Cotton Oversize Basic',
                slug='ao-thun-cotton-oversize-basic',
                category_id=cat1.id,
                price=220000,
                promotional_price=179000,
                stock=120,
                sizes='S, M, L, XL',
                colors='Trắng, Đen, Xám chì, Xanh bơ',
                image_url='https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80',
                description='Chất liệu 100% cotton 2 chiều 250gsm dày dặn, thấm hút mồ hôi cực tốt. Thiết kế form rộng che khuyết điểm hiệu quả.',
                is_featured=True
            ),
            Product(
                name='Áo Polo Nam Phối Cổ Dệt Bo',
                slug='ao-polo-nam-phoi-co-det-bo',
                category_id=cat1.id,
                price=290000,
                promotional_price=249000,
                stock=85,
                sizes='M, L, XL, XXL',
                colors='Đen viền trắng, Trắng viền đen, Xanh navy',
                image_url='https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&auto=format&fit=crop&q=80',
                description='Vải cá sấu mắt chim thoáng khí, không xù lông sau khi giặt. Thích hợp đi làm, dự tiệc nhẹ hoặc hẹn hò.',
                is_featured=True
            ),
            Product(
                name='Áo Thun Unisex Graphic In Chữ Nổi',
                slug='ao-thun-unisex-graphic-in-chu-noi',
                category_id=cat1.id,
                price=250000,
                promotional_price=None,
                stock=40,
                sizes='M, L, XL',
                colors='Đen, Kem',
                image_url='https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600&auto=format&fit=crop&q=80',
                description='Họa tiết typo trẻ trung in lụa cao cấp không bong tróc. Phong cách đường phố năng động.',
                is_featured=False
            ),

            # Áo Sơ Mi
            Product(
                name='Áo Sơ Mi Oxford Dài Tay Chống Nhăn',
                slug='ao-so-mi-oxford-dai-tay-chong-nhan',
                category_id=cat2.id,
                price=380000,
                promotional_price=320000,
                stock=60,
                sizes='S, M, L, XL',
                colors='Trắng, Xanh Pastel, Xám nhạt',
                image_url='https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=600&auto=format&fit=crop&q=80',
                description='Chất liệu cotton pha sợi tổng hợp hạn chế nhăn tối đa. Form regular-fit tôn dáng công sở hiện đại.',
                is_featured=True
            ),
            Product(
                name='Áo Sơ Mi Cuban Họa Tiết Vintage',
                slug='ao-so-mi-cuban-hoa-tiet-vintage',
                category_id=cat2.id,
                price=320000,
                promotional_price=275000,
                stock=35,
                sizes='M, L, XL',
                colors='Họa tiết lá nhiệt đới, Họa tiết sóng biển',
                image_url='https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&auto=format&fit=crop&q=80',
                description='Cổ áo bẻ kiểu Cuban cổ điển, vải đũi tơ mềm rủ bay bổng rất mát mẻ cho những chuyến du lịch.',
                is_featured=False
            ),

            # Quần Jeans & Kaki
            Product(
                name='Quần Jeans Baggy Suông Rộng Wash Nhẹ',
                slug='quan-jeans-baggy-suong-rong-wash-nhe',
                category_id=cat3.id,
                price=420000,
                promotional_price=360000,
                stock=55,
                sizes='29, 30, 31, 32, 34',
                colors='Xanh nhạt, Xanh đậm, Đen khói',
                image_url='https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&auto=format&fit=crop&q=80',
                description='Chất denim 12oz bền chắc nhưng mềm mại, wash màu vintage tạo điểm nhấn phong cách streetwear.',
                is_featured=True
            ),
            Product(
                name='Quần Kaki Chino Hàn Quốc Ống Suông',
                slug='quan-kaki-chino-han-quoc-ong-suong',
                category_id=cat3.id,
                price=350000,
                promotional_price=299000,
                stock=70,
                sizes='29, 30, 31, 32',
                colors='Be sữa, Đen, Xanh Rêu',
                image_url='https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600&auto=format&fit=crop&q=80',
                description='Chất kaki co giãn nhẹ, giữ form chuẩn suốt cả ngày hoạt động. Phối hoàn hảo với áo polo hoặc sơ mi.',
                is_featured=False
            ),

            # Áo Khoác & Hoodie
            Product(
                name='Áo Khoác Bomber Varsity Học Đường',
                slug='ao-khoac-bomber-varsity-hoc-duong',
                category_id=cat4.id,
                price=550000,
                promotional_price=469000,
                stock=45,
                sizes='M, L, XL',
                colors='Xanh Navy tay trắng, Đen tay kem',
                image_url='https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&auto=format&fit=crop&q=80',
                description='Thân áo dạ lót dù trần bông ấm áp, tay da PU cao cấp không nổ da. Cúc bấm kim loại chắc chắn.',
                is_featured=True
            ),
            Product(
                name='Áo Hoodie Nỉ Bông Chân Cua Form Rộng',
                slug='ao-hoodie-ni-bong-chan-cua-form-rong',
                category_id=cat4.id,
                price=390000,
                promotional_price=339000,
                stock=60,
                sizes='S, M, L, XL',
                colors='Xám tiêu, Đen, Nâu socola',
                image_url='https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&auto=format&fit=crop&q=80',
                description='Mũ trùm 2 lớp đứng form, túi kangaroo tiện lợi trước bụng. Giữ ấm cực tốt trong những ngày se lạnh.',
                is_featured=True
            ),

            # Váy & Đầm Nữ
            Product(
                name='Đầm Xòe Hoa Nhí Vintage Cổ Vuông',
                slug='dam-xoe-hoa-nhi-vintage-co-vuong',
                category_id=cat5.id,
                price=450000,
                promotional_price=385000,
                stock=30,
                sizes='S, M, L',
                colors='Vàng hoa cúc, Xanh hoa pastel',
                image_url='https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&auto=format&fit=crop&q=80',
                description='Chất voan tơ hàn 2 lớp nhẹ tênh, chiết eo nhẹ tôn dáng vòng hai thon gọn và thanh lịch.',
                is_featured=True
            ),
            Product(
                name='Chân Váy Xếp Ly Tennis Năng Động',
                slug='chan-vay-xep-ly-tennis-nang-dong',
                category_id=cat5.id,
                price=260000,
                promotional_price=199000,
                stock=80,
                sizes='XS, S, M, L',
                colors='Trắng tinh khôi, Đen cá tính',
                image_url='https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600&auto=format&fit=crop&q=80',
                description='Có quần bảo hộ bên trong tiện lợi, ly ép nhiệt công nghệ cao không bị mất nếp sau khi giặt.',
                is_featured=False
            ),

            # Phụ Kiện
            Product(
                name='Nón Lưỡi Trai Nón Kết Thêu Logo',
                slug='non-luoi-trai-theu-logo',
                category_id=cat6.id,
                price=150000,
                promotional_price=119000,
                stock=90,
                sizes='Freesize',
                colors='Đen, Trắng, Be',
                image_url='https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600&auto=format&fit=crop&q=80',
                description='Chất vải kaki wash đứng form, khóa gài kim loại điều chỉnh độ rộng thoải mái phía sau.',
                is_featured=False
            ),
            Product(
                name='Túi Đeo Chéo Canvas Phong Cách Retro',
                slug='tui-deo-cheo-canvas-phong-cach-retro',
                category_id=cat6.id,
                price=210000,
                promotional_price=165000,
                stock=40,
                sizes='Freesize',
                colors='Đen, Trắng ngà, Xanh rêu',
                image_url='https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&auto=format&fit=crop&q=80',
                description='Vải bố canvas siêu bền, đựng vừa iPad, sổ tay, ví tiền và điện thoại gọn gàng.',
                is_featured=False
            )
        ]

        db.session.add_all(sample_products)
        db.session.commit()
        print(f"-> Đã tạo {len(sample_products)} sản phẩm thời trang mẫu!")

        # 4. Tạo một đơn hàng demo
        demo_order = Order(
            order_code='DH20261105-DEMO',
            user_id=customer.id,
            customer_name='Nguyễn Văn Khách',
            customer_email='khachhang@gmail.com',
            customer_phone='0912345678',
            shipping_address='456 Lê Duẩn, Quận 1, TP. Hồ Chí Minh',
            note='Giao giờ hành chính',
            total_amount=539000,
            payment_method='VIETQR',
            payment_status='paid',
            order_status='completed'
        )
        db.session.add(demo_order)
        db.session.flush()

        item1 = OrderItem(
            order_id=demo_order.id,
            product_id=sample_products[0].id,
            product_name=sample_products[0].name,
            price=179000,
            quantity=1,
            size='L',
            color='Trắng',
            subtotal=179000
        )
        item2 = OrderItem(
            order_id=demo_order.id,
            product_id=sample_products[5].id,
            product_name=sample_products[5].name,
            price=360000,
            quantity=1,
            size='31',
            color='Xanh nhạt',
            subtotal=360000
        )
        db.session.add_all([item1, item2])
        db.session.commit()
        print("-> Đã tạo 1 đơn hàng mẫu thành công.")

if __name__ == '__main__':
    seed()
    print("\n=== HOÀN TẤT TẠO DỮ LIỆU CƠ SỞ DỮ LIỆU MẪU! ===")
