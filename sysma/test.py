from config import DB_ENGINE, SysplData
from sqlalchemy.orm import Session
from controllers.functionalities.tools import plate_convert

with Session(DB_ENGINE) as session:
    failed = \
        session.query(SysplData).filter(
            SysplData.history_id == 1, SysplData.failed == True
        ).all()
    
    for f in failed:
        print(i.finaceira_nome)

    # for i in failed:
    #     i.finaceira_nome = "teste"

    # session.commit()