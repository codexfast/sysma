
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime

from config import Base


class SysFazendaHistory(Base):
    __tablename__ = "sysfazendahistory"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("Projects")



class SysFazendaData(Base):
    __tablename__ = "sysfazendadata"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey("sysfazendahistory.id"), nullable=False)
    placa = Column(String)
    renavam = Column(String)
    multa_renainf = Column(Float)
    ipva = Column(Float)
    divida_ativa = Column(Float)
    multas_detran = Column(Float)
    outras_multas = Column(Float)
    dpvat = Column(Float)
    taxa_licenciamento = Column(Float)

    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    sysfazendahistory = relationship("SysFazendaHistory")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    


class SysFazendalConfig(Base):
    __tablename__ = "sysfazendaconfig"

    id = Column(Integer, primary_key=True)

    anti_captcha_key = Column(String)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)
    
