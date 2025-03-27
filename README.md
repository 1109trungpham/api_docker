# Cấu trúc thư mục dự án
api_docker/
│── app/
│   ├── main.py
│   ├── requirements.txt
│── dockerfile         

# main.py (chứa mã nguồn API)

# requirements.txt (chứa danh sách thư viện cần cài đặt):
fastapi
httpx
uvicorn
pydantic

# dockerfile (chứa cấu hình docker image):
FROM python:3.9                                                     <!-- Sử dụng Python 3.9 làm base image -->
WORKDIR /app                                                        <!-- Thiết lập thư mục làm việc trong container -->
COPY app/ /app/                                                     <!-- Copy toàn bộ thư mục app vào container -->
RUN pip install --no-cache-dir -r requirements.txt                  <!-- Cài đặt thư viện từ requirements.txt -->
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  <!-- Chạy ứng dụng với Uvicorn -->

# Triển khai API trên Docker
<!-- Đảm bảo bạn đang ở thư mục dự án (api_docker/) khi chạy lệnh dưới -->
docker build -t api_docker .           <!-- Xây dựng Docker Image -->
docker run -p 8000:8000 api_docker     <!-- Tạo và chạy Docker Container -->

# Kiểm tra API
http://127.0.0.1:8000/docs                                                          <!-- Truy cập Swagger UI của API -->
http://127.0.0.1:8000/weather?lon=105.85&lat=21.03&start_year=2023&end_year=2024    <!-- Thử API -->



