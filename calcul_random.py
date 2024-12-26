import random
import math

bareme = {
    "*": 5,
    "/": 6,
    "+": 3,
    "-": 4,
    "√": 10,
    "∛": 15,
    "^": 20,
    "%": 20,
}


class CalculRandom:
    def __init__(self, calcul1: str, resultat_calcul: int):
        self._calcul = calcul1
        self._resultat = resultat_calcul

    @property
    def calcul(self):
        return self._calcul

    @calcul.setter
    def calcul(self, value):
        self._calcul = value

    @property
    def resultat(self):
        return self._resultat

    @resultat.setter
    def resultat(self, value):
        self._resultat = value

    def point(self):
        if self._calcul[0] == "√":
            return math.sqrt(int(self._calcul[1:]))
        elif self._calcul[0] == "∛":
            return (int(self._calcul[1:])) ** (1 / 3)
        number1, operation, number2 = self._calcul.split(" ")
        point_total = bareme.get(operation)
        if self._resultat == eval(self._calcul):
            return point_total
        else:
            return 0


def generate_calcul():
    global calcul3, result
    operation = random.choice(list(bareme.keys()))
    if operation == "√":
        liste_perfect = [0, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121]
        number1 = random.choice(liste_perfect)
        calcul3 = f"√{number1}"
        result = round(math.sqrt(number1))
    elif operation == "∛":
        liste_perfect = [number ** 3 for number in range(1, 8)]
        number1 = random.choice(liste_perfect)
        calcul3 = f"∛{number1}"
        result = round(number1 ** (1 / 3))
    elif operation == "^":
        number1 = random.randint(1, 5)
        number2 = random.randint(1, 3)
        calcul3 = f"{number1} ^ {number2}"
        result = number1 ** number2
    elif operation == "%":
        number1 = random.randint(1, 100)
        number2 = random.randint(1, 100)
        if number2 == 0:
            number2 = 1
        if number1 == 0:
            number1 = 1
        if number2 > number1:
            number1, number2 = number2, number1
        calcul3 = f"{number1} % {number2}"
        result = number1 % number2
    elif operation == "+":
        number1 = random.randint(50, 100)
        number2 = random.randint(50, 100)
        calcul3 = f"{number1} + {number2}"
        result = number1 + number2
    elif operation == "-":
        number1 = random.randint(50, 100)
        number2 = random.randint(50, 100)
        if number2 > number1:
            number1, number2 = number2, number1
        calcul3 = f"{number1} - {number2}"
        result = number1 - number2
    elif operation == "*":
        number1 = random.randint(1, 10)
        number2 = random.randint(1, 10)
        calcul3 = f"{number1} * {number2}"
        result = number1 * number2
    elif operation == "/":
        number1 = random.randint(1, 10)
        number2 = random.randint(1, 10)
        if number2 == 0:
            number2 = 1
        if number1 == 0:
            number1 = 1
        if number2 > number1:
            number1, number2 = number2, number1
        if number1 % number2 != 0:
            return generate_calcul()
        calcul3 = f"{number1} / {number2}"
        result = number1 / number2
    return CalculRandom(calcul3, result)
