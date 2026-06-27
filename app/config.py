import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # Phase 3 uses a Supabase Postgres connection string here.
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    ).replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional future integration settings.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY", "")
    IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
    IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT", "")

    @classmethod
    def missing_current_values(cls):
        required_names = [
            "SECRET_KEY",
        ]

        return [name for name in required_names if not os.getenv(name)]

    @classmethod
    def missing_phase3_values(cls):
        required_names = [
            "DATABASE_URL",
        ]

        return [name for name in required_names if not os.getenv(name)]
