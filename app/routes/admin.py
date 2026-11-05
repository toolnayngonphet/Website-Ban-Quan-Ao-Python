import os
import uuid
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.forms.product_forms import ProductForm, CategoryForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập vào khu vực quản trị viên!', 'danger')
        return redirect(url_for('main.index'))

def save_product_image(form_image):
    """Xử lý và lưu ảnh sản phẩm bằng Pillow: resize chuẩn 600x600"""
    random_hex = uuid.uuid4().hex[:12]
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext.lower()
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    # Đảm bảo thư mục tồn tại
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Sử dụng Pillow để mở và tối ưu kích thước ảnh
    output_size = (600, 600)
    img = Image.open(form_image)
    
    # Convert RGBA sang RGB nếu là file png/webp có kênh alpha
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
        
    img.thumbnail(output_size)
    img.save(picture_path, quality=88, optimize=True)

    return picture_fn

@admin_bp.route('/')
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    completed_orders = Order.query.filter_by(order_status='completed').all()
    total_revenue = sum(order.total_amount for order in completed_orders)
    
    # Đơn hàng mới nhất
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    # Sản phẩm sắp hết hàng (tồn kho < 10)
    low_stock_products = Product.query.filter(Product.stock < 10).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           recent_orders=recent_orders,
                           low_stock_products=low_stock_products)

# ==================== QUẢN LÝ SẢN PHẨM ====================
@admin_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str).strip()
    category_id = request.args.get('category_id', type=int)

    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category_id:
        query = query.filter_by(category_id=category_id)

    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=current_app.config.get('ADMIN_ITEMS_PER_PAGE', 10), error_out=False
    )
    categories = Category.query.all()

    return render_template('admin/products.html',
                           products=pagination.items,
                           pagination=pagination,
                           categories=categories,
                           search=search,
                           category_id=category_id)

@admin_bp.route('/products/new', methods=['GET', 'POST'])
def product_new():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        # Tạo slug từ tên sản phẩm
        import re
        slug_base = re.sub(r'[^a-zA-Z0-9\s-]', '', form.name.data.lower()).replace(' ', '-')
        slug = f"{slug_base}-{uuid.uuid4().hex[:6]}"

        image_filename = 'default_product.jpg'
        if form.image.data:
            image_filename = save_product_image(form.image.data)

        product = Product(
            name=form.name.data.strip(),
            slug=slug,
            category_id=form.category_id.data,
            price=form.price.data,
            promotional_price=form.promotional_price.data or None,
            stock=form.stock.data,
            sizes=form.sizes.data.strip(),
            colors=form.colors.data.strip(),
            description=form.description.data,
            is_featured=form.is_featured.data,
            image_url=image_filename
        )
        db.session.add(product)
        db.session.commit()
        flash('Đã thêm sản phẩm mới thành công!', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title='Thêm sản phẩm mới')

@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def product_edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product.name = form.name.data.strip()
        product.category_id = form.category_id.data
        product.price = form.price.data
        product.promotional_price = form.promotional_price.data or None
        product.stock = form.stock.data
        product.sizes = form.sizes.data.strip()
        product.colors = form.colors.data.strip()
        product.description = form.description.data
        product.is_featured = form.is_featured.data

        if form.image.data:
            product.image_url = save_product_image(form.image.data)

        db.session.commit()
        flash('Cập nhật thông tin sản phẩm thành công!', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, title='Chỉnh sửa sản phẩm')

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
def product_delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Đã xóa sản phẩm "{product.name}".', 'info')
    return redirect(url_for('admin.products'))

# ==================== QUẢN LÝ DANH MỤC ====================
@admin_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        import re
        slug_base = re.sub(r'[^a-zA-Z0-9\s-]', '', form.name.data.lower()).replace(' ', '-')
        slug = f"{slug_base}-{uuid.uuid4().hex[:4]}"
        
        category = Category(
            name=form.name.data.strip(),
            slug=slug,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Đã thêm danh mục mới!', 'success')
        return redirect(url_for('admin.categories'))

    all_categories = Category.query.all()
    return render_template('admin/categories.html', form=form, categories=all_categories)

@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
def category_delete(id):
    category = Category.query.get_or_404(id)
    if category.products.count() > 0:
        flash('Không thể xóa danh mục đang có sản phẩm. Hãy xóa hoặc chuyển sản phẩm trước.', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Đã xóa danh mục thành công.', 'info')
    return redirect(url_for('admin.categories'))

# ==================== QUẢN LÝ ĐƠN HÀNG ====================
@admin_bp.route('/orders')
def orders():
    status = request.args.get('status', '')
    query = Order.query
    if status:
        query = query.filter_by(order_status=status)
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders, current_status=status)

@admin_bp.route('/orders/<int:id>')
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:id>/update-status', methods=['POST'])
def order_update_status(id):
    order = Order.query.get_or_404(id)
    order.order_status = request.form.get('order_status', order.order_status)
    order.payment_status = request.form.get('payment_status', order.payment_status)
    db.session.commit()
    flash(f'Đã cập nhật trạng thái đơn hàng #{order.order_code}!', 'success')
    return redirect(url_for('admin.order_detail', id=order.id))
