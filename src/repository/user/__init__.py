from typing import TYPE_CHECKING

from src.database.models import UsersOrm

from .methods import Methods
from .properties import Properties


if TYPE_CHECKING:
    from src.repository import Crud


class User(Methods, Properties):

    def __init__(self, crud: "Crud", obj: UsersOrm):
        self.crud = crud
        self.session = crud.session
        self.obj = obj
