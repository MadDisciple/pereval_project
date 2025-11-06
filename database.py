from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


class Base(DeclarativeBase):
    pass

def get_db():
    if not settings.DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not set.")

    try:
        engine = create_engine(settings.DATABASE_URL, echo=True)

        Base.metadata.create_all(bind=engine)

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Connection Error: {e}")

    try:
        yield db
    finally:
        db.close()