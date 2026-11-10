import os
from pathlib import Path

from dotenv import load_dotenv


PASTA_BACKEND = Path(__file__).parent
load_dotenv(PASTA_BACKEND / ".env.local")


class Configuracao:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
