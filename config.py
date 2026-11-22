import os
from sqlalchemy import URL

class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "student_db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    