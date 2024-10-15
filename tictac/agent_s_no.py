from base import entorn
from practica.joc import Accions
from tictac.joc import Accio

from tictac import joc
from tictac.estat_s_no import Estat


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.__cami = None

    def cerca(self, estat: Estat, torn_max=True):
        if estat.es_meta():
            return estat, (1 if not torn_max else -1)

        puntuacio_fills = []

        for fill in estat.genera_fills():
            punt_fill = self.cerca(fill, not torn_max)
            puntuacio_fills.append(punt_fill)

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> Accio | tuple[Accio, object]:
        estat_inicial = Estat(percepcio["taulell"], self.jugador)

        res = self.cerca(estat_inicial)
        if len(res[0].accions_previes) > 0:
            solucio, punt = res
            return Accio.POSAR, solucio.accions_previes[0]
        else:
            return Accio.ESPERAR
