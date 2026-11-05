from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail
import threading

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            app.logger.info(f"Đã gửi email thành công đến: {msg.recipients}")
        except Exception as e:
            app.logger.error(f"Gửi email thất bại: {e}")

class MailService:
    @staticmethod
    def send_order_confirmation(order):
        """
        Gửi email xác nhận đặt hàng kèm hóa đơn chi tiết cho khách hàng.
        Sử dụng Flask-Mail và chạy nền qua Threading để không làm chậm giao diện.
        """
        try:
            app = current_app._get_current_object()
            sender = app.config.get('MAIL_DEFAULT_SENDER')
            
            subject = f"Xác nhận đơn hàng #{order.order_code} - Fashion Store"
            
            # Render nội dung email từ template HTML
            html_body = render_template('email/order_confirmation.html', order=order)
            
            msg = Message(
                subject=subject,
                sender=sender,
                recipients=[order.customer_email],
                html=html_body
            )
            
            # Chạy thread bất đồng bộ để trải nghiệm người dùng nhanh nhất
            thr = threading.Thread(target=send_async_email, args=[app, msg])
            thr.start()
            return True
        except Exception as e:
            current_app.logger.error(f"Lỗi khởi tạo email: {e}")
            return False
