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
    
    records         = db.relationship('Record', backref='user_record', lazy=True)
    face_analyses   = db.relationship('FaceAnalysis', backref='user_face', lazy=True)
    voice_analyses  = db.relationship('VoiceAnalysis', backref='user_voice', lazy=True)


class Question(db.Model):
    __tablename__   = 'question'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content         = db.Column(db.Text, nullable=False)


class Record(db.Model):
    __tablename__ = 'record'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # use user_id instead of username
    v_name          = db.Column(db.String(255))  # Video name "username_qid_v"
    a_name          = db.Column(db.String(255))  # Audio name "username_qid_a"
    date            = db.Column(db.DateTime, default=db.func.current_timestamp())
    summary         = db.Column(db.Text, nullable=False)  # Store the summary

    user            = db.relationship('User', backref='record_user', lazy=True)
    qid             = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  # Foreign key to question
    question        = db.relationship('Question', backref='record_qid', lazy=True)  # relationship to Question

class FaceAnalysis(db.Model):
    __tablename__ = 'face_analysis'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # use user_id instead of username
    question_id     = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    happy           = db.Column(db.Float, default=0.0)
    sad             = db.Column(db.Float, default=0.0)
    angry           = db.Column(db.Float, default=0.0)
    calm            = db.Column(db.Float, default=0.0)
    fear            = db.Column(db.Float, default=0.0)
    smile           = db.Column(db.Float, default=0.0)
    
    user            = db.relationship('User', backref='face_analysis', lazy=True)
    question        = db.relationship('Question', backref='face_analysis_question', lazy=True)

class VoiceAnalysis(db.Model):
    __tablename__ = 'voice_analysis'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # use user_id instead of username
    question_id     = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    transcript      = db.Column(db.String(255), nullable=False)
    mixed           = db.Column(db.Float, default=0.0)
    negative        = db.Column(db.Float, default=0.0)
    neutral         = db.Column(db.Float, default=0.0)
    positive        = db.Column(db.Float, default=0.0)
    
    user            = db.relationship('User', backref='voice_analysis', lazy=True)
    question        = db.relationship('Question', backref='voice_analysis', lazy=True)
