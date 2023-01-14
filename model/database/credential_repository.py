from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from sqlalchemy.pool import NullPool
from ..entity.entity import UserCredential
from ..database.util import DB_URL
from typing import List


class CredentialRepository:

    __session: Session = None

    def add_user_credential(self, credential: UserCredential):
        with self.__create_session() as session:
            session.add(credential)
            session.commit()

    def __create_session(self):
        engine = create_engine(DB_URL, poolclass=NullPool)
        return Session(engine)

    def get_all_credentials(self) -> List[UserCredential]:
        with self.__create_session() as session:
            return session.scalars(select(UserCredential)).all()
