from base import entorn
from practica import joc
from practica.joc import Accions


class Viatger(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(Viatger, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percepcio: dict
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        return Accions.ESPERAR
