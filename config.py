import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://nms_user:vayvanna@localhost/nms_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# This file just holds your connection URL (and maybe other settings):