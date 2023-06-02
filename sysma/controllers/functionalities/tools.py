import re


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

if __name__ == "__main__":
    placa = "DMW6133"

    print(plate_convert(placa))
    

