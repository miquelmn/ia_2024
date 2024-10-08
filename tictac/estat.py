from tictac import agent

class Estat:

    def __init__(self, taulell, agent_actual: agent, accions_previes=None):
        if accions_previes is None:
            accions_previes = []

        self.taulell = taulell
        self.accions_previes = accions_previes
        self.agent_actual = agent_actual

    def es_meta(self) -> bool:
        pos_x, pos_y = self.accions_previes[-1]

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
        continu = False
        count = 0
        best_lineal = 0

        for i, j in zip(
                range(
                    pos_1 - (3 * desp[0]), pos_1 + (3 * desp[0]), desp[0]
                ),
                range(
                    pos_2 - (3 * desp[1]), pos_2 + (3 * desp[1]), desp[1]
                ),
        ):
            if not (0 <= i < len(self.taulell) and 0 <= j < len(self.taulell[0])):
                continue

            if self.taulell[i][j].tipus is agent.jugador:
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

        return best_lineal >= 3

    def __linear_check(self, pos_1, pos_2, agent, reverse=False) -> bool:
        continu = False
        count = 0
        best_lineal = 0
        for x in range(
                max(pos_1 - 3, 0),
                min(pos_1 + 3, len(self.taulell[0])),
                1,
        ):
            if reverse:
                tipus = self.taulell[pos_2][x].tipus
            else:
                tipus = self.taulell[x][pos_2].tipus

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

        return best_lineal >= 3
