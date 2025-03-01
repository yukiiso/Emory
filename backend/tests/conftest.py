import pytest
from backend.run import app, db

@pytest.fixture(scope="function")
def test_client():
    # テスト用の Flask アプリをセットアップ
    app.config["ENV"] = "test"
    app.config["TESTING"] = True

    # テスト用データベースを作成
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()  # テスト後にデータを削除
