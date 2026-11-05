from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    
    # Quan hệ 1-n với Product
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'
