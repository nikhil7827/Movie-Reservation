import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/movie_reservation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
