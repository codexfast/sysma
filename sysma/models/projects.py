from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime


from config import Base


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    leiloeiro = Column(String, nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=False)
    patio = Column(String, nullable=False)
    finished_at = Column(DateTime(timezone=True))
    estado = Column(String)
    endereco = Column(String)
    cidade = Column(String)
    descricao = Column(String)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
