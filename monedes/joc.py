import enum
import random

import pygame

from base import agent, entorn, joc

class AccionsMoneda(entorn.Accio, enum.Enum):
    DESPLACAR = 0
    GIRAR = 1
    BOTAR = 2
    RES = 3

class Moneda(joc.Joc):
    def __init__(self, agents: list[agent.Agent], random_order: bool = False):
        super(Moneda, self).__init__(agents, (800, 512), title="Casa")

        monedes = "CXCX "

        if random_order:
            monedes = ''.join(random.sample(monedes, len(monedes)))

        self.__monedes = monedes

    @staticmethod
    def __gira(caract: str):
        if caract == "C":
            return "X"
        elif caract == "X":
            return "C"
        else:
            return caract

    def __empty_pos(self) -> int:
        return self.__monedes.find(" ")

    def _aplica(self, accio: entorn.Accio, params=None, agent_actual=None) -> None:
        id_moneda = params
        monedes_aux = list(self.__monedes)
        if accio is AccionsMoneda.DESPLACAR:
            if (self.__empty_pos() != (id_moneda - 1)) and (
                    self.__empty_pos() != (id_moneda + 1)
            ):
                raise joc.HasPerdut("Moneda una damunt l'altra")
            monedes_aux[id_moneda] = " "
            monedes_aux[self.__empty_pos()] = self.__monedes[id_moneda]
        elif accio is AccionsMoneda.BOTAR:
            if (self.__empty_pos() != (id_moneda - 2)) and (
                    self.__empty_pos() != (id_moneda + 2)
            ):
                raise joc.HasPerdut("Moneda una damunt l'altra")
            monedes_aux[id_moneda] = " "
            monedes_aux[self.__empty_pos()] = self.__gira(self.__monedes[id_moneda])
        elif accio is AccionsMoneda.GIRAR:
            monedes_aux[id_moneda] = self.__gira(self.__monedes[id_moneda])
        elif accio is not AccionsMoneda.RES:
            raise Exception(f"Acció no existent en aquest joc: {accio}")

        self.__monedes = "".join(monedes_aux)

    def _draw(self) -> None:
        super(Moneda, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(0, 255, 189))

        cara = pygame.image.load("../assets/monedes/cara.png")
        cara = pygame.transform.scale(cara, (150, 150))

        creu = pygame.image.load("../assets/monedes/creu.png")
        creu = pygame.transform.scale(creu, (150, 150))

        for i, c in enumerate(self.__monedes):
            if c is 'X':
                window.blit(creu, (20 + (i * 150), 181))
            elif c is 'C':
                window.blit(cara, (20 + (i * 150), 181))

    def percepcio(self) -> dict:
        return {"Monedes": self.__monedes}
