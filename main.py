# ---------------------------------------------------
# Tradutor para a linguagem CALC
#
# versao 1a (ago-2024)
# ---------------------------------------------------
from lexico import Lexico
from sintatico import Sintatico
class Tradutor:
    def __init__(self, nomeArq):
        # self.arq = None
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)
        self.sintatico = Sintatico(self.lexico)

    def traduz(self):
        self.sintatico.traduz()

    def finaliza(self):
        self.arq.close()


# inicia a traducao
if __name__ == '__main__':
    x = Tradutor('teste.txt')
    x.inicializa()
    x.traduz()
    # x.lexico.testaLexico()
    x.sintatico.testa_lexico()

    x.finaliza()
