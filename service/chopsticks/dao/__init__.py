from typing import Any

from chopsticks.dao.abstract_dao import AbstractDAO
from chopsticks.dao.passthrough_dao import PassthroughDAO
from chopsticks.dao.sqlite_dao import SQLiteDAO

DAO = {
    "passthrough": PassthroughDAO,
    "sqlite": SQLiteDAO
}

def get_dao(dao_name: str, *args: Any, **kwargs: Any) -> AbstractDAO:
    dao_class = DAO.get(dao_name, PassthroughDAO)
    return dao_class(*args, **kwargs)
