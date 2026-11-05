from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class CheckoutForm(FlaskForm):
    customer_name = StringField('Họ và tên người nhận', validators=[
        DataRequired(message='Vui lòng nhập họ tên người nhận'),
        Length(max=100)
    ])
    customer_email = StringField('Địa chỉ Email', validators=[
        DataRequired(message='Vui lòng nhập email'),
        Email(message='Email không hợp lệ')
    ])
    customer_phone = StringField('Số điện thoại liên hệ', validators=[
        DataRequired(message='Vui lòng nhập số điện thoại'),
        Length(min=9, max=15, message='Số điện thoại không hợp lệ')
    ])
    shipping_address = StringField('Địa chỉ nhận hàng chi tiết', validators=[
        DataRequired(message='Vui lòng nhập địa chỉ nhận hàng'),
        Length(max=255)
    ])
    note = TextAreaField('Ghi chú đơn hàng (Thời gian giao, chỉ dẫn...)')
    payment_method = RadioField('Phương thức thanh toán', choices=[
        ('COD', 'Thanh toán tiền mặt khi nhận hàng (COD)'),
        ('VIETQR', 'Chuyển khoản ngân hàng tức thì (Mã VietQR tự động)')
    ], default='VIETQR', validators=[DataRequired()])
    submit = SubmitField('Xác nhận đặt hàng')
