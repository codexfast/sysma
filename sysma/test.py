        
import config
from sqlalchemy.orm import Session
from modules.syspl.models.syspl import SysplData


with Session(config.DB_ENGINE) as session:
    sdata = session.query(SysplData).filter(SysplData.history_id==1).all()