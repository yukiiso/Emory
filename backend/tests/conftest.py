import os
import sys
import pytest

# `Emory/` を PYTHONPATH に追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../.."))

from backend.app import create_app
from backend.models import db

@pytest.fixture(scope="function")
def test_client():
    """テスト用の Flask クライアントを作成"""
    app = create_app(test=True)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
