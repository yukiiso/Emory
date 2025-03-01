from app import create_app
from config import FLASK_HOST, FLASK_PORT

# Flask アプリを作成
app = create_app()

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=int(FLASK_PORT))
