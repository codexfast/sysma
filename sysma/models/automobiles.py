import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime
from controllers.functionalities.tools import create_signature


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from config import Base


class Automobiles(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    signature = Column(String, nullable=False, default=create_signature)
    parent_signature = Column(String, nullable=False)
    
    placa = Column(String)
    placa_mercosul = Column(String)
    renavam = Column(String)
    chassi = Column(String)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("Projects")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
