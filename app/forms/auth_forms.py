from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập hoặc Email', validators=[DataRequired(message='Vui lòng nhập tên đăng nhập hoặc email')])
    password = PasswordField('Mật khẩu', validators=[DataRequired(message='Vui lòng nhập mật khẩu')])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(message='Vui lòng nhập tên đăng nhập'),
        Length(min=3, max=30, message='Tên đăng nhập từ 3 đến 30 ký tự')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Vui lòng nhập email'),
        Email(message='Email không hợp lệ')
    ])
    full_name = StringField('Họ và tên', validators=[
        DataRequired(message='Vui lòng nhập họ và tên'),
        Length(max=100)
    ])
    phone = StringField('Số điện thoại', validators=[
        DataRequired(message='Vui lòng nhập số điện thoại'),
        Length(min=9, max=15, message='Số điện thoại không hợp lệ')
    ])
    address = StringField('Địa chỉ nhận hàng', validators=[
        DataRequired(message='Vui lòng nhập địa chỉ'),
        Length(max=255)
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(message='Vui lòng nhập mật khẩu'),
        Length(min=6, message='Mật khẩu phải từ 6 ký tự trở lên')
    ])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(message='Vui lòng xác nhận mật khẩu'),
        EqualTo('password', message='Mật khẩu xác nhận không khớp')
    ])
    submit = SubmitField('Đăng ký tài khoản')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập này đã được sử dụng. Vui lòng chọn tên khác.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email này đã được đăng ký tài khoản. Vui lòng sử dụng email khác.')

class ProfileForm(FlaskForm):
    full_name = StringField('Họ và tên', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Số điện thoại', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Địa chỉ nhận hàng', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Cập nhật thông tin')
