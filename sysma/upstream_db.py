import sqlalchemy
import datetime
import uuid

from config import DB_ENGINE as SQLITE_ENGINE

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError

from models.projects import Projects
from models.automobiles import Automobiles

from modules.sysdivida.models.sysdivida import *
from modules.sysfazenda.models.sysfazenda import *
from modules.syspl.models.syspl import *

Base = declarative_base()

def get_hex_mac_address():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

def get_mac_address():
    return uuid.getnode()

class ProjectsMS(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    mac_address_pc = Column(String(64), default=get_mac_address)
    signature = Column(String(64), nullable=False, unique=True)
    name = Column(String(32), nullable=False)
    leiloeiro = Column(String(32), nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=False)
    patio = Column(String(64), nullable=False)
    finished_at = Column(DateTime(timezone=True))
    estado = Column(String(16))
    endereco = Column(String(64))
    cidade = Column(String(32))
    descricao = Column(String(4096))

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>" 

class AutomobilesMS(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("projects.signature"), nullable=False)

    
    placa = Column(String(16))
    placa_mercosul = Column(String(16))
    renavam = Column(String(16))
    chassi = Column(String(16))

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("ProjectsMS")

class SysplHistoryMS(Base):
    __tablename__ = "sysplhistory"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("projects.signature"), nullable=False)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("ProjectsMS")

class SysplDataMS(Base):
    __tablename__ = "syspldata"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("sysplhistory.signature"), nullable=False)
    
    placa = Column(String(16), default=None)
    renavam = Column(String(16), default=None)
    chassi = Column(String(16), default=None)

    finaceira_nome = Column(String(32), default=None)
    finaceira_vigencia_do_contrato = Column(String(128), default=None)
    dados_veiculo_restricao_1 = Column(String(128), default=None)
    comun_venda_data_da_inclusao = Column(String(128), default=None)
    dados_veiculo_bloqueio_de_guincho = Column(String(128), default=None)
    dados_veiculo_ultimo_licenciamento = Column(String(128), default=None)
    
    bloqueio_1_tipo = Column(String(128), default=None)
    bloqueio_1_data_inclusao = Column(String(128), default=None)
    bloqueio_1_descricao = Column(String(128), default=None)

    bloqueio_2_tipo = Column(String(128), default=None)
    bloqueio_2_data_inclusao = Column(String(128), default=None)
    bloqueio_2_descricao = Column(String(128), default=None)
    
    bloqueio_3_tipo = Column(String(128), default=None)
    bloqueio_3_data_inclusao = Column(String(128), default=None)
    bloqueio_3_descricao = Column(String(128), default=None)
    
    bloqueio_4_tipo = Column(String(128), default=None)
    bloqueio_4_data_inclusao = Column(String(128), default=None)
    bloqueio_4_descricao = Column(String(128), default=None)

    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    sysplhistory = relationship("SysplHistoryMS")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
class SysFazendaHistoryMS(Base):
    __tablename__ = "sysfazendahistory"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("projects.signature"), nullable=False)

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("ProjectsMS")

class SysFazendaDataMS(Base):
    __tablename__ = "sysfazendadata"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("sysfazendahistory.signature"), nullable=False)


    placa = Column(String(16))
    renavam = Column(String(16))
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

    sysfazendahistory = relationship("SysFazendaHistoryMS")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"

class SysDividaHistoryMS(Base):
    __tablename__ = "sysdividahistory"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("projects.signature"), nullable=False)


    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    project = relationship("ProjectsMS")

class SysDividaDataMS(Base):
    __tablename__ = "sysdividadata"

    id = Column(Integer, primary_key=True)
    signature = Column(String(64), nullable=False, unique=True)
    parent_signature = Column(String(64), ForeignKey("sysdividahistory.signature"), nullable=False)


    placa = Column(String(16))
    renavam = Column(String(16))
    
    lote = Column(Integer)
    valor = Column(Float)
    ait = Column(String(16))
    guia = Column(String(16))
    debito = Column(String(16))


    failed = Column(Boolean, default=False)
    
    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    sysdividahistory = relationship("SysDividaHistoryMS")


    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"

