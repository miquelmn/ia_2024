""" Fitxer que conté els diferents agents aspiradors.

Autor: Miquel Miró Nicolau (UIB), 2022
"""
from base import agent
from base import entorn


class Aspirador(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | None:
        return None
