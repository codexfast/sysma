from config import *
from sqlalchemy.orm import Session
from controllers.functionalities.tools import plate_convert


with Session(DB_ENGINE) as session:

    # last_history = session.query(SysplHistory).order_by(SysplHistory.id.desc()).first()
    last_history = session.query(SysplHistory).filter(SysplHistory.project_id == 6).order_by(SysplHistory.id.desc()).first()

    print(last_history)
