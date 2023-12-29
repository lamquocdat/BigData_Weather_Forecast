from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

# Thông tin kết nối tới MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("DB_NAME", "your_database_name")

# Khởi tạo client MongoDB
client = MongoClient(MONGO_URI)

# Kết nối tới database
db = client[DB_NAME]
