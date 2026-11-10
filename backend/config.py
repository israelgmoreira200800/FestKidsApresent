import os
from pathlib import Path

from dotenv import load_dotenv


PASTA_BACKEND = Path(__file__).parent
load_dotenv(PASTA_BACKEND / ".env.local")


class Configuracao:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FRONTEND_ORIGINS = [
        origem.strip()
        for origem in os.getenv(
            "FRONTEND_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500",
        ).split(",")
        if origem.strip()
    ]
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "1000000"))
