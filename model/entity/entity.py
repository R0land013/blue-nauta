from sqlalchemy import Column
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserCredential(Base):
    # This table is used for storing encrypted user credentials
    
    def __repr__(self) -> str:
        return f'{self.username} {self.password}'
    
    def __str__(self) -> str:
        return self.__repr__()

    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False)
    username_key = Column(String(200))
    password = Column(String(200), nullable=False)
    password_key = Column(String(200))
    is_default = Column(Boolean, nullable=False)