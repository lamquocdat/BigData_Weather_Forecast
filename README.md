# BigData_Weather_Forecast
Đồ án dự báo thời tiết môn Công nghệ Dữ liệu lớn IE212, UIT

## Tạo file .env
Sao chép nội dung trong file .env.example và dán vào file .env trong thư mục webapp (tạo file .env nếu chưa có).

Chỉnh sửa lại nội dung trong file .env cho phù hợp.

## Chạy Kafka
Cần phải tải kafka và chạy thử được kafka trước.

Trong thư mục kafka chạy hai lệnh sau ở hai terminal độc lập để chạy zookeeper và server:
``````
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties
``````

## Chạy Producer
Chạy producer trong thư mục machine_learning/notebooks/Weather_producer.ipynb (trong project thì cái này được chạy trên anaconda, với các đường dẫn csv tùy chỉnh)

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
pip install pyspark flask kafka-python python-dotenv pymongo pandas

# Lưu thông tin các thư viện vừa cài đặt vào requirements.txt
pip freeze > requirements.txt

# Chạy lệnh sau để chạy project
python app.py

# Kể từ các lần sau, khi mở project lên thì chỉ cần chạy:
## Window
cd .\webapp ; venv\Scripts\activate ; python app.py

## Linux
cd .\webapp && venv\Scripts\activate && python app.py
``````

## Về model machine learning và các đối tượng liên quan
Chạy file training-weather-forcast.ipynb trong machine_learning/notebooks/training-weather-forcast.ipynb để xuất các model (trong project thì file này được chạy trên kaggle)

Sau khi xuất model xong thì đưa vào thư mục webapp/app/models và muốn sử dụng model đó thì sửa đường dẫn model_path trỏ đến model đó trong mykafka/consumer.py

Các thành phần khác như StringIndexer thì sau khi xuất ra cần đưa vào webapp/app/utils và muốn sử dụng StringIndexer đó thì sửa đường dẫn trong StringIndexerModel.load() trong app/services/predictServices.py

## Retrain model và cập nhật
Cứ mỗi lần cần cập nhật model thì chạy lại file notebook và xuất ra mô hình (cả StringIndexer nếu có)

Sau đó đem các file đó trong các thư mục tương ứng là webapp/app/models và webapp/app/utils, sửa lại đường dẫn dẫn đến model trong comsumer.py và đường dẫn dẫn đến StringIndexer hoặc những thành phần khác trong predictServices.py

Sau đó chạy lại web app