from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(255), nullable=False)
    age             = db.Column(db.Integer)
    gender          = db.Column(db.Enum('Male', 'Female', 'Other', name='gender_enum'))
    username        = db.Column(db.String(255), unique=True, nullable=False)
    email           = db.Column(db.String(255), unique=True, nullable=False)
    password        = db.Column(db.String(255), nullable=False)
    category        = db.Column(db.Enum('0', '1'), nullable=False)
    
    records         = db.relationship("Record", back_populates="user")  # Corrected relationship


class Question(db.Model):
    __tablename__   = 'question'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content         = db.Column(db.Text, nullable=False)


class Record(db.Model):
    __tablename__ = 'record'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    v_name          = db.Column(db.String(255))  # Video name "username_qid_v"
    a_name          = db.Column(db.String(255))  # Audio name "username_qid_a"
    date            = db.Column(db.DateTime, default=db.func.current_timestamp())
    summary         = db.Column(db.Text, nullable=False)  # Store the summary

    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    
    qid             = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  # Foreign key to question
    
    user            = db.relationship("User", back_populates="records")
    question        = db.relationship("Question", backref="records")  # Establishing proper relationship


class FaceAnalysis(db.Model):
    __tablename__ = 'face_analysis'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    happy           = db.Column(db.Float, default=0.0)
    sad             = db.Column(db.Float, default=0.0)
    angry           = db.Column(db.Float, default=0.0)
    calm            = db.Column(db.Float, default=0.0)
    fear            = db.Column(db.Float, default=0.0)
    smile           = db.Column(db.Float, default=0.0)
    
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id     = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    user            = db.relationship("User", backref="face_analyses")
    question        = db.relationship("Question", backref="face_analyses")


class VoiceAnalysis(db.Model):
    __tablename__ = 'voice_analysis'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    question_id     = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    transcript      = db.Column(db.String(255), nullable=False)
    mixed           = db.Column(db.Float, default=0.0)
    negative        = db.Column(db.Float, default=0.0)
    neutral         = db.Column(db.Float, default=0.0)
    positive        = db.Column(db.Float, default=0.0)
    
    user            = db.relationship("User", backref="voice_analyses")
    question        = db.relationship("Question", backref="voice_analyses")
