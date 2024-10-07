""" Joc del Tic, tac, toe

Fitxer que implementa un joc de n en línia. La dificultat es paramètrica. Dins el modul podem trobar
el les següents classes:
    Accio (entorn.Accio, enum.Enum). Enumerat que indica la acció a realitzar.
    Agent (base.Agent). Classe pare dels agents a desenvolupar.
    Taulell (base.joc). El joc en sí.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""

import enum

import pygame

import base
from base import entorn, joc


class Accio(entorn.Accio, enum.Enum):
    ESPERAR = 0
    POSAR = 1


class Agent(base.Agent):
    random__used = set()

    def __init__(self, nom: str):
        super().__init__(long_memoria=1)

        self.__nom = nom
        self.__jugador = None

    def pinta(self, display):
        pass

    @property
    def jugador(self):
        return self.__jugador

    @jugador.setter
    def jugador(self, jugador):
        """Defineix amb quina fitxa juga l'agent

        Args:
            tipus (str): "X" ó "0"

        Returns:
            None
        """
        self.__jugador = jugador

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        return Accio.ESPERAR

    @property
    def nom(self):
        return self.__nom


def drawX(window, x, y):
    pygame.draw.lines(
        window, (255, 0, 0), True, [(x - 45, y - 45), (x + 45, y + 45)], 5
    )
    pygame.draw.lines(
        window, (255, 0, 0), True, [(x - 45, y + 45), (x + 50, y - 45)], 5
    )


class Casella:

    def __init__(
        self,
        tipus=" ",
    ):
        self.tipus = tipus

    def draw(self, window, x, y, width=100, height=100):
        pygame.draw.rect(
            window,
            pygame.Color(0, 0, 0),
            pygame.Rect(x * width, y * height, width, height),
            2,
        )

        if self.tipus == "X":
            drawX(window, (x * 100) + 50, (y * 100) + 50)
        if self.tipus == "0":
            pygame.draw.circle(
                window, (0, 0, 255), ((x * 100) + 50, (y * 100) + 50), 40, width=5
            )

    def posa(self, tipus):
        if self.tipus != " ":
            raise Exception("Has fet trampes: aquesta casella ja està ocupada")
        self.tipus = tipus

    def __str__(self):
        return self.tipus


class Taulell(joc.Joc):
    def __init__(
        self,
        agents: list[Agent] | Agent,
        mida_taulell: tuple[int, int] = (8, 8),
        dificultat: int = 4,
    ):
        super(Taulell, self).__init__(
            agents, (mida_taulell[0] * 100, mida_taulell[1] * 100), title="Minimax"
        )

        self.__caselles = []
        self.__mida_taulell = mida_taulell

        for x in range(mida_taulell[0]):
            caselles_col = []
            for y in range(mida_taulell[1]):
                tipus = " "
                caselles_col.append(Casella(tipus))
            self.__caselles.append(caselles_col)

        for agent, tipus in zip(agents, ["0", "X"]):
            agent.jugador = tipus

        if not isinstance(agents, list):
            agents = [agents]

        self._agents = agents
        self.torn = 0
        self.acabat = False
        self.dificultat = dificultat

    def _aplica(
        self, accio: entorn.Accio, params=None, agent_actual: Agent = None
    ) -> None:
        if not self.acabat:
            if accio not in Accio:
                raise ValueError(f"Acció no existent en aquest joc: {accio}")

            if accio is not Accio.ESPERAR and not isinstance(params, tuple):
                raise ValueError("Paràmetres incorrectes")

            if accio is Accio.POSAR:
                pos_x, pos_y = params
                if not (
                    0 <= pos_x < len(self.__caselles)
                    and 0 <= pos_y < len(self.__caselles[0])
                ):
                    raise ValueError(f"Posició {params} fora dels límits")

                self.__caselles[pos_x][pos_y].posa(agent_actual.jugador)
                self.acabat = self.__ha_guanyat((pos_x, pos_y))

            if self.acabat:
                print(f"Agent {agent_actual.nom} ha guanyat")
            self.torn += 1

    def _draw(self) -> None:
        super(Taulell, self)._draw()
        window = self._game_window
        window.fill(pygame.Color(255, 255, 255))

        for x in range(len(self.__caselles)):
            for y in range(len(self.__caselles[0])):
                self.__caselles[x][y].draw(window, x, y)

    def __ha_guanyat(self, posicio: tuple) -> bool:
        pos_x, pos_y = posicio

        horizontal_check = self.__linear_check(pos_x, pos_y, self.agent_actual)
        vertical_check = self.__linear_check(
            pos_y, pos_x, self.agent_actual, reverse=True
        )

        diagonal_check_tl = self.__diagonal_check(
            pos_x, pos_y, self.agent_actual, (+1, -1)
        )
        diagonal_check_tr = self.__diagonal_check(
            pos_x, pos_y, self.agent_actual, (+1, +1)
        )

        return (
            horizontal_check or vertical_check or diagonal_check_tl or diagonal_check_tr
        )

    def __diagonal_check(self, pos_1, pos_2, agent, desp: tuple):
        dificultat = self.dificultat
        continu = False
        count = 0
        best_lineal = 0

        for i, j in zip(
            range(
                pos_1 - (dificultat * desp[0]), pos_1 + (dificultat * desp[0]), desp[0]
            ),
            range(
                pos_2 - (dificultat * desp[1]), pos_2 + (dificultat * desp[1]), desp[1]
            ),
        ):
            if not (0 <= i < len(self.__caselles) and 0 <= j < len(self.__caselles[0])):
                continue

            if self.__caselles[i][j].tipus is agent.jugador:
                if not continu:
                    continu = True
                count += 1
            else:
                continu = False
                if count > best_lineal:
                    best_lineal = count
                count = 0
        if count > best_lineal:
            best_lineal = count

        return best_lineal >= dificultat

    def __linear_check(self, pos_1, pos_2, agent, reverse=False) -> bool:
        dificultat = self.dificultat

        continu = False
        count = 0
        best_lineal = 0
        for x in range(
            max(pos_1 - dificultat, 0),
            min(pos_1 + dificultat, self.__mida_taulell[0]),
            1,
        ):
            if reverse:
                tipus = self.__caselles[pos_2][x].tipus
            else:
                tipus = self.__caselles[x][pos_2].tipus

            if tipus is agent.jugador:
                if not continu:
                    continu = True
                count += 1
            else:
                continu = False
                if count > best_lineal:
                    best_lineal = count
                count = 0

        if count > best_lineal:
            best_lineal = count

        return best_lineal >= dificultat

    @property
    def agent_actual(self):
        return self._agents[self.torn % len(self._agents)]

    def percepcio(self) -> dict:
        return {
            "taulell": [[c.tipus for c in row] for row in self.__caselles],
            "mida": self.__mida_taulell,
        }
