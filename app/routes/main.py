from flask import Blueprint, render_template, request, current_app
from app.models.product import Product
from app.models.category import Category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    new_products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('main/index.html',
                           featured_products=featured_products,
                           new_products=new_products,
                           categories=categories)

@main_bp.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category', '', type=str)
    search_query = request.args.get('q', '', type=str).strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest', type=str)

    query = Product.query

    selected_category = None
    if category_slug:
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter(Product.category_id == selected_category.id)

    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    per_page = current_app.config.get('ITEMS_PER_PAGE', 8)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    categories = Category.query.all()

    return render_template('main/shop.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           selected_category=selected_category,
                           search_query=search_query,
                           min_price=min_price,
                           max_price=max_price,
                           sort_by=sort_by)

@main_bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    return render_template('main/product_detail.html',
                           product=product,
                           related_products=related_products)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')
