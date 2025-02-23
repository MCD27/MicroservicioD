from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://universidaddb_user:tBJNxMWU2oP9VwDAnLToB69gGCM1RCYX@dpg-cut7rbogph6c73b0hs8g-a/universidaddb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

