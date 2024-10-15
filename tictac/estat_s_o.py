import copy


class Estat:

    def __init__(self, taulell, fitxa: str, accions_previes=None):
        self.taulell = taulell
        self.accions_previes = accions_previes
        self.fitxa = fitxa

        self.__es_meta = None

    def __hash__(self):
        return hash(str(self.taulell) + "," + self.fitxa)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self.taulell)

    def es_ple(self):
        ocupats = 0

        for row in self.taulell:
            for casella in row:
                ocupats += int(casella != " ")

        return ocupats == len(self.taulell[0]) * len(self.taulell[1])

    def __guanyador(self):
        if self.__es_meta is None:
            meta = False
            for pos_x, pos_y in [(0, 0), (1, 0), (2, 0)]:
                horizontal_check = self.__linear_check(pos_x, pos_y)
                vertical_check = self.__linear_check(pos_y, pos_x, reverse=True)

                diagonal_check_tl = self.__diagonal_check(pos_x, pos_y, (+1, -1))
                diagonal_check_tr = self.__diagonal_check(pos_x, pos_y, (+1, +1))

                meta = (
                        horizontal_check
                        or vertical_check
                        or diagonal_check_tl
                        or diagonal_check_tr
                )

                if meta:
                    break

            self.__es_meta = meta

        return self.__es_meta

    def es_meta(self) -> bool:
        ple = self.es_ple()
        guanyador = self.__guanyador()

        return guanyador or ple

    def __diagonal_check(self, pos_1, pos_2, desp: tuple):
        continu = False
        count = 0
        best_lineal = 0
        fitxa = None

        for i, j in zip(
                range(pos_1 - (3 * desp[0]), pos_1 + (3 * desp[0]), desp[0]),
                range(pos_2 - (3 * desp[1]), pos_2 + (3 * desp[1]), desp[1]),
        ):
            if not (0 <= i < len(self.taulell) and 0 <= j < len(self.taulell[0])):
                continue

            if (
                    self.taulell[i][j] == fitxa
                    or fitxa is None
                    and self.taulell[i][j] != " "
            ):
                fitxa = self.taulell[i][j]
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

    def __linear_check(self, pos_1, pos_2, reverse=False) -> bool:
        continu = False
        count = 0
        best_lineal = 0

        fitxa = None
        for x in range(
                max(pos_1 - 3, 0),
                min(pos_1 + 3, len(self.taulell[0])),
                1,
        ):
            if reverse:
                tipus = self.taulell[pos_2][x]
            else:
                tipus = self.taulell[x][pos_2]

            if tipus is fitxa or fitxa is None and tipus != " ":
                fitxa = tipus
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

    @staticmethod
    def gira(fitxa):
        if fitxa == "0":
            return "X"
        else:
            return "0"

    def genera_fills(self):
        fills = []

        for pos_x in range(len(self.taulell)):
            for pos_y in range(len(self.taulell[0])):
                casella = self.taulell[pos_x][pos_y]
                if casella == " ":
                    nou_estat = copy.copy(self)
                    nou_estat.taulell = copy.copy(self.taulell)

                    nou_estat.taulell[pos_x][pos_y] = self.fitxa
                    nou_estat.accions_previes = (pos_x, pos_y)
                    nou_estat.fitxa = Estat.gira(self.fitxa)
                    nou_estat.__es_meta = None

                    fills.append(nou_estat)

        return fills
