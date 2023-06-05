from config import DB_ENGINE, SysplData, SysplLogin
from sqlalchemy.orm import Session
from controllers.functionalities.tools import plate_convert

with Session(DB_ENGINE) as session:

    login_syspl:SysplLogin = session.query(SysplLogin).one_or_none()

    if login_syspl:
        print(login_syspl.id)