from sqlalchemy import create_engine
from ..entity.entity import Base
from pathlib import Path
import os


__BLUE_NAUTA_FOLDER_PATH = Path(os.path.join(str(Path.home()), '.blue-nauta/'))

if not __BLUE_NAUTA_FOLDER_PATH.exists():
    __BLUE_NAUTA_FOLDER_PATH.mkdir()

__BLUE_NAUTA_DB_PATH = str(os.path.join(str(__BLUE_NAUTA_FOLDER_PATH), 'data.db'))

DB_URL = f'sqlite:///{__BLUE_NAUTA_DB_PATH}?check_same_thread=False'

def create_database():
    engine = create_engine(DB_URL, echo=False, future=True)
    Base.metadata.create_all(engine)

