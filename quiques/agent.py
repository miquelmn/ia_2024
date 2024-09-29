""" Fitxer que conté l'agent Barca.

Percepcions:
    ClauPercepcio.LLOC
    ClauPercepcio.QUICA_ESQ
    ClauPercepcio.LLOP_ESQ
    ClauPercepcio.QUICA_DRETA
    ClauPercepcio.LLOP_DRETA

Accions:
    AccionsBarca.MOURE, (nombre_de_quiques, nombres_de_llop)
    AccionsBarca.ATURA
"""
import abc

from base import agent
from quiques.joc import  AccionsBarca



class Barca(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        print(self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percepcio: dict) -> AccionsBarca | tuple[AccionsBarca, (int, int)]:
        pass



