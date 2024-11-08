
# Hệ Thống Crawl Dữ Liệu lớn thời gian thực và tự động
## Giới thiệu
Dự án này là một hệ thống tự động được thiết kế để crawl dữ liệu từ web theo thời gian thực và lưu trữ vào cơ sở dữ liệu. Hệ thống có thể cấu hình để lấy dữ liệu từ các trang web cụ thể, trích xuất dữ liệu có cấu trúc và lưu trữ vào cơ sở dữ liệu quan hệ hoặc NoSQL để xử lý và phân tích thêm.

Mục tiêu của hệ thống là tự động hóa quá trình lấy dữ liệu từ các nguồn khác nhau mà không cần sự can thiệp thủ công. Hệ thống có khả năng tích hợp với nhiều loại cơ sở dữ liệu khác nhau, giúp việc quản lý dữ liệu trở nên đơn giản và hiệu quả hơn.

# Kiến Trúc Hệ Thống

Hệ thống bao gồm các thành phần chính sau:

**Web Data (Nguồn dữ liệu từ web):** Dữ liệu được lấy từ các nguồn web cụ thể.

**Crawler Application:** Ứng dụng crawler tự động lấy dữ liệu từ các trang web mục tiêu.

**MongoDB Server:** Dữ liệu thu thập từ Crawler sẽ được lưu vào MongoDB để xử lý bước đầu.

**Spark Server:** Xử lý và phân tích và làm sạch dữ liệu với Apache Spark.

**Postgres Server:** Sau khi được Spark xử lý, dữ liệu sẽ được lưu trữ vào Postgres để lưu trữ dạng quan hệ.

**PowerBI App:** Ứng dụng Power BI giúp trực quan hóa dữ liệu và tạo ra các báo cáo trực quan.

## Cách Hoạt Động
1. **Dữ liệu được lấy từ các trang web qua Crawler App.**
2. **Sau khi thu thập, dữ liệu được lưu tạm thời vào MongoDB.**
3. **Apache Spark xử lý và làm sạch dữ liệu.**
4. **Dữ liệu sau đó được lưu vào Postgres để lưu trữ dài hạn.**
5. **Dữ liệu cuối cùng sẽ được trực quan hóa bằng PowerBI.**
## Cài Đặt
1. **Cài đặt Docker:**

   - Truy cập trang tải Docker: [Docker Downloads](https://www.docker.com/products/docker-desktop)
   - Tải và cài đặt Docker Desktop theo hướng dẫn trên trang.
   - 
2. **Clone Dự Án từ GitHub:**

   - Mở terminal hoặc command prompt.
   - Chạy lệnh sau để sao chép dự án từ GitHub:
     ```
     git clone https://github.com/NRI12/stream_crawl_data.git
     ```
   - Di chuyển vào thư mục dự án:
     ```
     cd stream_crawl_data
     ```

3. **Xây Dựng và Chạy Dự Án với Docker Compose:**

   - Chạy lệnh sau để xây dựng và khởi chạy các container:
     ```
     docker-compose up --build
     ```

4. **Xem Trạng Thái và Logs:**

   - Để kiểm tra trạng thái của các container và xem log, sử dụng lệnh:
     ```
     docker-compose logs
     ```

   - Để dừng và loại bỏ các container, sử dụng lệnh:
     ```
     docker-compose down
     ```
## Kết quả
Ứng dụng sẽ tự động thu lập tiền xử lý và lưu dữ liệu dựa trên trang web đã cài đặt bằng spider vào các thành phần tương ứng bạn có thể mở xem trên các csdl server cài trên máy với authentication  được setting trên docker-compose (not safe but continue)
# scrapy_khanhhuyen
