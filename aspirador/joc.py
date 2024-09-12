from base import agent, entorn, joc

class AspiradorNoG(joc.JocNoGrafic):

    def __init__(self, agents: list[agent.Agent]):
        super(AspiradorNoG, self).__init__(agents=agents)
        # TODO


    def _draw(self):
        # TODO
        pass


    def percepcio(self) -> entorn.Percepcio | dict:
        # TODO
        pass


    def _aplica(self, accio: entorn.Accio, params=None, agent_actual=None):
        # TODO
        pass

