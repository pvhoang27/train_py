import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_first_page():
    print("Đang khởi tạo trình duyệt...")
    options = webdriver.ChromeOptions()
    # Tạm thời không chạy ngầm (không dùng headless) để bạn nhìn thấy trình duyệt đang làm gì
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = "https://vnexpress.net/tra-cuu-3-321-phuong-xa-tren-ca-nuoc-sau-sap-xep-4903454.html"
    driver.get(url)
    print("Đã mở trang web. Đang chờ tải dữ liệu...")

    try:
        # Chờ trang load ổn định một chút
        time.sleep(3)
        
        # Tìm TẤT CẢ các thẻ iframe trên trang
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Tìm thấy {len(iframes)} iframe trên trang. Đang quét từng iframe để tìm bảng...")
        
        table_found = False
        
        for index, iframe in enumerate(iframes):
            try:
                # Đảm bảo đứng ở trang gốc trước khi chui vào iframe
                driver.switch_to.default_content() 
                driver.switch_to.frame(iframe)
                
                # Thử tìm các hàng dữ liệu (tr.body-row) trong iframe này (Chờ tối đa 3s)
                rows = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.body-row"))
                )
                
                if len(rows) > 0:
                    print(f"-> ĐÚNG RỒI! Đã tìm thấy bảng ở iframe thứ {index + 1}.")
                    table_found = True
                    
                    data = []
                    for row in rows:
                        # Tìm thẻ <p> chứa chữ
                        cols = row.find_elements(By.CSS_SELECTOR, "td div.cell-body p")
                        if len(cols) >= 3:
                            tinh = cols[0].text.strip()
                            xa_moi = cols[1].text.strip()
                            xa_cu = cols[2].text.strip()
                            data.append([tinh, xa_moi, xa_cu])
                    
                    # BƯỚC QUAN TRỌNG: LƯU FILE CSV
                    if data:
                        df = pd.DataFrame(data, columns=["Tỉnh", "Phường, xã mới", "Phường, xã trước sáp nhập"])
                        print("\n--- KẾT QUẢ TRANG 1 ---")
                        print(df.head(5))
                        
                        file_name = "data_phuong_xa_page1.csv"
                        df.to_csv(file_name, index=False, encoding='utf-8-sig')
                        print(f"\n=> ĐÃ LƯU THÀNH CÔNG {len(data)} dòng vào file: {file_name}")
                    
                    break # Tìm thấy bảng và lấy xong rồi thì thoát vòng lặp quét iframe
            except:
                # Nếu iframe này không có bảng, nó sẽ quăng lỗi timeout, ta kệ nó và đi tìm iframe tiếp theo
                continue
                
        if not table_found:
            print("Đã quét hết iframe nhưng vẫn không thấy bảng. Có thể web vừa đổi cấu trúc!")

    except Exception as e:
        print(f"Lỗi ngoài dự kiến: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_first_page()