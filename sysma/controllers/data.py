import config
import typing
import dataclasses
from dataclasses import field

from sqlalchemy.orm import Session
from models.automobiles import Automobiles

@dataclasses.dataclass
class Resources:

    __autos: typing.List[Automobiles] = field(init=False, repr=False)

    def __post_init__(self):
        with Session(config.DB_ENGINE) as session:
            self.__autos = session.query(Automobiles).all()


    def get_autos(self) -> typing.Generator:
        for a in self.__autos:
            yield a

    def __len__(self) -> int:
        return len(self.__autos)
    
    