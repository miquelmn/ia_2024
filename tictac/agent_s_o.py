""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from base import entorn
from tictac import joc
from tictac.estat_s_o import Estat
from tictac.joc import Accio



class Agent(joc.Agent):
    PODA = True

    def __init__(self, nom):
        super(Agent, self).__init__(nom)
        self.__cami = None
        self.__visitats = None

    def cerca(self, estat: Estat, alpha, beta, torn_max=True):
        if estat.es_meta():
            return estat, (1 if not torn_max else -1)

        puntuacio_fills = []

        for fill in estat.genera_fills():
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, alpha, beta, not torn_max)


                if isinstance(punt_fill, tuple):
                    if Agent.PODA:
                        if torn_max:
                            alpha = max(alpha, punt_fill[1])
                        else:
                            beta = min(beta, punt_fill[1])

                        if alpha > beta:
                            break

                    puntuacio_fills.append(punt_fill)
                self.__visitats.add(fill)

        if len(puntuacio_fills) > 0:
            puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
            if torn_max:
                return puntuacio_fills[0]
            else:
                return puntuacio_fills[-1]
        else:
            return 0

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> Accio | tuple[Accio, object]:
        self.__visitats = set()
        estat_inicial = Estat(percepcio["taulell"], self.jugador)

        res = self.cerca(estat_inicial, alpha=-float('inf'), beta=float('inf'))

        if isinstance(res, tuple) and res[0].accions_previes is not None and len(res[0].accions_previes) > 0:
            solucio, punt = res
            return Accio.POSAR, solucio.accions_previes
        else:
            return Accio.ESPERAR
