from sqlalchemy import create_engine
from ..entity.entity import Base

DB_URL = 'sqlite:///data.db?check_same_thread=False'

def create_database():
    engine = create_engine(DB_URL, echo=False, future=True)
    Base.metadata.create_all(engine)

