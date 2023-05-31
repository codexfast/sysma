from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, Boolean

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from config import Base


class SysplHistory(Base):
    __tablename__ = "sysplhistory"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Projects")



class SysplData(Base):
    __tablename__ = "syspldata"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey("sysplhistory.id"), nullable=False)
    
    placa = Column(String, default=None)
    finaceira_nome = Column(String, default=None)
    finaceira_vigencia_do_contrato = Column(String, default=None)
    dados_veiculo_restricao_1 = Column(String, default=None)
    comun_venda_data_da_inclusao = Column(String, default=None)
    dados_veiculo_bloqueio_de_guincho = Column(String, default=None)
    dados_veiculo_ultimo_licenciamento = Column(String, default=None)
    
    bloqueio_1_tipo = Column(String, default=None)
    bloqueio_1_data_inclusao = Column(String, default=None)
    bloqueio_1_descricao = Column(String, default=None)

    bloqueio_2_tipo = Column(String, default=None)
    bloqueio_2_data_inclusao = Column(String, default=None)
    bloqueio_2_descricao = Column(String, default=None)
    
    bloqueio_3_tipo = Column(String, default=None)
    bloqueio_3_data_inclusao = Column(String, default=None)
    bloqueio_3_descricao = Column(String, default=None)
    
    bloqueio_4_tipo = Column(String, default=None)
    bloqueio_4_data_inclusao = Column(String, default=None)
    bloqueio_4_descricao = Column(String, default=None)

    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    sysplhistory = relationship("SysplHistory")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    

class SysplLogin(Base):
    __tablename__ = "syspllogin"

    id = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)

