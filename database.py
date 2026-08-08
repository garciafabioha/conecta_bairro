import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# ---------------------------------------------------------
# AMBIENTE STREAMLIT CLOUD / NEON
# ---------------------------------------------------------

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if DB_HOST and DB_NAME and DB_USER and DB_PASSWORD:

    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        query={
            "sslmode": "require",
        },
    )

else:

    # -----------------------------------------------------
    # AMBIENTE LOCAL
    # -----------------------------------------------------

    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise RuntimeError(
            "Configuração do banco de dados não encontrada."
        )

# ---------------------------------------------------------
# ENGINE
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

# ---------------------------------------------------------
# SESSÃO
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# ---------------------------------------------------------
# BASE DOS MODELS
# ---------------------------------------------------------

class Base(DeclarativeBase):
    pass