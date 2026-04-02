import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_all_pages():
    print("Đang khởi tạo trình duyệt...")
    options = webdriver.ChromeOptions()
    # Bạn có thể bỏ comment dòng dưới nếu muốn trình duyệt chạy ngầm (không hiện cửa sổ)
    # options.add_argument('--headless') 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://vnexpress.net/tra-cuu-3-321-phuong-xa-tren-ca-nuoc-sau-sap-xep-4903454.html"
    driver.get(url)
    print("Đã mở trang web. Đang chờ tải dữ liệu...")

    all_data = [] # Mảng lớn để lưu toàn bộ dữ liệu của tất cả các trang

    try:
        time.sleep(3)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Đang quét {len(iframes)} iframe để tìm bảng...")
        
        table_found = False
        
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.default_content() 
                driver.switch_to.frame(iframe)
                
                # Kiểm tra xem có bảng ở đây không
                WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.body-row"))
                )
                
                print(f"-> ĐÚNG RỒI! Bắt đầu cào dữ liệu từ bảng này.")
                table_found = True
                
                # Lấy tổng số trang để in log cho đẹp (từ thẻ <span class="pagination-total">)
                try:
                    total_pages_str = driver.find_element(By.CSS_SELECTOR, "span.pagination-total").text
                    total_pages = int(total_pages_str)
                except:
                    total_pages = 333 # Fallback mặc định nếu không lấy được số
                    
                current_page = 1
                
                # VÒNG LẶP CÀO TẤT CẢ CÁC TRANG
                while True:
                    print(f"Đang cào dữ liệu trang {current_page}/{total_pages}...")
                    
                    # 1. Chờ dữ liệu của trang hiện tại ổn định
                    rows = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.body-row"))
                    )
                    
                    # 2. Lấy dữ liệu từng hàng
                    for row in rows:
                        cols = row.find_elements(By.CSS_SELECTOR, "td div.cell-body p")
                        if len(cols) >= 3:
                            tinh = cols[0].text.strip()
                            xa_moi = cols[1].text.strip()
                            xa_cu = cols[2].text.strip()
                            all_data.append([tinh, xa_moi, xa_cu])
                            
                    # 3. Tìm nút Next (Tiếp theo)
                    try:
                        next_btn = driver.find_element(By.CSS_SELECTOR, "button.pagination-btn.next")
                        
                        # Kiểm tra xem nút Next có bị khóa không (nghĩa là đã đến trang cuối)
                        if next_btn.get_attribute("disabled") == "true" or current_page >= total_pages:
                            print("Đã quét đến trang cuối cùng!")
                            break
                            
                        # Dùng Javascript để click nút Next (tránh lỗi nút bị che khuất)
                        driver.execute_script("arguments[0].click();", next_btn)
                        
                        current_page += 1
                        
                        # RẤT QUAN TRỌNG: Dừng 1 - 1.5 giây để bảng cập nhật dữ liệu mới sau khi bấm Next
                        time.sleep(1.5) 
                        
                    except Exception as e_btn:
                        print("Không tìm thấy nút Next hoặc đã hết trang.")
                        break

                break # Xong toàn bộ quá trình thì thoát vòng lặp tìm iframe
                
            except Exception as e_iframe:
                continue # Nếu lỗi ở iframe này thì thử iframe khác
                
        if not table_found:
            print("Đã quét hết iframe nhưng vẫn không thấy bảng.")
        
        # BƯỚC CUỐI: LƯU TOÀN BỘ DỮ LIỆU RA FILE CSV
        if all_data:
            df = pd.DataFrame(all_data, columns=["Tỉnh", "Phường, xã mới", "Phường, xã trước sáp nhập"])
            file_name = "full_data_phuong_xa_333_trang.csv"
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            
            print("\n" + "="*40)
            print("🎉 HOÀN THÀNH!")
            print(f"Tổng số dòng cào được: {len(all_data)}")
            print(f"Đã lưu toàn bộ vào file: {file_name}")
            print("="*40)

    except Exception as e:
        print(f"Lỗi ngoài dự kiến: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_all_pages()