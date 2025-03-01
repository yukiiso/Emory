from models import db, User, Session, UserResponse

def seed_database():
    """初回の Seed Data を投入"""
    if User.query.first():  # すでにデータがある場合はスキップ
        print("✅ Seed Data はすでに投入済みです")
        return

    # ユーザーの追加
    user1 = User(name="Alice", email="alice@example.com")
    user2 = User(name="Bob", email="bob@example.com")

    db.session.add_all([user1, user2])
    db.session.commit()

    # セッションの追加
    session1 = Session(user_id=user1.id)
    session2 = Session(user_id=user2.id)

    db.session.add_all([session1, session2])
    db.session.commit()

    # ユーザー回答の追加
    response1 = UserResponse(user_id=user1.id, session_id=session1.id, response_text="Feeling good!")
    response2 = UserResponse(user_id=user2.id, session_id=session2.id, response_text="Not so great.")

    db.session.add_all([response1, response2])
    db.session.commit()

    print("✅ Seed Data の投入が完了しました！")
