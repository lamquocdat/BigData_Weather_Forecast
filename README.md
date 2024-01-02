# BigData_Weather_Forecast
Đồ án dự báo thời tiết môn Công nghệ Dữ liệu lớn IE212, trường UIT

## Tạo file .env
Sao chép nội dung trong file .env.example và dán vào file .env trong thư mục webapp (tạo file .env nếu chưa có).
Chỉnh sửa lại nội dung trong file .env cho phù hợp.

## Chạy Kafka
Cần phải tải kafka trước.
Trong thư mục kafka chạy hai lệnh sau:
``````
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties
``````

## Chạy Producer
Chạy producer trong thư mục machine_learning/notebooks/producer.ipynb
Hiện tại đang chạy old_motobike.ipynb để test với đồ án dự đoán giá xe cũ.

## Chạy Web app 
Sau đó chạy các lệnh sau để chạy web app
``````
# Chuyển đến thư mục web app
cd .\webapp
# Nếu chưa có file venv thì chạy lệnh
python -m venv venv

# Chạy một trong hai lệnh sau để chạy project trong môi trường ảo
## Trên Windows
venv\Scripts\activate

## macOS/Linux
venv/bin/activate

# Chạy các file sau để cài đặt các thư viện cần thiết, nếu báo lỗi thiếu thư viện vui lòng tự cài thêm
pip install flask kafka-python python-dotenv pymongo joblib scikit-learn pandas numpy
pip freeze > requirements.txt

# Chạy lệnh sau để chạy project
python app.py
``````

## Về model machine learning và các  đối tượng liên quan
Sau khi xuất model xong thì đưa vào thư mục webapp/app/models
Các thành phần khác như encoder, scaler thì sau khi xuất ra cần đưa vào webapp/app/utils

## Retrain model và cập nhật
Cứ mỗi lần cần cập nhật model thì chạy lại file notebook và xuất ra mô hình (cả scaler, encoder nếu có) thành file .joblib
Sau đó đem các file đó trong các thư mục tương ứng là webapp/app/models và webapp/app/utils
Sau đó chạy lại web app