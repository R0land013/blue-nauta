from ..entity.entity import UserCredential
from cryptography.fernet import Fernet
from ..database.credential_repository import CredentialRepository
from model.database.util import create_database
from typing import List, Tuple


class CredentialManager:

    def __init__(self):
        create_database()
        self.__credential_repo = CredentialRepository()

    def get_credentials(self) -> List[UserCredential]:
        encrypted_credentials = self.__credential_repo.get_all_credentials()

        credentials_to_return = []
        for an_encrypted_credential in encrypted_credentials:
            decrypted_credential = UserCredential()

            decrypted_credential.id = an_encrypted_credential.id
            decrypted_credential.username = self.__decrypt(
                an_encrypted_credential.username, an_encrypted_credential.username_key)

            decrypted_credential.password = self.__decrypt(
                an_encrypted_credential.password, an_encrypted_credential.password_key)

            decrypted_credential.is_default = an_encrypted_credential.is_default
            credentials_to_return.append(decrypted_credential)

        return credentials_to_return

    def __decrypt(self, encrypted_string: str, encryption_key: str):
        fernet = Fernet(encryption_key)
        return fernet.decrypt(encrypted_string.encode()).decode()

    def save_username_and_password(self, username, password):
        encrypted_username, username_key = self.__encrypt(username)
        encrypted_password, password_key = self.__encrypt(password)

        new_user_credential = UserCredential(username=encrypted_username,
                                             username_key=username_key,
                                             password=encrypted_password,
                                             password_key=password_key,
                                             is_default=False)

        self.__credential_repo.add_user_credential(new_user_credential)

    def __encrypt(self, a_string: str) -> Tuple[str, str]:
        encoded_key = Fernet.generate_key()
        fernet = Fernet(encoded_key)
        encrypted_string = fernet.encrypt(a_string.encode()).decode()
        decoded_key = encoded_key.decode()

        return (encrypted_string, decoded_key)

    def set_account_as_default(self, account: UserCredential):
        self.__credential_repo.set_user_credential_as_default(account)

    def clear_default_credentials(self):
        self.__credential_repo.set_not_default_all_credentials()

    def get_default_credential(self) -> UserCredential:
        encrypted_account = self.__credential_repo.get_default_credential()

        if encrypted_account:
            default_account = UserCredential()
            default_account.id = encrypted_account.id
            default_account.username = self.__decrypt(
                encrypted_account.username, encrypted_account.username_key)
            default_account.password = self.__decrypt(
                encrypted_account.password, encrypted_account.password_key)
            return default_account

        return None

    def update_credential(self, credential: UserCredential):
        encrypted_username, username_key = self.__encrypt(credential.username)
        encrypted_password, password_key = self.__encrypt(credential.password)

        updated_credential = UserCredential(
            id=credential.id,
            username=encrypted_username,
            username_key=username_key,
            password=encrypted_password,
            password_key=password_key)

        self.__credential_repo.update_credential(updated_credential)
    
    def delete_credential(self, credential_id: int):
        self.__credential_repo.delete_credential(credential_id)
