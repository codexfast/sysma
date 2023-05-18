from .xlsx import Xlsx
from model.automobiles import Automobiles

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import Delete, select

import typing
import config


class LoadSysmaResource(Xlsx):

    def __init__(self, xlsx_file):
        super().__init__(xlsx_file)

        with Session(config.DB_ENGINE) as session:
            
            # contanto os recursos
            self.count_resources = session.query(Automobiles).count()            

        self.valid_resources, \
            self.invalid_resources = self.__verify_xlsx()

    def __verify_xlsx(self) -> typing.Tuple[typing.List[typing.Tuple]]:

        """
        Verifica os recursos validos e invalidos
        retornado lista paras os mesmos
        """


        def resource_valid(resource):
            assert len(resource) >= 3, "Verifique a planilha de entrada de dados"

            placa, renavam, chassi = resource

            if placa:
                if renavam or chassi:
                    return True
                
            return False


        # Recursos carregados da planilha
        resources = list(self.ws.iter_rows(values_only=True))
        
        # apagando primeira linhas pois será os titulos da planilha padronizada
        del resources[0]

        # Verifica e armazena recursos válidos e inválidos
        valid = list(filter(resource_valid, resources))
        invalid = list(value for value in resources if value not in valid)
        

        return (valid, invalid)

    def record_resources(self):

        assert len(self.valid_resources) > 0, "Não há recursos para gravar"


        with Session(config.DB_ENGINE) as session, session.begin():

            # limpa tudo antes dos novos dados
            session.execute(Delete(Automobiles))

            # inserido novos dados validos
            autos = [Automobiles(
                placa=placa,
                renavam=renavam,
                chassi=chassi,
            ) for (placa, renavam, chassi) in self.valid_resources]

            session.add_all(autos)


    def merge_resources(self) -> typing.List[typing.Tuple]:
        
        assert len(self.valid_resources) > 0, "Não há recursos para gravar"

                    
        with Session(config.DB_ENGINE) as session:

            # inserido novos dados não repetidos

            insert_err = []

            for (placa, renavam, chassi) in self.valid_resources:

                try:
                    with session.begin():

                        session.add(
                            Automobiles(
                                placa=placa,
                                renavam=renavam,
                                chassi=chassi,
                            )
                        )

                    
                except IntegrityError:

                    insert_err.append((placa, renavam, chassi))
                    session.rollback()
        
        return insert_err