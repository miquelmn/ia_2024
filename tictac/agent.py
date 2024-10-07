"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""

from base import entorn
from tictac import joc


class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(
        self, percepcio: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        return joc.Accio.ESPERAR
