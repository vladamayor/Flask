import os
from atexit import register

from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "Room48320785")
PG_DB = os.getenv("PG_DB", "app")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5431)


PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(PG_DSN)

register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisements(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, server_default=func.now())
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)


Base.metadata.create_all()
