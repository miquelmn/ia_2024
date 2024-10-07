from queue import PriorityQueue

from base import agent, entorn
from monedes.joc import AccionsMoneda

SOLUCIO = " XXXC"


class Estat:
    def __init__(self, info: str, pes: int, accions_previes: list = None):
        if accions_previes is None:
            accions_previes = []

        self.__info = info
        self.__pes = pes
        self.__accions_previes = accions_previes

    def __hash__(self):
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    @property
    def accions_previes(self):
        return self.__accions_previes

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.__info == other.info

    def es_meta(self) -> bool:
        return self.__info == SOLUCIO

    def genera_fills(self):
        fills = []

        buit = self.__info.find(" ")

        despls = [buit - 1, buit + 1]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.__info[desp]
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 1,
                        self.__accions_previes + [(AccionsMoneda.DESPLACAR, desp)],
                    )
                )

        for i in range(len(self.__info)):
            info_aux = list(self.__info)
            info_aux[i] = self.gira(info_aux[i])
            fills.append(
                Estat(
                    "".join(info_aux),
                    self.__pes + 2,
                    self.__accions_previes + [(AccionsMoneda.GIRAR, i)]
                )
            )

        despls = [buit - 2, buit + 2]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.gira(self.__info[desp])
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 2,
                        self.__accions_previes + [(AccionsMoneda.BOTAR, desp)]
                    )
                )

        return fills

    def calc_heuristica(self):
        pos = self.__info.find(" ")
        heuristica = 0
        for lletra_es, lletra_sol in zip(self.__info, SOLUCIO):
            if lletra_sol != " ":
                heuristica += int(lletra_es != lletra_sol)

        heuristica += pos

        return heuristica + self.__pes

    def __str__(self):
        return str(self.__info)

    def __lt__(self, other):
        return False

    @staticmethod
    def gira(moneda):
        if moneda == "C":
            return "X"
        elif moneda == "X":
            return "C"
        else:
            return " "


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca(self, estat_inicial):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial))

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.genera_fills()

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.calc_heuristica(), estat_f))

            self.__tancats.add(actual)

        if actual.es_meta():
            self.__accions = actual.accions_previes

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat_inicial = Estat(percepcio["Monedes"], 0)

        if self.__accions is None:
            self.cerca(estat_inicial)

        if self.__accions:
            acc = self.__accions.pop()

            return acc[0], acc[1]
        else:
            return AccionsMoneda.RES
