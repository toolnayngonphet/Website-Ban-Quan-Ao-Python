from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class ProductForm(FlaskForm):
    name = StringField('Tên sản phẩm', validators=[
        DataRequired(message='Vui lòng nhập tên sản phẩm'),
        Length(max=200)
    ])
    category_id = SelectField('Danh mục', coerce=int, validators=[
        DataRequired(message='Vui lòng chọn danh mục')
    ])
    price = FloatField('Giá gốc (VNĐ)', validators=[
        DataRequired(message='Vui lòng nhập giá bán'),
        NumberRange(min=1000, message='Giá bán tối thiểu 1.000 VNĐ')
    ])
    promotional_price = FloatField('Giá khuyến mãi (VNĐ)', validators=[
        Optional(),
        NumberRange(min=0, message='Giá khuyến mãi không hợp lệ')
    ])
    stock = IntegerField('Số lượng tồn kho', validators=[
        DataRequired(message='Vui lòng nhập số lượng tồn kho'),
        NumberRange(min=0, message='Số lượng không âm')
    ], default=50)
    sizes = StringField('Kích thước (cách nhau bởi dấu phẩy)', default='S, M, L, XL')
    colors = StringField('Màu sắc (cách nhau bởi dấu phẩy)', default='Đen, Trắng, Xanh')
    image = FileField('Hình ảnh sản phẩm', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Chỉ chấp nhận file ảnh: jpg, jpeg, png, webp')
    ])
    description = TextAreaField('Mô tả chi tiết sản phẩm')
    is_featured = BooleanField('Sản phẩm nổi bật (Hiển thị trang chủ)')
    submit = SubmitField('Lưu sản phẩm')

class CategoryForm(FlaskForm):
    name = StringField('Tên danh mục', validators=[
        DataRequired(message='Vui lòng nhập tên danh mục'),
        Length(max=100)
    ])
    description = TextAreaField('Mô tả danh mục')
    submit = SubmitField('Lưu danh mục')
