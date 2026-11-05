from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    promotional_price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(255), default='default_product.jpg')
    sizes = db.Column(db.String(100), default='S, M, L, XL')  # Chuỗi phân cách bởi dấu phẩy
    colors = db.Column(db.String(100), default='Đen, Trắng') # Chuỗi phân cách bởi dấu phẩy
    description = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    @property
    def current_price(self):
        if self.promotional_price and 0 < self.promotional_price < self.price:
            return self.promotional_price
        return self.price

    @property
    def discount_percent(self):
        if self.promotional_price and 0 < self.promotional_price < self.price:
            return int(round((1 - self.promotional_price / self.price) * 100))
        return 0

    @property
    def size_list(self):
        if not self.sizes:
            return []
        return [s.strip() for s in self.sizes.split(',') if s.strip()]

    @property
    def color_list(self):
        if not self.colors:
            return []
        return [c.strip() for c in self.colors.split(',') if c.strip()]

    def to_dict(self):
        """Hàm serialize sang JSON cho REST API (CLO3)"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'price': self.price,
            'promotional_price': self.promotional_price,
            'current_price': self.current_price,
            'discount_percent': self.discount_percent,
            'stock': self.stock,
            'image_url': self.image_url,
            'sizes': self.size_list,
            'colors': self.color_list,
            'category_name': self.category.name if self.category else '',
            'is_featured': self.is_featured,
            'description': self.description
        }

    def __repr__(self):
        return f'<Product {self.name} - {self.price}>'
