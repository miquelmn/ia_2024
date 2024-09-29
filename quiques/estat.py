import copy
import itertools


class Estat:
    MAX_ANIMALS = 3

    # QUIQUES, LLOPS
    # Només funciona en aquest problema, fa el producte cartesià
    moviments_poss = [
        acc
        for acc in itertools.product([0, 1, 2], [0, 1, 2])
        if (acc[-1] + acc[-2]) < 3 and not (acc[-1] == 0 and acc[-2] == 0)
    ]

    def __init__(self, local_barca: str, llops_esq: int, polls_esq: int, accions_previes=None):
        if accions_previes is None:
            accions_previes = []

        self.llops_esq = llops_esq
        self.quica_esq = polls_esq
        self.local_barca = local_barca

        self.accions_previes = accions_previes

    def __hash__(self):
        return hash((self.llops_esq, self.quica_esq))

    @property
    def llops_dreta(self):
        return self.MAX_ANIMALS - self.llops_esq

    @property
    def quica_dreta(self):
        return self.MAX_ANIMALS - self.quica_esq

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (
                self.llops_esq == other.llops_esq
                and self.quica_esq == other.quica_esq
                and self.local_barca == other.local_barca
        )

    def _legal(self) -> bool:
        """ Mètode per detectar si un estat és legal.

        Un estat és legal si no hi ha cap valor negatiu ni major que el màxim

        Returns:
            Booleà indicant si és legal o no.
        """
        return (0 <= self.llops_esq <= self.MAX_ANIMALS) and (0 <= self.quica_esq <= self.MAX_ANIMALS)

    def es_meta(self) -> bool:
        return self.quica_esq == 0 and self.llops_esq == 0

    def es_segur(self) -> bool:
        """ Únicament és segur si hi ha manco llops que gallines, o bé no hi ha gallines.

        Returns:
            Booleà indicant si és segur o no.
        """
        return (
                self.quica_esq >= self.llops_esq or self.quica_esq == 0
        ) and (
                self.quica_dreta >= self.llops_dreta or self.quica_dreta == 0
        )

    def genera_fill(self) -> list:
        """ Mètode per generar els estats fills.

        Genera tots els estats fill a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        estats_generats = []

        for moviments in self.moviments_poss:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = (self)
            nou_estat.accions_previes.append(moviments)

            quiques, llops = moviments

            if self.local_barca is "ESQ":
                # Si la barca és a l'esquerra restam animals a aquella illa.
                quiques = -quiques
                llops = -llops

            nou_estat.local_barca = -self.local_barca
            nou_estat.quica_esq += quiques
            nou_estat.llops_esq += llops

            if nou_estat._legal():
                estats_generats.append(nou_estat)

        return estats_generats

    def __str__(self):
        return (f"Llops esq: {self.llops_esq}, Quiques esq: {self.quica_esq} | "
                f"Llops dreta: {self.llops_dreta}, Quiques dreta: {self.quica_dreta} | Accio {self.accions_previes}")