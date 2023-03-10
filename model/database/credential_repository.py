from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update, delete
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

    def set_user_credential_as_default(self, credential: UserCredential):
        with self.__create_session() as session:
            
            # set the default credential
            session.execute(
                update(UserCredential)
                .where(UserCredential.id == credential.id)
                .values(is_default=True))
            
            # set not default the others credentials
            session.execute(
                update(UserCredential)
                .where(UserCredential.id != credential.id)
                .values(is_default=False))
            
            session.commit()
    
    def set_not_default_all_credentials(self):
        with self.__create_session() as session:
            
            session.execute(
                update(UserCredential)
                .values(is_default=False))
            session.commit()
    
    def get_default_credential(self) -> UserCredential:
        with self.__create_session() as session:
            
            default_credential = session.scalar(
                select(UserCredential)
                .where(UserCredential.is_default == True))
            
            return default_credential

    def update_credential(self, credential: UserCredential):
        with self.__create_session() as session:

            session.execute(
                update(UserCredential)
                .where(UserCredential.id == credential.id)
                .values(
                    username=credential.username,
                    username_key=credential.username_key,
                    password=credential.password,
                    password_key=credential.password_key)
            )
            session.commit()
    
    def delete_credential(self, credential_id: int):
        with self.__create_session() as session:

            session.execute(
                delete(UserCredential)
                .where(UserCredential.id == credential_id)
            )
            session.commit()