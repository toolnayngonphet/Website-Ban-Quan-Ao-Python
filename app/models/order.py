from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text, nullable=True)
    
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_method = db.Column(db.String(30), default='COD', nullable=False)  # 'COD' hoặc 'VIETQR'
    payment_status = db.Column(db.String(30), default='pending', nullable=False)  # 'pending', 'paid', 'failed'
    order_status = db.Column(db.String(30), default='pending', nullable=False)  # 'pending', 'confirmed', 'shipping', 'completed', 'cancelled'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy='joined', cascade='all, delete-orphan')

    def to_dict(self):
        """Serialize sang JSON cho REST API (CLO3)"""
        return {
            'order_code': self.order_code,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': self.shipping_address,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'order_status': self.order_status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': [item.to_dict() for item in self.items]
        }

    def __repr__(self):
        return f'<Order {self.order_code} - {self.total_amount}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    size = db.Column(db.String(20), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    subtotal = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'price': self.price,
            'quantity': self.quantity,
            'size': self.size,
            'color': self.color,
            'subtotal': self.subtotal
        }
