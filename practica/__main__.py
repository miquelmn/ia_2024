from practica import agent, joc


def main():
    mida = (12,12)

    agents = [agent.Viatger("Miquel", size=mida), agent.Viatger("Tomeu", size=mida)]
    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
