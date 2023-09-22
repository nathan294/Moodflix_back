import os

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


class Settings:
    def __init__(self, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT):
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT


settings = Settings(
    DB_NAME=DB_NAME, DB_USER=DB_USER, DB_PASS=DB_PASS, DB_HOST=DB_HOST, DB_PORT=DB_PORT
)
