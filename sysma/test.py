# from controllers.functionalities.tools import compare
# from controllers.core.xlsx import Xlsx
# from sqlalchemy.orm import Session

# from config import *

# class LoadDividaAssets(Xlsx):
#     def __init__(self, xlsx_file):
#         super().__init__(xlsx_file)

#         # Recursos carregados da planilha
#         self.resources = list(self.ws.iter_rows(values_only=True))

#     def _verify(self, asset: tuple) -> bool:
#         lote, placa, renavam, valor = asset

#         if not None in (lote, placa, renavam, valor) :
#             return True
        
#         return False

#     def get(self) -> list:
#         return list(filter(self._verify, self.resources))


# def check_input_dividas(filepath, syspl_data):

#     raw_ = LoadDividaAssets(filepath).get()
#     del raw_[0]

#     assets_divida = [(a[1], a[2],)for a in raw_]
#     syspl_data = [(s.placa, s.renavam) for s in syspl_data]

#     return compare(assets_divida, syspl_data)

# with Session(DB_ENGINE) as session:
            
#     last_history = session.query(SysplHistory).filter(SysplHistory.project_id == 1).order_by(SysplHistory.id.desc()).first()

#     syspl_data = \
#         session.query(SysplData)\
#             .filter(SysplData.history_id == last_history.id, SysplData.failed == False).all()\
#                     if not last_history is None else []
    
#     print(check_input_dividas(r"C:\Users\Gilberto\Desktop\08-06-2023.15-29-54.DVIDAS_PREENCHIMENTO.v2.xlsx", syspl_data))


# a = [
#     (1, "ASD4324", "123RA314", 19992.34),
#     (2, "FGH4324", "756RA314", 7567),
# ]

# for lote, placa, renavam, saldo in a:
    
#     if placa.upper() == "ASD4324":
#         print(saldo)

import datetime

print(datetime.datetime.now())