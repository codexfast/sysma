from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from config import Base


class Automobiles(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    placa = Column(String, unique=True)
    renavam = Column(String)
    chassi = Column(String)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Projects")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
