import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'thoi-trang-fashion-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'clothing_shop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads', 'products')
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # 6 MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Mail configuration (Flask-Mail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'demo.shop.fashion@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'demo-app-password')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', ('Shop Quần Áo Fashion Store', 'demo.shop.fashion@gmail.com'))
    
    # VietQR Payment Configuration (CLO3)
    VIETQR_BANK_ID = os.environ.get('VIETQR_BANK_ID', 'MB')  # MB Bank
    VIETQR_ACCOUNT_NO = os.environ.get('VIETQR_ACCOUNT_NO', '0388999888')
    VIETQR_ACCOUNT_NAME = os.environ.get('VIETQR_ACCOUNT_NAME', 'NGUYEN VAN A')
    VIETQR_TEMPLATE = 'compact2'  # compact, compact2, qr_only
    
    # Pagination
    ITEMS_PER_PAGE = 8
    ADMIN_ITEMS_PER_PAGE = 10
