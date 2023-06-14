import datetime

from sqlalchemy.sql import func
from sqlalchemy import Column, Boolean, Integer, DateTime


from config import Base


class GeneralSettings(Base):
    __tablename__ = "generalsettings"

    id = Column(Integer, primary_key=True)
    headless_mode = Column(Boolean, nullable=False)
    

    time_created = Column(DateTime(timezone=True), default=datetime.datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)

    def __repr__(self):
        return f"<{self.__tablename__.capitalize()}>"
    
