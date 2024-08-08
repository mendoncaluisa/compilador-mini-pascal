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
        self.identificador_lista()  # <identifier_list>
        self.consome(TOKEN.fechaParentese)
        self.consome(TOKEN.ptoVirg)
        self.declaracoes()  # <declarations>
        self.declaracao_subprograma()  # <subprogram_declarations>
        self.comando_composto()  # <compound_statement>
        self.consome(TOKEN.pto)

    def identificador_lista(self):  # <identifier_list>
        pass

    def resto_identificador_lista(self):  # <resto_identifier_list>
        pass

    def declaracoes(self):  # <declarations>
        pass

    def tipo(self):  # <type>
        pass

    def standard_tipo(self):  # <standard_type>
        pass

    def declaracoes_subprgrama(self):  # <subprogram_declarations>
        pass

    def declaracao_subprograma(self):  # <subprogram_declaration>
        pass

    def cabecalho_subprograma(self):  # <subprogram_head>
        pass

    def argumentos(self):  # <arguments>
        pass

    def parametros_lista(self):  # <parameter_list>
        pass

    def resto_parametros_lista(self):  # <resto_parameter_list> ->
        pass

    def comando_composto(self):  # <compound_statement>
        pass

    def comando_opcional(self):  # <optional_statements>
        pass

    def comando_list(self):  # <statement_list>
        pass

    def resto_comando_lista(self):  # <resto_statement_list>
        pass

    def comando(self):  # <statement>
        pass

    def comando_if(self):  # <if_statement>
        pass

    def else_opcional(self):  # <opc_else>
        pass

    def variavel(self):  # <variable>
        pass

    def index_opcional(self):  # <opc_index>
        pass

    def procedimento_comando(self):  # <procedure_statement>
        pass

    def parametros_opcionais(self):  # <opc_parameters>
        pass

    def lista_expressao(self):  # <expression_list>
        pass

    def resto_lista_expressao(self):  # <resto_expression_list>
        pass

    def expressao(self):  # <expression>
        pass

    def resto_expressao(self):  # <resto_expression>
        pass

    def expressao_simples(self):  # <simple_expression>
        pass

    def resto_expressao_simples(self):  # <resto_simple_expression>
        pass

    def termo(self):  # <term>
        pass

    def resto_termo(self):  # <resto_term>
        pass

    def uno(self):  # <uno>
        pass

    def fator(self):  # <factor>
        pass

    def resto_identificador(self):  # <resto_id>
        pass

    def entrada_saida(self):  # <inputOutput>
        pass

    def saidas(self):  # <outputs>
        pass

    def resto_saidas(self):  # <restoOutputs>
        pass

    def saida(self):  # <out>
        pass
