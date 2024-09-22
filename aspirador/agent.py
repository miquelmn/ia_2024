""" Fitxer que conté els diferents agents aspiradors.

Percepcions:
    "Loc": [0]
    "Net": [1]

Accions:
    AccionsAspirador.DRETA
    AccionsAspirador.ESQUERRA
    AccionsAspirador.ATURA
    AccionsAspirador.ASPIRA

Autor: Miquel Miró Nicolau (UIB), 2022
"""
import abc

import pygame

from aspirador.joc_gui import AccionsAspirador
from base import agent
from base import entorn


class Aspirador(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=1)

    def pinta(self, display):
        img = pygame.image.load("../assets/aspirador/sprite.png")
        img = pygame.transform.scale(img, (100, 100))
        display.blit(img, self._posicio_pintar)

    @abc.abstractmethod
    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio:
        pass


class AspiradorTaula(Aspirador):
    TAULA = {
        (0, True): AccionsAspirador.DRETA,
        (0, False): AccionsAspirador.ASPIRA,
        (1, True): AccionsAspirador.ESQUERRA,
        (1, False): AccionsAspirador.ASPIRA,
    }

    def actua(self, percepcio: dict) -> entorn.Accio:
        return AspiradorTaula.TAULA[
            (percepcio["Loc"], percepcio["Net"])
        ]


class AspiradorReflex(Aspirador):
    def actua(self, percepcio: dict) -> entorn.Accio:
        """ TODO """


class AspiradorMemoria(Aspirador):
    def actua(self, percepcio: dict) -> entorn.Accio:
        memoria = self.get_memoria(1)

        if memoria is None:
            memoria = [False, False]

        if not percepcio["Net"]:
            return AccionsAspirador.ASPIRA

        memoria[percepcio["Loc"]] = True

        self.set_memoria(memoria)

        if memoria[0] and memoria[1]:
            return AccionsAspirador.ATURA

        if percepcio["Loc"] == 0:
            return AccionsAspirador.DRETA
        else:
            return AccionsAspirador.ESQUERRA
