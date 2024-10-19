from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

# Thông tin kết nối tới MongoDB
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
DB_NAME = os.environ.get("DB_NAME", "your_database_name")

# Khởi tạo client MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)

# Kết nối tới database
db = client[DB_NAME]
