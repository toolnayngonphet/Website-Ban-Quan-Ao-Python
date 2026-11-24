import os
import sys
import time
import threading

sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from seed_data import seed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.makedirs('screenshots', exist_ok=True)

# Run seed
seed()

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False

def run_server():
    app.run(port=5050, debug=False, use_reloader=False)

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(2)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1280,850')
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Trang chu
    driver.get('http://127.0.0.1:5050/')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_1_trang_chu.png')
    print('1. Trang chu captured')

    # 2. Cua hang
    driver.get('http://127.0.0.1:5050/shop')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_2_cua_hang.png')
    print('2. Cua hang captured')

    # 3. Chi tiet san pham
    driver.get('http://127.0.0.1:5050/product/ao-thun-cotton-oversize-basic')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_3_chi_tiet_san_pham.png')
    print('3. Chi tiet san pham captured')

    # 4. Gio hang
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_4_gio_hang.png')
    print('4. Gio hang captured')

    # 5. Thanh toan VietQR (demo order)
    driver.get('http://127.0.0.1:5050/order/success/DH20261105-DEMO')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_5_thanh_toan_vietqr.png')
    print('5. Thanh toan VietQR captured')

    # 6. Admin Dashboard
    driver.get('http://127.0.0.1:5050/login')
    driver.find_element(By.NAME, 'username').send_keys('admin')
    driver.find_element(By.NAME, 'password').send_keys('admin123')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    time.sleep(1.5)
    driver.get('http://127.0.0.1:5050/admin/')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_6_admin_dashboard.png')
    print('6. Admin Dashboard captured')

    # 7. Admin Products
    driver.get('http://127.0.0.1:5050/admin/products')
    time.sleep(1.5)
    driver.save_screenshot('screenshots/hinh4_7_admin_products.png')
    print('7. Admin Products captured')

finally:
    driver.quit()
    print('ALL SCREENSHOTS CAPTURED SUCCESSFULLY!')
