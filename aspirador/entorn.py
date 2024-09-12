""" Fitxer amb tota la informació de l'base de l'aspirador.

Autor: Miquel Miró Nicolau (UIB), 2022
"""

import enum
import random

from base import entorn


class AccionsAspirador(entorn.Accio, enum.Enum):
    ESQUERRA = 0
    DRETA = 1
    ASPIRA = 2
    ATURA = 3


class Sensor(enum.Enum):
    LLOC = 0
    ESTAT = 1


class Localitzacio(enum.Enum):
    HABITACIO_ESQ = 0
    HABITACIO_DRET = 1

    @staticmethod
    def aleatori() -> enum.Enum:
        if random.randint(0, 1) == 0:
            return Localitzacio.HABITACIO_DRET
        else:
            return Localitzacio.HABITACIO_ESQ


class EstatHabitacio(enum.Enum):
    NET = 0
    BRUT = 1

    @staticmethod
    def aleatori() -> enum.Enum:
        if random.randint(0, 1) == 0:
            return EstatHabitacio.NET
        else:
            return EstatHabitacio.BRUT
