from flask import Flask
from mykafka  import init_kafka
from routes import main
import os

def create_app():
    template_dir = os.path.abspath('templates')
    app = Flask(__name__, template_folder=template_dir)

    # Đăng ký các routes cho ứng dụng
    app.register_blueprint(main)

    # Cấu hình kafka
    init_kafka()

    return app
