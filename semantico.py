# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (ago-2024)
# ---------------------------------------------------

# Dentro do semantico teremos a tabela de símbolos e o arquivo alvo que será gerado (nós geraremos código em python)

from ttoken import TOKEN

class Semantico:

    def __init__(self, sintatico):
        #nos usaremos um dicionario para representar a nossa tabela de simbolos
        self.tabelaSimbolos = dict()
        self.sintatico = sintatico
        self.subrotinaAtual = 'program'
        #a partir daqui a gente vai criar o Semantico. ELe e o Sintatico são muito amarrados entao a gente nao vai criar um objeto pro semantico

        #self.alvo = open(nomeAlvo, "wt")

    #def fechaAlvo(self):

    #   self.alvo.close()

    def erroSemantico(self, msg):
        (token, lexema, linha, coluna) = self.sintatico.tokenLido
        print(f'Erro na linha {linha}: ')
        print(f' {msg}')
        raise Exception

    #no metodo gera, nivel é o nivel de identação. Cada nível é igual a 4 espaços. Nivel 0: 0 espaços, Nivel 1: 4 espaços
    #def gera(self, nivel, codigo):
    #    identacao = ' ' * 4 * nivel
    #    linha = identacao + codigo
    #   self.alvo.write(linha)

    #pega os identificadores e seu respectivo tipo e salva na tabela de símbolos
    def declara(self, nomes, tipo): #tipo será uma string

        for id in nomes:
            if self.existe_id(id):
                msg = f'Identificador {id} ja existente'
                self.erroSemantico(msg)
            else:
                if self.subrotinaAtual == 'program':
                    if tipo == TOKEN.FUNCTION or tipo == TOKEN.PROCEDURE:
                        tab_funcao = dict()
                        self.tabelaSimbolos[id] = (tipo,tab_funcao)
                    else:
                        self.tabelaSimbolos[id] = (tipo, None)
                else:
                    nome = self.subrotinaAtual
                    (tipo_rotina,tabela) = self.tabelaSimbolos[nome]
                    tabela[id] = (tipo,None)



    def existe_id(self, identificador):
        if self.subrotinaAtual != 'program':
            nome = self.subrotinaAtual
            (tipo_rotina, tabela) = self.tabelaSimbolos[nome]
            if identificador in tabela:
                return True

        if identificador in self.tabelaSimbolos:
            return True
        else:
            return False

    #verifica o que é o identificador que eu passei (se é variavel, funcao, procedimento, etc.)
    def consulta_tipo_id(self,id):
        if self.subrotinaAtual != 'program':
            nome = self.subrotinaAtual
            (tipo_rotina, tabela) = self.tabelaSimbolos[nome]
            if id in tabela:
                return tabela[id]
        else:
            return self.tabelaSimbolos[id]

    def entrou_subrotina(self,nome):
        self.subrotinaAtual = nome

    def saiu_subrotina(self):
        self.subrotinaAtual = 'program'