class UpstreamDatabase:
    ENGINE = sqlalchemy.create_engine("mysql+pymysql://dbmasteruser:YNy!,)j|xo,QH6iSveOJn~JrP?6MxESY@ls-5d28a98e46d7000be4f11b277403773aef805312.cznbjserm8wq.us-east-1.rds.amazonaws.com/sysma")

    def __init__(self) -> None:
        # cria caso nao exista as tabelas
        Base.metadata.create_all(self.ENGINE)        

    # obtem dados do banco baseado em sqlite
    def get_data(self):

        data = {}

        with Session(SQLITE_ENGINE) as session:

            data['projects'] = session.query(Projects).all()
            data['automobiles'] = session.query(Automobiles).all()
            data['sysplhistory'] = session.query(SysplHistory).all()
            data['syspldata'] = session.query(SysplData).all()
            data['sysfazendahistory'] = session.query(SysFazendaHistory).all()
            data['sysfazendadata'] = session.query(SysFazendaData).all()
            data['sysdividahistory'] = session.query(SysDividaHistory).all()
            data['sysdividadata'] = session.query(SysDividaData).all()
            

        return data
            
    def upstream(self, callback: None):
        data = self.get_data()

        with Session(self.ENGINE) as session:

            def custom_commit(instance:list):
                for i in instance:
                    session.add(i)
                    
                    try:
                        session.commit()
                    except IntegrityError as err:
                        
                        if 'Duplicate entry' in err.orig.args[1]:
                            
                            print(f"{i.__tablename__} com registro duplicado")

                        session.rollback()
                        

            projects: list[ProjectsMS] = [
                ProjectsMS(
                    signature=_.signature,
                    name=_.name,
                    leiloeiro=_.leiloeiro,
                    date_start=_.date_start,
                    patio=_.patio,
                    finished_at=_.finished_at,
                    estado=_.estado,
                    endereco=_.endereco,
                    cidade=_.cidade,
                    descricao=_.descricao,
                ) for _ in data.get('projects')
            ]

            sysplhistory: list[SysplHistoryMS] = [
                SysplHistoryMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,
                    time_created=_.time_created
                ) for _ in data.get('sysplhistory')
            ]

            sysfazendahistory: list[SysFazendaHistoryMS] = [
                SysFazendaHistoryMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,
                    time_created=_.time_created
                ) for _ in data.get('sysfazendahistory')
            ]

            sysdividahistory: list[SysDividaHistoryMS] = [
                SysDividaHistoryMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,
                    time_created=_.time_created
                ) for _ in data.get('sysdividahistory')
            ]

            syspldata: list[SysplDataMS] = [
                SysplDataMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,
                    
                    placa=_.placa,
                    renavam=_.renavam,
                    chassi=_.chassi,

                    finaceira_nome=_.finaceira_nome,
                    finaceira_vigencia_do_contrato=_.finaceira_vigencia_do_contrato,
                    dados_veiculo_restricao_1=_.dados_veiculo_restricao_1,
                    comun_venda_data_da_inclusao=_.comun_venda_data_da_inclusao,
                    dados_veiculo_bloqueio_de_guincho=_.dados_veiculo_bloqueio_de_guincho,
                    dados_veiculo_ultimo_licenciamento=_.dados_veiculo_ultimo_licenciamento,

                    bloqueio_1_tipo=_.bloqueio_1_tipo,
                    bloqueio_1_data_inclusao=_.bloqueio_1_data_inclusao,
                    bloqueio_1_descricao=_.bloqueio_1_descricao,

                    bloqueio_2_tipo=_.bloqueio_2_tipo,
                    bloqueio_2_data_inclusao=_.bloqueio_2_data_inclusao,
                    bloqueio_2_descricao=_.bloqueio_2_descricao,

                    bloqueio_4_tipo=_.bloqueio_4_tipo,
                    bloqueio_4_data_inclusao=_.bloqueio_4_data_inclusao,
                    bloqueio_4_descricao=_.bloqueio_4_descricao,

                    bloqueio_3_tipo=_.bloqueio_3_tipo,
                    bloqueio_3_data_inclusao=_.bloqueio_3_data_inclusao,
                    bloqueio_3_descricao=_.bloqueio_3_descricao,
                    
                    failed=_.failed,

                    time_created=_.time_created
                ) for _ in data.get('syspldata')
            ]

            sysfazendadata: list[SysFazendaDataMS] = [
                SysFazendaDataMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,

                    placa=_.placa,
                    renavam=_.renavam,
                    multa_renainf=_.multa_renainf,
                    ipva=_.ipva,
                    divida_ativa=_.divida_ativa,
                    multas_detran=_.multas_detran,
                    outras_multas=_.outras_multas,
                    dpvat=_.dpvat,
                    taxa_licenciamento=_.taxa_licenciamento,


                    failed=_.failed,

                    time_created=_.time_created
                ) for _ in data.get('sysfazendadata')
            ]

            sysdividadata: list[SysDividaDataMS] = [
                SysDividaDataMS(
                    signature=_.signature,
                    parent_signature=_.parent_signature,

                    placa=_.placa,
                    renavam=_.renavam,
                    
                    lote=_.lote,
                    valor=_.valor,
                    ait=_.ait,
                    guia=_.guia,
                    debito=_.debito,
                    
                    failed=_.failed,

                    time_created=_.time_created
                ) for _ in data.get('sysdividadata')
            ]


            custom_commit(projects)

            custom_commit(sysplhistory)
            custom_commit(sysfazendahistory)
            custom_commit(sysdividahistory)

            custom_commit(syspldata)
            custom_commit(sysfazendadata)
            custom_commit(sysdividadata)

            if callback:
                callback()


# s = UpstreamDatabase()
# s.upstream()



# p = ProjectsMS(
#     signature="asd",
#     name="Teste I",
#     leiloeiro="Teste",
#     date_start="2023-06-01 00:00:00.000000",
#     patio="Teste"
# )

# print(p)