import requests
import psycopg2
import json
# URL của API
url = "https://debatedata.io/api/motion/update-infinite-motions"

# Database connection parameters
connection = psycopg2.connect(
    host="localhost",      # Host là localhost
    port="5432", 
    database="process_data",
    user="root",
    password="root"
)
    # Open a cursor to perform database operations
cursor = connection.cursor()
    
    # Create table if it doesn't exist
create_table_query = """
        CREATE TABLE IF NOT EXISTS competition_data (
            index SERIAL PRIMARY KEY,
            city TEXT,
            country TEXT,
            date TIMESTAMP,
            infoslide TEXT,
            level TEXT,
            motion TEXT,
            region TEXT,
            round TEXT,
            tournament TEXT,
            types TEXT[],
            adjudicators TEXT[]
        )
    """
    
cursor.execute(create_table_query)
connection.commit()
print("Table created successfully.")
    

try:
    # Mở cursor để thực hiện thao tác với DB
    cursor = connection.cursor()

    # Câu lệnh SQL để chèn dữ liệu vào bảng competition_data
    insert_query = """
        INSERT INTO competition_data (
            city, country, date, infoslide, level, motion, region, 
            round, tournament, types, adjudicators
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Khởi tạo pageNumber
    page_number = 1
    while True:
        # Payload của yêu cầu POST
        payload = {
            "chartAdded": False,
            "citiesActivated": [],
            "level": [],
            "motionTypes": [],
            "online": False,
            "pageLimit": 12,
            "pageNumber": page_number,
            "randomActivated": False,
            "searchText": "",
            "sortDate": False,
            "style": [],
            "video": False
        }

        # Headers (nếu cần)
        headers = {
            "Content-Type": "application/json"
        }

        # Gửi yêu cầu POST
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi

        # Chuyển dữ liệu thành JSON và lấy phần 'motions'
        data = response.json()
        motions = data.get("motions", [])

        # Nếu không còn motion nào trong kết quả, dừng vòng lặp
        if not motions:
            print("Không còn dữ liệu để lấy.")
            break

        # Duyệt qua từng motion và lưu vào DB
        for motion_data in motions:
            # Lấy các trường từ từng motion
           
            city = motion_data.get("City", None)
            country = motion_data.get("Country", None)
            
            date = motion_data.get("Date", None)
            
            infoslide = motion_data.get("Infoslide", None)
            
            level = motion_data.get("Level", None)
            
            motion = motion_data.get("Motion", None)
            region =motion_data.get("Region", None)
            
            round = motion_data.get("Round", None)
            
            tournament = motion_data.get("Tournament", None)
            
            types = motion_data.get("Types", [])
            
            adjudicators = motion_data.get("adjudicators", [])
            

            # Thực hiện INSERT vào bảng
            cursor.execute(insert_query, (
                city, country, date, infoslide, level, motion, region, 
                round, tournament, types, adjudicators
            ))

        # Lưu thay đổi vào DB
        connection.commit()
        print(f"Dữ liệu từ trang {page_number} đã được lưu vào DB.")

        # Tăng pageNumber để lấy trang kế tiếp
        page_number += 1

except Exception as error:
    print("Error:", error)

finally:
    # Đóng cursor và connection
    cursor.close()
    connection.close()
