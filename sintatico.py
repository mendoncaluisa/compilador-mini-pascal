# ---------------------------------------------------
# Tradutor para a linguagem CALC
#
# versao 1a (mar-2024)
# ---------------------------------------------------
from lexico import TOKEN, Lexico


#  from semantico import Semantico

class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico
        self.nome_alvo = 'alvo.out'
        #  self.semantico = Semantico(self.nome_alvo)

    def traduz(self):
        self.token_lido = self.lexico.getToken()
        try:
            self.p()
            print('Traduzido com sucesso.')

        except:
            pass
        #  self.semantico.finaliza()

    def consome(self, token_atual):
        (token, lexema, linha, coluna) = self.token_lido
        if token_atual == token:
            self.token_lido = self.lexico.getToken()
        else:
            msg_token_lido = TOKEN.msg(token)
            msg_token_atual = TOKEN.msg(token_atual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msg_token_lido
            print(f'Era esperado {msg_token_atual} mas veio {msg}')
            raise Exception

    def testaLexico(self):
        self.token_lido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.token_lido
        while token != TOKEN.eof:
            self.lexico.imprimeToken(self.token_lido)
            self.token_lido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.token_lido

#  -------------------------- segue a gramatica -----------------------------------------

    def programa(self):
        """
        <program> ->
        program id ( <identifier_list> ) ;
        <declarations>
        <subprogram_declarations>
        <compound_statement>
        .
        """

        self.consome(TOKEN.PROGRAM)
        lexema = self.token_lido[1]
        self.consome(TOKEN.id)
        self.consome(TOKEN.abreParentese)
        self.identifier_list()  # <identifier_list>
        self.consome(TOKEN.fechaParentese)
        self.consome(TOKEN.ptoVirg)
        self.declarations()  # <declarations>
        self.subprogram_declaration()  # <subprogram_declarations>
        self.compound_statement()  # <compound_statement>
        self.consome(TOKEN.pto)

    def identifier_list(self):  # <identifier_list>
        self.consome(TOKEN.id)
        self.resto_identifier_list()
        pass

    def resto_identifier_list(self):  # <resto_identifier_list>
        while token_lido ==  TOKEN.virg:
            self.consome(TOKEN.virg)
            self.consome(TOKEN.id)
        
        pass

    def declarations(self):  # <declarations>
        
        while token_lido[0] == TOKEN.variavel:
            self.consome(TOKEN.variavel)
            self.identifier_list()
            self.consome(TOKEN.doisPontos)
            self.type()
            self.consome(TOKEN.ptoVirg)
        
        pass

    def type(self):  # <type>
        
        if token_lido[0] == TOKEN.string:
            self.consome(TOKEN.string)
            self.consome(TOKEN.abreColchete)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.ptoPto)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.OF)
            self.standard_type()

    def standard_type(self):  # <standard_type>

        pass

    def subprogram_declarations(self):  # <subprogram_declarations>
        
        while token_lido == subprogram_declaration():
            self.subprogram_declaration
            self.consome(TOKEN.ptoVirg)
        
        pass

    def subprogram_declaration(self):  # <subprogram_declaration>
        
        self.subprogram_head()
        self.declarations()
        self.compound_statement()


    def subprogram_head(self):  # <subprogram_head>
        
        if token_lido == 'function':
            self.consome(TOKEN.reservada)
            self.consome(TOKEN.id)
            self.arguments()
            self.consome(TOKEN.doisPontos)
            self.standard_type()
            self.consome(TOKEN.ptoVirg)
        
        elif token_lido == 'procedure':
            self.consome(TOKEN.reservada)
            self.consome(TOKEN.id)
            self.arguments()


    def arguments(self):  # <arguments>
        
        self.consome(TOKEN.abreParentese)
        self.parameter_list()
        self.consome(TOKEN.fechaParentese)

        pass

    def parameter_list(self):  # <parameter_list>

        self.identifier_list()
        self.consome(TOKEN.doisPontos)
        self.type()
        self.resto_parameter_list()


    def resto_parameter_list(self):  # <resto_parameter_list> ->

        while token_lido == TOKEN.ptoVirg
            self.consome(TOKEN.ptoVirg)  # ;
            self.identifier_list()  # identifier_list
            self.consome(TOKEN.doisPontos)  # :
            self.type()  # type       

        pass

    def compound_statement(self):  # <compound_statement>
        
        self.consome(TOKEN.BEGIN)
        self.optional_statements()
        self.consome(TOKEN.END)

    def optional_statements(self):  # <optional_statements>
        
        self.statement_list()

        pass

    def statement_list(self):  # <statement_list>
        
        self.statement()
        self.resto_statement_list()

    def resto_statement_list(self):  # <resto_statement_list>
        
        while token_lido[0] == TOKEN.ptoVirg
            self.consome(TOKEN.ptoVirg)
            self.statement()
        
        pass

    def statement(self):  # <statement>
        
        pass

    def if_statement(self):  # <if_statement>

        self.consome(TOKEN.IF)
        self.expression()
        self.consome(TOKEN.THEN)
        self.statement()
        self.opc_else()

    def opc_else(self):  # <opc_else>

        self.consome(TOKEN.ELSE)
        self.statement()
        
        pass

    def variable(self):  # <variable>
        
        self.consome(TOKEN.id)
        self.opc_else()

    def opc_index(self):  # <opc_index>
        
        self.consome(TOKEN.abreColchete)
        self.expression()
        self.consome(TOKEN.fechaColchete)
        
        pass

    def procedure_statement(self):  # <procedure_statement>
        
        self.consome(TOKEN.id)
        self.opc_parameters


    def opc_parameters(self):  # <opc_parameters>
        
        self.consome(TOKEN.abreParentese)
        self.expression_list
        self.consome(TOKEN.fechaParentese)

        pass

    def expression_list(self):  # <expression_list>
        
        self.expression()
        self.resto_expression_list()

    def resto_expression_list(self):  # <resto_expression_list>
        
        self.consome(TOKEN.ptoVirg)
        self.expression()
        self.resto_expression_list()
        
        pass

    def expression(self):  # <expression>
        
        self.simple_expression()
        self.resto_expression()

    def resto_expression(self):  # <resto_expression>
        
        self.consome(TOKEN.relop)
        self.simple_expression()
        self.resto_expression()
        
        pass

    def simple_expression(self):  # <simple_expression>
        
        self.term()
        self.resto_simple_expression()

    def resto_simple_expression(self):  # <resto_simple_expression>
        
        while token_lido[0] == TOKEN.ADDOP:
            self.consome(TOKEN.ADDOP)
            self.term()
        
        pass

    def term(self):  # <term>

        self.uno()
        self.resto_term()

    def resto_term(self):  # <resto_term>
        
        while token_lido[0] == TOKEN.MULOP:
            self.consome(TOKEN.MULOP)
            self.uno()
        
        pass

    def uno(self):  # <uno>

        if token_lido[0] == TOKEN.ADDOP:
            self.consome(TOKEN.ADDOP)
            self.factor()
        
        else:
            self.factor()

    def factor(self):  # <factor>
        
        if token_lido[0] == TOKEN.id:
            self.consome(TOKEN.id)
            self.resto_id()
        
        elif token_lido[0] == TOKEN.numInteger:
            self.consome(TOKEN.numInteger)

        elif token_lido[0] == TOKEN.numReal:
            self.consome(TOKEN.numReal)
        
        elif token_lido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.expression()
            self.consome(TOKEN.fechaParentese)

        elif token_lido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.factor()

    def resto_id(self):  # <resto_id>
        
        self.consome(TOKEN.abreParentese)
        self.expression_list()
        self.consome(TOKEN.fechaParentese)
        
        pass

    def input_output(self):  # <inputOutput>

        if token_lido[0] == TOKEN.writeln:
            self.consome(TOKEN.writeln)
            self.consome(TOKEN.abreParentese)
            self.outputs()
            self.consome(TOKEN.fechaParentese)

        elif token_lido[0] == TOKEN.write:
            self.consome(TOKEN.write)
            self.consome(TOKEN.abreParentese)
            self.outputs()
            self.consome(TOKEN.fechaParentese)
        
        elif token_lido[0] == TOKEN.read:
            self.consome(TOKEN.read)
            self.consome(TOKEN.abreParentese)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaParentese)

        elif token_lido[0] == TOKEN.readln:
            self.consome(TOKEN.readln)
            self.consome(TOKEN.abreParentese)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaParentese)

    def outputs(self):  # <outputs>

        self.out()
        self.resto_outputs()

    def resto_outputs(self):  # <restoOutputs>
        
        self.consome(TOKEN.virg)
        self.out()
        self.resto_outputs()
        
        pass

    def out(self):  # <out>

        if token_lido[0] == TOKEN.numInteger:
            self.consome(TOKEN.numInteger)

        elif token_lido[0] == TOKEN.numReal:
            self.consome(TOKEN.numReal)

        elif token_lido[0] == TOKEN.id:
            self.consome(TOKEN.id)

        elif token_lido[0] == TOKEN.string:
            self.consome(TOKEN.string)
        pass
