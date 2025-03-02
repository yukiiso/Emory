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
            user1 = User(name='Alice', age=30, gender='Female', username='alice', email='alice@example.com', password='hashed_password', category = "1")
            user2 = User(name='Bob', age=25, gender='Male', username='bob', email='bob@example.com', password='hashed_password', category = "1")
            db.session.add_all([user1, user2])
            db.session.commit()
            print("SQL data seeded successfully.")
        else:
            print("SQL data already exists. Skipping seed.")
    except Exception as e:
        print(f"Error seeding SQL data: {e}")

    try:
        if not Question.query.first():
            question1 = Question(content='What is the concern or problem that brought you here?')
            question2 = Question(content='How is this concern or problem impacting your life?')
            question3 = Question(content='What are your hopes and wishes for resolving this concern or problem?')
            question4 = Question(content='What activities do you enjoy doing?')
            question5 = Question(content='Is there anything you want to talk about?')
            db.session.add_all([question1, question2, question3, question4, question5])
            db.session.commit()
            print("SQL data seeded successfully.")
        else:
            print("SQL data already exists. Skipping seed.")
    except Exception as e:
        print(f"Error seeding SQL data: {e}")

def seed_dynamo_data(): 

    return
