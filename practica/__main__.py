from practica import agent, joc


def main():
    agents = [agent.Viatger("Miquel")]
    lab = joc.Laberint(agents)
    lab.comencar()


if __name__ == "__main__":
    main()
