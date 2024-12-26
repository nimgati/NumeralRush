import json

from calcul_random import CalculRandom

levels = {
    1: [
        CalculRandom(calcul1="17 + 23", resultat_calcul=0),
        CalculRandom(calcul1="25 + 73", resultat_calcul=0),
        CalculRandom(calcul1="89 + 9", resultat_calcul=0),
        CalculRandom(calcul1="73 + 30", resultat_calcul=0),
        CalculRandom(calcul1="45 + 55", resultat_calcul=0),
        CalculRandom(calcul1="10 + 46 + 12", resultat_calcul=0),
        CalculRandom(calcul1="14 + 28 + 6", resultat_calcul=0),
        CalculRandom(calcul1="17 + 13 + 25", resultat_calcul=0),
        CalculRandom(calcul1="1 + 1", resultat_calcul=0),
        CalculRandom(calcul1="1 + 1", resultat_calcul=0),
        CalculRandom(calcul1="1 + 1", resultat_calcul=0),
        CalculRandom(calcul1="1 + 1", resultat_calcul=0),
        CalculRandom(calcul1="1 + 1", resultat_calcul=0),
    ],
    2: [
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
        CalculRandom(calcul1="", resultat_calcul=0),
    ]
}


def get_level(level: int) -> list[CalculRandom] | None:
    if level not in levels.keys():
        return None
    return levels[level]

def get_level_len(level: int) -> int:
    if level not in levels.keys():
        return 0
    return len(levels[level])

def get_all_levels() -> list[int]:
    return list(levels.keys())

def level_terminated(level: int, score: int) -> bool:
    if level not in levels.keys():
        return False
    try:
        with open("level_win.json") as f:
            data = json.load(f)

        data[level] = f"{score}/{len(levels[level])}"
        with open("level_win.json", "w") as f:
            json.dump(data, f)
        return True
    except Exception:
        return False
