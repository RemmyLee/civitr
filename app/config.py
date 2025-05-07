import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///models.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODELS_PER_PAGE = 24
    IMAGES_PER_PAGE = 24
    CREATORS_PER_PAGE = 24
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')