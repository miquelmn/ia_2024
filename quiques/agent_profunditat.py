""" Fitxer que conté l'agent barca en profunditat.

S'ha d'implementar el mètode:
    actua()
"""
from quiques.agent import Barca
from quiques.estat import Estat
from quiques.joc import AccionsBarca


class BarcaProfunditat(Barca):
    def __init__(self):
        super(BarcaProfunditat, self).__init__()

    def actua(self, percepcio: dict) -> AccionsBarca | (AccionsBarca, (int, int)):
        pass
