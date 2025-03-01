from backend.models import db, User, Question, Record, FaceAnalysis, VoiceAnalysis

def seed_database(app):
    """初回の Seed Data を投入"""
    print("Seeding SQL and DynamoDB data...")

    with app.app_context():
        seed_sql_data(db, User, Question, Record, FaceAnalysis, VoiceAnalysis)
        seed_dynamo_data()

    print("Seeding completed.")

def seed_sql_data(db, User, Question, Record, FaceAnalysis, VoiceAnalysis):
    """SQL データベースにシードデータを挿入する"""
    
    try:
        # Check if any users already exist in the SQL database
        if not User.query.first():  # Check if the 'users' table is empty
            user1 = User(name='Alice', age=30, gender='Female', username='alice', email='alice@example.com', password='hashed_password')
            user2 = User(name='Bob', age=25, gender='Male', username='bob', email='bob@example.com', password='hashed_password')
            db.session.add_all([user1, user2])
            db.session.commit()
            print("SQL data seeded successfully.")
        else:
            print("SQL data already exists. Skipping seed.")
    except Exception as e:
        print(f"Error seeding SQL data: {e}")

def seed_dynamo_data(): 

    return
