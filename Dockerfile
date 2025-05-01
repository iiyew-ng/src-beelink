# Base image Ubuntu + Python
FROM python:3.10-slim-bullseye

# Thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ mã nguồn vào container
COPY . /app

# Cài đặt các gói phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Expose cổng Flask (mặc định là 5000)
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app.py"]