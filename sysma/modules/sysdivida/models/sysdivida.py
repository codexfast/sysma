
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from controllers.functionalities.tools import create_signature



from config import Base

import datetime


class SysDividaHistory(Base):
    __tablename__ = "sysdividahistory"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    signature = Column(String, nullable=False, default=create_signature)
    parent_signature = Column(String, nullable=False)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("Projects")



class SysDividaData(Base):
    __tablename__ = "sysdividadata"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey("sysdividahistory.id"), nullable=False)
    signature = Column(String, nullable=False, default=create_signature)
    parent_signature = Column(String, nullable=False)
    
    placa = Column(String)
    renavam = Column(String)
    
    lote = Column(Integer)
    valor = Column(Float)
    ait = Column(String)
    guia = Column(String)
    debito = Column(String)


    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    sysdividahistory = relationship("SysDividaHistory")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    