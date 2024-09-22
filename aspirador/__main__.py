from aspirador import joc_gui, agent


def main():
    agents = [agent.AspiradorTaula()]

    hab = joc_gui.Aspirador(agents)
    hab.comencar()


if __name__ == "__main__":
    main()
