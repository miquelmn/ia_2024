from tictac import joc
from tictac import agent_s_no as agent
from tictac import agent_s_o as agent


def main():
    quatre = joc.Taulell(
        [agent.Agent("Agent1"), agent.Agent("Agent2")],
        mida_taulell=(3, 3),
        dificultat=3
    )
    quatre.comencar()


if __name__ == "__main__":
    main()
