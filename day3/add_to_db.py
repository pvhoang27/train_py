import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Lệnh này sẽ tự động tìm file .env trong cùng thư mục và tải các biến vào hệ thống
load_dotenv()

def import_csv_to_mysql():
    print("Đang đọc file CSV...")
    df = pd.DataFrame()
    
    try:
        df = pd.read_csv("full_data_phuong_xa_333_trang.csv")
    except FileNotFoundError:
        print("Không tìm thấy file CSV. Hãy chắc chắn đường dẫn đúng.")
        return

    # Đổi tên cột trong DataFrame cho khớp với Database
    df.rename(columns={
        'Tỉnh': 'tinh_thanh',
        'Phường, xã mới': 'phuong_xa_moi',
        'Phường, xã trước sáp nhập': 'phuong_xa_cu'
    }, inplace=True)

    # ---------------------------------------------------------
    # LẤY THÔNG TIN TỪ FILE .ENV (KHÔNG LỘ MẬT KHẨU TRONG CODE NỮA)
    # ---------------------------------------------------------
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')

    # Tạo chuỗi kết nối
    engine_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    
    print("Đang kết nối vào MySQL...")
    try:
        engine = create_engine(engine_url)
        
        # Đẩy dữ liệu vào bảng
        df.to_sql(name='ds_phuong_xa_sap_nhap', con=engine, if_exists='replace', index=False)
        
        print(f"🎉 Đã thêm thành công {len(df)} dòng vào database {database}!")
        
    except Exception as e:
        print(f"Lỗi khi kết nối hoặc thêm dữ liệu vào DB: {e}")

if __name__ == "__main__":
    import_csv_to_mysql()