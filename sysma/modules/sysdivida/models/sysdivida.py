
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from config import Base


class SysDividaHistory(Base):
    __tablename__ = "sysdividahistory"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Projects")



class SysDividaData(Base):
    __tablename__ = "sysdividadata"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey("sysdividahistory.id"), nullable=False)
    
    placa = Column(String)
    renavam = Column(String)
    
    lote = Column(Integer)
    valor = Column(Float)
    ait = Column(String)
    guia = Column(String)
    debito = Column(String)


    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    sysdividahistory = relationship("SysDividaHistory")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    