from config import DB_ENGINE, SysplData
from sqlalchemy.orm import Session
from controllers.functionalities.tools import plate_convert

with Session(DB_ENGINE) as session:
    failed = \
        session.query(SysplData).filter(
            SysplData.history_id == 1, SysplData.failed == True
        ).all()
    
    for f in failed:
        print(f.finaceira_nome)

    for i in failed:
        i.placa=""
        i.finaceira_nome=""
        i.finaceira_vigencia_do_contrato=""
        i.dados_veiculo_restricao_1=""
        i.comun_venda_data_da_inclusao=""
        i.dados_veiculo_bloqueio_de_guincho=""
        i.dados_veiculo_ultimo_licenciamento=""

        i.bloqueio_1_tipo = ""
        i.bloqueio_1_data_inclusao = ""
        i.bloqueio_1_descricao = ""

        i.bloqueio_2_tipo = ""
        i.bloqueio_2_data_inclusao = ""
        i.bloqueio_2_descricao = ""

        i.bloqueio_3_tipo = ""
        i.bloqueio_3_data_inclusao = ""
        i.bloqueio_3_descricao = ""

        i.bloqueio_4_tipo = ""
        i.bloqueio_4_data_inclusao = ""
        i.bloqueio_4_descricao = ""

    session.commit()