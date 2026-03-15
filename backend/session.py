from sqlalchemy.orm import sessionmaker
from dbengine import engine

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
