from app import create_app
import sys
from dotenv import load_dotenv
load_dotenv()
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))

    app.run(debug=True, port=port)
