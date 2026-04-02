from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnimeModel(Base):
    __tablename__ = "anime_results"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    anime_type = Column(String)
    episodes = Column(String)
    rating = Column(String)
    score = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)