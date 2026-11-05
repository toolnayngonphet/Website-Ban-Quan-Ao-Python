import os
from flask import Flask, render_template, session
from config import Config
from app.extensions import db, login_manager, mail, csrf
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.cart import cart_bp
from app.routes.admin import admin_bp
from app.routes.api import api_bp
from app.models.category import Category

def format_currency(value):
    """Template filter định dạng tiền Việt Nam: 250000 -> 250.000 đ"""
    try:
        val = int(round(float(value)))
        return f"{val:,.0f}".replace(',', '.') + " đ"
    except (ValueError, TypeError):
        return f"{value} đ"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Đảm bảo thư mục upload và instance tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    # Khởi tạo các extension
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Miễn trừ CSRF cho API Blueprint (CLO3) để gọi từ các client bên ngoài
    csrf.exempt(api_bp)

    # Đăng ký Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Đăng ký custom Jinja filters
    app.jinja_env.filters['currency'] = format_currency

    # Context processor: Cung cấp giỏ hàng và danh mục ở mọi template
    @app.context_processor
    def inject_global_data():
        cart = session.get('cart', {})
        cart_count = sum(item.get('quantity', 0) for item in cart.values())
        try:
            categories = Category.query.all()
        except Exception:
            categories = []
        return {
            'cart_count': cart_count,
            'header_categories': categories
        }

    # Trang lỗi tùy biến
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
