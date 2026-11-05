import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import current_user
from app.extensions import db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.forms.checkout_forms import CheckoutForm
from app.services.vietqr_service import VietQRService
from app.services.mail_service import MailService

cart_bp = Blueprint('cart', __name__)

def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def calculate_cart_total(cart):
    total = 0.0
    total_qty = 0
    for key, item in cart.items():
        total += item['price'] * item['quantity']
        total_qty += item['quantity']
    return total, total_qty

@cart_bp.route('/cart')
def view_cart():
    cart = get_cart()
    total_amount, total_qty = calculate_cart_total(cart)
    return render_template('cart/cart.html', cart=cart, total_amount=total_amount, total_qty=total_qty)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size', product.size_list[0] if product.size_list else 'Freesize')
    color = request.form.get('color', product.color_list[0] if product.color_list else 'Tiêu chuẩn')

    if quantity <= 0:
        flash('Số lượng mua phải lớn hơn 0.', 'warning')
        return redirect(request.referrer or url_for('main.index'))

    cart = get_cart()
    item_key = f"{product.id}_{size}_{color}"

    if item_key in cart:
        cart[item_key]['quantity'] += quantity
    else:
        cart[item_key] = {
            'product_id': product.id,
            'name': product.name,
            'slug': product.slug,
            'price': product.current_price,
            'image': product.image_url,
            'size': size,
            'color': color,
            'quantity': quantity
        }

    session.modified = True
    flash(f'Đã thêm "{product.name} ({size}, {color})" vào giỏ hàng!', 'success')
    return redirect(request.referrer or url_for('cart.view_cart'))

@cart_bp.route('/cart/update', methods=['POST'])
def update_cart():
    cart = get_cart()
    item_key = request.form.get('item_key')
    action = request.form.get('action')

    if item_key in cart:
        if action == 'increase':
            cart[item_key]['quantity'] += 1
        elif action == 'decrease':
            cart[item_key]['quantity'] -= 1
            if cart[item_key]['quantity'] <= 0:
                del cart[item_key]
        elif action == 'set':
            qty = int(request.form.get('quantity', 1))
            if qty > 0:
                cart[item_key]['quantity'] = qty
            else:
                del cart[item_key]
        session.modified = True

    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<item_key>', methods=['POST', 'GET'])
def remove_from_cart(item_key):
    cart = get_cart()
    if item_key in cart:
        item_name = cart[item_key]['name']
        del cart[item_key]
        session.modified = True
        flash(f'Đã xóa sản phẩm khỏi giỏ hàng.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/clear')
def clear_cart():
    session['cart'] = {}
    session.modified = True
    flash('Đã làm trống giỏ hàng.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    if not cart:
        flash('Giỏ hàng của bạn đang trống. Vui lòng chọn sản phẩm trước khi thanh toán.', 'warning')
        return redirect(url_for('main.shop'))

    total_amount, total_qty = calculate_cart_total(cart)
    form = CheckoutForm()

    # Tự động điền thông tin nếu khách hàng đã đăng nhập
    if request.method == 'GET' and current_user.is_authenticated:
        form.customer_name.data = current_user.full_name or current_user.username
        form.customer_email.data = current_user.email
        form.customer_phone.data = current_user.phone or ''
        form.shipping_address.data = current_user.address or ''

    if form.validate_on_submit():
        order_code = f"DH{datetime.now().strftime('%Y%m%d%H%M')}-{str(uuid.uuid4())[:4].upper()}"

        new_order = Order(
            order_code=order_code,
            user_id=current_user.id if current_user.is_authenticated else None,
            customer_name=form.customer_name.data.strip(),
            customer_email=form.customer_email.data.strip().lower(),
            customer_phone=form.customer_phone.data.strip(),
            shipping_address=form.shipping_address.data.strip(),
            note=form.note.data.strip() if form.note.data else None,
            total_amount=total_amount,
            payment_method=form.payment_method.data,
            payment_status='pending',
            order_status='pending'
        )
        db.session.add(new_order)
        db.session.flush()

        # Tạo các chi tiết đơn hàng (OrderItem) & cập nhật tồn kho
        for key, item in cart.items():
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product_id'],
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                size=item['size'],
                color=item['color'],
                subtotal=item['price'] * item['quantity']
            )
            db.session.add(order_item)

            prod = Product.query.get(item['product_id'])
            if prod:
                prod.stock = max(0, prod.stock - item['quantity'])

        db.session.commit()

        # Gửi email xác nhận đơn hàng qua Flask-Mail
        MailService.send_order_confirmation(new_order)

        # Xóa giỏ hàng sau khi đặt thành công
        session['cart'] = {}
        session.modified = True

        flash('Đặt hàng thành công! Đơn hàng của bạn đã được ghi nhận.', 'success')
        return redirect(url_for('cart.order_success', order_code=order_code))

    return render_template('cart/checkout.html', form=form, cart=cart, total_amount=total_amount, total_qty=total_qty)

@cart_bp.route('/order/success/<order_code>')
def order_success(order_code):
    order = Order.query.filter_by(order_code=order_code).first_or_404()
    
    qr_data = None
    banks = []
    if order.payment_method == 'VIETQR':
        # Sinh dữ liệu mã QR VietQR (CLO3)
        qr_data = VietQRService.generate_qr_url(order.order_code, order.total_amount)
        # Gọi API lấy danh sách ngân hàng để hiển thị tham khảo
        banks = VietQRService.get_supported_banks()[:6]

    return render_template('cart/order_success.html', order=order, qr_data=qr_data, banks=banks)
