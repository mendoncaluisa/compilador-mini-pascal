# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (ago-2024)
# ---------------------------------------------------

from lexico import TOKEN, Lexico
from semantico import Semantico

class Sintatico:
    def __init__(self, lexico):

        self.lexico = lexico
        self.semantico = Semantico(self)  # estou passando o sintatico pro semantico

    def traduz(self):
        self.token_lido = self.lexico.get_token()  # o sintatico pede para o lexico token por token
        try:  # ao receber o token ele vai na gramática e verifica se está de acordo com a gramática
            self.program()  # esse é o método de ponto de partida que faz ele entrar na gramátic
            print('Traduzido com sucesso.')
        except:
            pass

    # o método que chama o consome, vai passar o lexema pra ser consumido. Entao aqui no
    # metodo consome, é feita a verificação: o token que é pra ser consumido, é igual ao token_lido do
    # método traduz? Se sim, deu certo, se não, trata o erro aqui mesmo no consome "era esperado (token_atual)
    # tal coisa mas veio tal coisa (token_lido)"
    def consome(self, token_atual):
        (token, lexema, linha, coluna) = self.token_lido
        if token_atual == token:  # se o token consumido é igual ao token lido, pego um novo token pra analisar
            self.token_lido = self.lexico.get_token()
        else:  # trata o erro quando o token que era pra ser consumido não é igual ao token que foi lido
            msg_token_lido = TOKEN.msg(token)
            msg_token_atual = TOKEN.msg(token_atual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msg_token_lido
            print(f'Era esperado {msg_token_atual} mas veio {msg}')
            raise Exception

    # -------------------------------- Implementando a gramática --------------------------------

    # <program> -> program id ( ) ; <declarations> <subprogram_declarations> <compound_statement> .
    def program(self):
        self.consome(TOKEN.PROGRAM)
        self.consome(TOKEN.id)
        self.consome(TOKEN.abreParentese)
        self.consome(TOKEN.fechaParentese)
        self.consome(TOKEN.ptoVirg)
        self.declarations()
        self.subprogram_declarations()
        self.compound_statement()
        self.consome(TOKEN.pto)

    # <identifier_list> -> id <resto_identifier_list>
    def identifier_list(self):
        nome = self.token_lido[1]
        self.consome(TOKEN.id)
        lista = [nome]
        lista2 = self.resto_identifier_list()
        return lista + lista2

    # <resto_identifier_list> ->, id < resto_identifier_list > | LAMBDA
    def resto_identifier_list(self):
        if self.token_lido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            return self.identifier_list()
        else:
            return []

    # <declarations> -> var <identifier_list> : <type> ; <declarations> | LAMBDA

    def declarations(self):
        if self.token_lido[0] == TOKEN.VAR:
            self.consome(TOKEN.VAR)
            nomes = self.identifier_list()
            self.consome(TOKEN.doisPontos)
            tipo = self.type()
            self.consome(TOKEN.ptoVirg)
            self.semantico.declara(nomes, tipo)
            self.declarations()
        else:
            pass

    # <type> -> <standard_type> | array [ num .. num ] of <standard_type>
    def type(self):
        if self.token_lido[0] == TOKEN.ARRAY:
            self.consome(TOKEN.ARRAY)
            self.consome(TOKEN.abreColchete)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.ptoPto)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.fechaColchete)
            self.consome(TOKEN.OF)
            tipo = self.standard_type()
            return TOKEN.ARRAY, tipo
        else:
            return self.standard_type()

    # <standard_type> -> integer | real
    def standard_type(self):
        if self.token_lido[0] == TOKEN.INTEGER:
            self.consome(TOKEN.INTEGER)
            return TOKEN.INTEGER
        else:
            self.consome(TOKEN.REAL)
            return TOKEN.REAL

    # <subprogram_declarations> -> <subprogram_declaration> ; <subprogram_declarations> | LAMBDA
    def subprogram_declarations(self):
        if self.token_lido[0] == TOKEN.BEGIN:
            pass
        else:
            self.subprogram_declaration()
            self.consome(TOKEN.ptoVirg)
            self.subprogram_declarations()

    # <subprogram_declaration> -> <subprogram_head> <declarations> <compound_statement>
    def subprogram_declaration(self):
        self.subprogram_head()
        self.declarations()
        self.compound_statement()

    # <subprogram_head> -> function id <arguments> : <standard_type> ; | procedure id <arguments> ;
    def subprogram_head(self):
        if self.token_lido[0] == TOKEN.FUNCTION:
            self.consome(TOKEN.FUNCTION)
            nome_funcao = self.token_lido[1]
            self.consome(TOKEN.id)
            self.semantico.declara(nome_funcao, TOKEN.FUNCTION)
            self.arguments()
            self.consome(TOKEN.doisPontos)
            self.standard_type()
            self.consome(TOKEN.ptoVirg)
        else:
            self.consome(TOKEN.PROCEDURE)
            nome_procedimento = self.token_lido[1]
            self.consome(TOKEN.id)
            self.semantico.declara(nome_procedimento, TOKEN.PROCEDURE)
            self.arguments()
            self.consome(TOKEN.ptoVirg)

    # <arguments> -> ( <parameter_list> ) | LAMBDA
    def arguments(self):
        if self.token_lido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.parameter_list()
            self.consome(TOKEN.fechaParentese)
        else:
            pass

    # <parameter_list> -> <identifier_list> : <type> <resto_parameter_list>
    def parameter_list(self):
        self.identifier_list()
        self.consome(TOKEN.doisPontos)
        self.type()
        self.resto_parameter_list()

    # <resto_parameter_list> -> ; <identifier_list> : <type> <resto_parameter_list> | LAMBDA
    def resto_parameter_list(self):
        if self.token_lido[0] == TOKEN.ptoVirg:
            self.consome(TOKEN.ptoVirg)
            self.identifier_list()
            self.consome(TOKEN.doisPontos)
            self.type()
            self.resto_parameter_list()
        else:
            pass

    # <compound_statement> -> begin <optional_statements> end
    def compound_statement(self):
        self.consome(TOKEN.BEGIN)
        self.optional_statements()
        self.consome(TOKEN.END)

    # < optional_statements > -> < statement_list > | LAMBDA
    def optional_statements(self):
        if self.token_lido[0] == TOKEN.END:
            pass
        else:
            self.statement_list()

    # <statement_list> -> <statement> <resto_statement_list>
    def statement_list(self):
        self.statement()
        self.resto_statement_list()

    # < resto_statement_list > -> ; < statement > < resto_statement_list > | LAMBDA
    def resto_statement_list(self):
        if self.token_lido[0] == TOKEN.ptoVirg:
            self.consome(TOKEN.virg)
            self.statement()
            self.resto_statement_list()
        else:
            pass

        # <statement> -> <variable> assignop <expression> | <procedure_statement> |
        # <compound_statement> | <if_statement> | return <expression> |
        # while <expression> do <statement> | <inputOutput>

    def statement(self):
        if self.token_lido[0] == TOKEN.id:
            nome = self.token_lido[1]
            if self.semantico.existe_id(nome):
                tipo = self.semantico.consulta_tipo_id(nome)
                if tipo in [TOKEN.INTEGER, TOKEN.REAL]:
                    self.variable()
                    self.consome(TOKEN.assignop)
                    self.expression()
                else:
                    self.procedure_statement()
            else:
                msg = 'Idenficador ' + nome + ' não declarado.'
                self.semantico.erro_semantico(msg)

        elif self.token_lido[0] == TOKEN.BEGIN:
            self.compound_statement()

        elif self.token_lido[0] == TOKEN.IF:
            self.if_statement()

        elif self.token_lido[0] == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.expression()

        elif self.token_lido[0] == TOKEN.WHILE:
            # while <expression> do <statement>
            self.consome(TOKEN.WHILE)
            self.expression()
            self.consome(TOKEN.DO)
            self.statement()

        else:
            self.input_output()

    # <if_statement> -> if <expression> then <statement> <opc_else>
    def if_statement(self):
        self.consome(TOKEN.IF)
        self.expression()
        self.consome(TOKEN.THEN)
        self.statement()
        self.opc_else()

    # <opc_else> -> else <statement> | LAMBDA
    def opc_else(self):
        if self.token_lido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.statement()
        else:
            pass

    def variable(self):  # <variable> -> id <opc_index>

        self.consome(TOKEN.id)
        self.opc_index()

    def opc_index(self):  # <opc_index> -> [ <expression> ] | LAMBDA

        if self.token_lido[0] != TOKEN.assignop:
            self.consome(TOKEN.abreColchete)
            self.expression()
            self.consome(TOKEN.fechaColchete)

        else:
            pass

    def procedure_statement(self):  # <procedure_statement> -> id <opc_parameters>

        self.consome(TOKEN.id)
        self.opc_parameters()

    def opc_parameters(self):  # <opc_parameters> -> ( <expression_list> ) | LAMBDA

        if self.token_lido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.expression_list()
            self.consome(TOKEN.fechaParentese)
        else:
            pass

    def expression_list(self):  # <expression_list> -><expression> <resto_expression_list>

        self.expression()
        self.resto_expression_list()

    def resto_expression_list(self):  # <resto_expression_list> -> , <expression> <resto_expression_list> | LAMBDA

        if self.token_lido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.expression()
            self.resto_expression_list()

        else:
            pass

    def expression(self):  # <expression> -> <simple_expression> <resto_expression>

        self.simple_expression()
        self.resto_expression()

    def resto_expression(self):  # <resto_expression> -> LAMBDA | relop <simple_expression> <resto_expression>

        if self.token_lido[0] == TOKEN.relop:
            self.consome(TOKEN.relop)
            self.simple_expression()
            self.resto_expression()

        else:
            pass

    def simple_expression(self):  # <simple_expression> -> <term> <resto_simple_expression>

        self.term()
        self.resto_simple_expression()

    def resto_simple_expression(self):  # <resto_simple_expression> -> LAMBDA | addop <term> <resto_simple_expression>

        if self.token_lido[0] == TOKEN.ADDOP:
            while self.token_lido[0] == TOKEN.ADDOP:
                self.consome(TOKEN.ADDOP)
                self.term()

        else:
            pass

    def term(self):  # <term> -> <uno> <resto_term>

        self.uno()
        self.resto_term()

    def resto_term(self):  # <resto_term> -> LAMBDA | mulop <uno> <resto_term>

        if self.token_lido[0] == TOKEN.MULOP:
            while self.token_lido[0] == TOKEN.MULOP:
                self.consome(TOKEN.MULOP)
                self.uno()

        else:
            pass

    def uno(self):  # <uno> -> <factor> | addop <factor>

        if self.token_lido[0] == TOKEN.ADDOP:
            self.consome(TOKEN.ADDOP)
            self.factor()

        else:
            self.factor()

    def factor(self):  # <factor> -> id <resto_id> | num | ( <expression> ) | not <factor>

        if self.token_lido[0] == TOKEN.id:
            token_id = self.token_lido
            self.consome(TOKEN.id)
            self.resto_id(token_id)

        elif self.token_lido[0] == TOKEN.numInteger:
            self.consome(TOKEN.numInteger)

        elif self.token_lido[0] == TOKEN.numReal:
            self.consome(TOKEN.numReal)

        elif self.token_lido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.expression()
            self.consome(TOKEN.fechaParentese)

        else:
            self.consome(TOKEN.NOT)
            self.factor()

        # <resto_id> -> ( <expression_list> ) | LAMBDA

    def resto_id(self, token_id):
        if self.token_lido[0] == TOKEN.abreParentese:
            tipo_id = self.semantico.consulta_tipo_id(token_id[1])
            if tipo_id != TOKEN.FUNCTION:
                msg = 'O identificador ' + token_id[1] + ' não é uma função.'
                self.semantico.erro_semantico(msg)
            self.consome(TOKEN.abreParentese)
            self.expression_list()
            self.consome(TOKEN.fechaParentese)
        else:
            pass

    def input_output(self):  # <inputOutput> -> writeln(<outputs>) | write(<outputs>) | read(id) | readln(id)

        if self.token_lido[0] == TOKEN.WRITELN:
            self.consome(TOKEN.WRITELN)
            self.consome(TOKEN.abreParentese)
            self.outputs()
            self.consome(TOKEN.fechaParentese)

        elif self.token_lido[0] == TOKEN.WRITE:
            self.consome(TOKEN.WRITE)
            self.consome(TOKEN.abreParentese)
            self.outputs()
            self.consome(TOKEN.fechaParentese)

        elif self.token_lido[0] == TOKEN.READ:
            self.consome(TOKEN.READ)
            self.consome(TOKEN.abreParentese)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaParentese)

        else:
            self.consome(TOKEN.READLN)
            self.consome(TOKEN.abreParentese)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaParentese)

    def outputs(self):  # <outputs> -> <out> <restoOutputs>

        self.out()
        self.resto_outputs()

    def resto_outputs(self):  # <restoOutputs> -> , <out> <restoOutputs> | LAMBDA
        if self.token_lido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.out()
            self.resto_outputs()
        else:
            pass

    def out(self):  # <out> -> num | id | string

        if self.token_lido[0] == TOKEN.numInteger:
            self.consome(TOKEN.numInteger)

        elif self.token_lido[0] == TOKEN.numReal:
            self.consome(TOKEN.numReal)

        elif self.token_lido[0] == TOKEN.id:
            self.consome(TOKEN.id)

        else:
            self.consome(TOKEN.string)

    # ------------------------- TESTA LEXICO ------------------------- #
    def testa_lexico(self):
        self.token_lido = self.lexico.get_token()
        (token, lexema, linha, coluna) = self.token_lido
        while token != TOKEN.eof:
            self.lexico.imprime_token(self.token_lido)
            self.token_lido = self.lexico.get_token()
            (token, lexema, linha, coluna) = self.token_lido
