from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.services.vietqr_service import VietQRService

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/products', methods=['GET'])
def get_products():
    """
    REST API trả về danh sách sản phẩm thời trang định dạng JSON (CLO3).
    Hỗ trợ tham số lọc: ?category_id=... &search=... &limit=...
    """
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    limit = request.args.get('limit', 20, type=int)

    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.limit(limit).all()
    return jsonify({
        'status': 'success',
        'count': len(products),
        'data': [p.to_dict() for p in products]
    }), 200

@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product_detail(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy sản phẩm'}), 404
    return jsonify({
        'status': 'success',
        'data': product.to_dict()
    }), 200

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    data = [{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'product_count': c.products.count()
    } for c in categories]
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    }), 200

@api_bp.route('/orders/<order_code>', methods=['GET'])
def get_order_by_code(order_code):
    order = Order.query.filter_by(order_code=order_code).first()
    if not order:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy đơn hàng'}), 404
    return jsonify({
        'status': 'success',
        'data': order.to_dict()
    }), 200

@api_bp.route('/banks', methods=['GET'])
def get_vietqr_banks():
    """Gọi API mạng bên ngoài và trả về JSON danh sách ngân hàng"""
    banks = VietQRService.get_supported_banks()
    return jsonify({
        'status': 'success',
        'count': len(banks),
        'data': banks
    }), 200
