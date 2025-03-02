from backend.app import create_app
from backend.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = create_app(test=False)

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
