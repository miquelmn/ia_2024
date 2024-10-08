from tictac import agent, joc


def main():
    #aqui s'ha d'afegir un agent adversari
    quatre = joc.Taulell([agent.Agent("Miquel")], mida_taulell=(5, 5), dificultat=3)
    quatre.comencar()


if __name__ == "__main__":
    main()
