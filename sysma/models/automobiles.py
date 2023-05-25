from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime


from config import Base


class Automobiles(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    placa = Column(String, unique=True)
    renavam = Column(String)
    chassi = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
