from tictac import agent, joc


def main():
    quatre = joc.Taulell([agent.Agent("Miquel"), agent.Agent("Francesc")], mida_taulell=(3, 3), dificultat=3)
    quatre.comencar()


if __name__ == "__main__":
    main()
