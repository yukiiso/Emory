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
    
    records         = db.relationship('Record', backref='user_record', lazy=True)
    face_analyses   = db.relationship('FaceAnalysis', backref='user_face', lazy=True)
    voice_analyses  = db.relationship('VoiceAnalysis', backref='user_voice', lazy=True)

class Question(db.Model):
    __tablename__   = 'question'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content         = db.Column(db.Text, nullable=False)
    
    face_analyses   = db.relationship('FaceAnalysis', backref='question_analysis', lazy=True)
    voice_analyses  = db.relationship('VoiceAnalysis', backref='question_voice', lazy=True)

class Record(db.Model):
    __tablename__ = 'record'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username        = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    v_name          = db.Column(db.String(255))  # Video name "username_qid_v"
    a_name          = db.Column(db.String(255))  # Audio name "username_qid_a"
    date            = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user            = db.relationship('User', backref='record_user', lazy=True)

class FaceAnalysis(db.Model):
    __tablename__ = 'face_analysis'
    
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username        = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
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
    username        = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    question_id     = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    speed           = db.Column(db.Float, default=0.0)
    pulse           = db.Column(db.Float, default=0.0)
    
    user            = db.relationship('User', backref='voice_analysis', lazy=True)
    question        = db.relationship('Question', backref='voice_analysis', lazy=True)