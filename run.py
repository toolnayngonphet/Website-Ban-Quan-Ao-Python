from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Order, OrderItem

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Product': Product,
        'Order': Order,
        'OrderItem': OrderItem
    }

@app.cli.command('init-db')
def init_db():
    """Lệnh khởi tạo cơ sở dữ liệu: flask init-db"""
    with app.app_context():
        db.create_all()
        print('Đã khởi tạo cơ sở dữ liệu SQLite thành công!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)
