import urllib.parse
import json
import requests
from flask import current_app

class VietQRService:
    """
    Dịch vụ tích hợp VietQR (CLO3: Lập trình mạng, API, JSON, urllib/requests).
    Tự động sinh mã QR thanh toán ngân hàng cho từng đơn hàng & tra cứu danh sách ngân hàng Việt Nam.
    """
    API_BANKS_URL = "https://api.vietqr.io/v2/banks"
    
    # Danh sách ngân hàng phổ biến dự phòng khi mất kết nối mạng
    FALLBACK_BANKS = [
        {"id": 17, "name": "Ngân hàng TMCP Quân đội", "code": "MB", "bin": "970422", "shortName": "MBBank", "logo": "https://api.vietqr.io/img/MB.png"},
        {"id": 43, "name": "Ngân hàng Ngoại thương Việt Nam", "code": "VCB", "bin": "970436", "shortName": "Vietcombank", "logo": "https://api.vietqr.io/img/VCB.png"},
        {"id": 44, "name": "Ngân hàng Công thương Việt Nam", "code": "CTG", "bin": "970415", "shortName": "VietinBank", "logo": "https://api.vietqr.io/img/CTG.png"},
        {"id": 2, "name": "Ngân hàng Nông nghiệp & Phát triển Nông thôn", "code": "VBA", "bin": "970405", "shortName": "Agribank", "logo": "https://api.vietqr.io/img/VBA.png"},
        {"id": 38, "name": "Ngân hàng TMCP Kỹ Thương", "code": "TCB", "bin": "970407", "shortName": "Techcombank", "logo": "https://api.vietqr.io/img/TCB.png"},
        {"id": 42, "name": "Ngân hàng TMCP Việt Nam Thịnh Vượng", "code": "VPB", "bin": "970432", "shortName": "VPBank", "logo": "https://api.vietqr.io/img/VPB.png"},
        {"id": 1, "name": "Ngân hàng TMCP Á Châu", "code": "ACB", "bin": "970416", "shortName": "ACB", "logo": "https://api.vietqr.io/img/ACB.png"}
    ]

    @classmethod
    def get_supported_banks(cls):
        """
        Gọi API VietQR qua requests (lập trình mạng + xử lý JSON)
        để lấy danh sách tất cả các ngân hàng Việt Nam hiện tại.
        """
        try:
            response = requests.get(cls.API_BANKS_URL, timeout=4)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == "00" and "data" in data:
                    return data["data"]
        except Exception as e:
            current_app.logger.warning(f"Không thể kết nối đến VietQR API: {e}. Sử dụng fallback.")
        return cls.FALLBACK_BANKS

    @classmethod
    def generate_qr_url(cls, order_code, amount, memo=None):
        """
        Sinh URL mã QR động chuẩn VietQR.
        Cú pháp: https://img.vietqr.io/image/<BANK_ID>-<ACCOUNT_NO>-<TEMPLATE>.png?amount=<AMOUNT>&addInfo=<MEMO>&accountName=<NAME>
        """
        bank_id = current_app.config.get('VIETQR_BANK_ID', 'MB')
        account_no = current_app.config.get('VIETQR_ACCOUNT_NO', '0388999888')
        account_name = current_app.config.get('VIETQR_ACCOUNT_NAME', 'SHOP QUAN AO FASHION')
        template = current_app.config.get('VIETQR_TEMPLATE', 'compact2')
        
        # Nội dung chuyển khoản mặc định là mã đơn hàng
        info_text = memo or f"DH {order_code}"
        
        params = {
            'amount': int(round(amount)),
            'addInfo': info_text,
            'accountName': account_name
        }
        query_string = urllib.parse.urlencode(params)
        
        qr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-{template}.png?{query_string}"
        return {
            'qr_url': qr_url,
            'bank_id': bank_id,
            'account_no': account_no,
            'account_name': account_name,
            'amount': int(round(amount)),
            'memo': info_text
        }
