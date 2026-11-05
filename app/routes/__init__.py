from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.cart import cart_bp
from app.routes.admin import admin_bp
from app.routes.api import api_bp

__all__ = ['main_bp', 'auth_bp', 'cart_bp', 'admin_bp', 'api_bp']
