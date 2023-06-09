import re
import typing

def is_plate(str: str) -> bool:
    placa = re.compile("^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$")

    if len(placa.findall(str)):
        return True
    
    return False

def is_mercosul(placa: str) -> bool:
    placa_mercosul = re.compile("^[a-zA-Z]{3}[0-9][A-Za-z][0-9]{2}$")

    if len(placa_mercosul.findall(placa)):
        return True
    
    return False

def plate_convert(placa: str) -> str:

    if not is_plate(placa): return placa

    rule_normal = {
        "A":"0",
        "B":"1",
        "C":"2",
        "D":"3",
        "E":"4",
        "F":"5",
        "G":"6",
        "H":"7",
        "I":"8",
        "J":"9",
    }

    rule_mercosul = {
        "0":"A",
        "1":"B",
        "2":"C",
        "3":"D",
        "4":"E",
        "5":"F",
        "6":"G",
        "7":"H",
        "8":"I",
        "9":"J",
    }

    p = list(placa)

    if is_mercosul(placa):

        # transforma em placa normal
        p[4] = rule_normal[p[4].upper()]

        return "".join(p)

    # transforma em placa mercosul
    p[4] = rule_mercosul[p[4]]

    return "".join(p)


def compare(_iterator1, _iterator2):
    
    if len(_iterator1) == len(_iterator2):
        if not False in list(map(lambda i: i in _iterator1, _iterator2)):
            return True
    
    return False

def selecionar_contas(montante: float, contas_por_data:typing.List[typing.Dict]) -> typing.List:

    selecionadas = []
    
    for conta in contas_por_data:
        if conta['value'] <= montante:  # se a conta puder ser paga com o montante restante
            selecionadas.append(conta)  # adiciona a conta às selecionadas
            montante -= conta['value']  # subtrai a quantia da conta do montante restante
        if montante == 0:  # se não há mais dinheiro restante
            break  # interrompe a seleção de contas
    return selecionadas