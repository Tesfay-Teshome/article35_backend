import os

db_URL = os.getenv('DATABASE_URL', 'postgres://localhost:5001/article35_db')
secret = os.getenv('SECRET', 'thisisarticle35_dbsecretkey.')