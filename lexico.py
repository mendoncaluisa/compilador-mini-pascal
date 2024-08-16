# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (ago-2024)
# ---------------------------------------------------
from ttoken import TOKEN


class Lexico:
        
    def __init__(self, arqfonte):
        self.arqfonte = arqfonte  # objeto file
        self.fonte = self.arqfonte.read()  # string contendo file
        self.tam_fonte = len(self.fonte)
        self.indice_fonte = 0
        self.token_lido = None  # (token, lexema, linha, coluna)
        self.linha = 1  # linha atual no fonte
        self.coluna = 0  # coluna atual no fonte

    def fim_do_arquivo(self):
        return self.indice_fonte >= self.tam_fonte

    def getchar(self):
        if self.fim_do_arquivo():
            return '\0'
        caractere = self.fonte[self.indice_fonte]
        self.indice_fonte += 1
        if caractere == '\n':
            self.linha += 1
            # colocar self.coluna = 1 também está funcionando, ver qual dos dois está realmente certo
            self.coluna = 0
        else:
            self.coluna += 1
        return caractere

    def ungetchar(self, simbolo):
        if simbolo == '\n':
            self.linha -= 1

        if simbolo == '\0':
            return

        if self.indice_fonte > 0:
            self.indice_fonte -= 1

        self.coluna -= 1

    def imprime_token(self, token_corrente):
        (token, lexema, linha, coluna) = token_corrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    def get_token(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''

        while simbolo in ['/', '\t', ' ', '\n']:
            if simbolo == '/':
                simbolo = self.getchar()
                if simbolo == '/':
                    # comentario
                    simbolo = self.getchar()
                    while simbolo != '\n':
                        simbolo = self.getchar()
                else: 
                    estado = 9
            while simbolo in [' ', '\t', '\n']:
                simbolo = self.getchar()

        # aqui vai começar a pegar um token...
        lin = self.linha  # onde inicia o token, para msgs
        col = self.coluna  # onde inicia o token, para msgs

        while True:
            if estado == 1:
                # inicio do automato
                if simbolo.isalpha():
                    estado = 2  # identificadores e palavras reservadas
                elif simbolo.isdigit():
                    estado = 3  # números
                elif simbolo == '':
                    estado = 4  # strings
                elif simbolo == "(":
                    return TOKEN.abreParentese, "(", lin, col
                elif simbolo == ")":
                    return TOKEN.fechaParentese, ")", lin, col
                elif simbolo == ",":
                    return TOKEN.virg, ",", lin, col
                elif simbolo == ";":
                    return TOKEN.ptoVirg, ";", lin, col
                elif simbolo == ":":
                    estado = 6
                elif simbolo == "..":
                    return TOKEN.ptoPto, "..", lin, col
                elif simbolo == "[":
                    return TOKEN.abreColchete, "[", lin, col
                elif simbolo == "]":
                    return TOKEN.fechaColchete, "]", lin, col
                elif simbolo == '\0':
                    return TOKEN.eof, '<eof>', lin, col
                elif simbolo == ".":  # pode ser . ou ..
                    estado = 5
                elif simbolo == "=":  #
                    return TOKEN.relop, '=', lin, col
                elif simbolo == ">":  # pode ser >=,  >
                    estado = 7
                elif simbolo == "<":  # pode ser <, <=
                    estado = 8
                elif simbolo == "*": 
                    return TOKEN.MULOP, "*", lin, col

            elif estado == 2:
                # identificadores e palavras reservadas
                if simbolo.isalnum():
                    estado = 2
                else:
                    self.ungetchar(simbolo)
                    token = TOKEN.reservada(lexema)
                    return token, lexema, lin, col

            elif estado == 3:
                # numeros
                if simbolo.isdigit():
                    estado = 3
                elif simbolo == '.':  # tratando de casos que sejam numero de ponto flutuante
                    estado = 31
                elif simbolo.isalpha():
                    lexema += simbolo
                    return TOKEN.erro, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.numInteger, lexema, lin, col
                
            elif estado == 31:
                # parte real do numero
                if simbolo.isdigit():
                    estado = 32
                elif simbolo == '.':
                    self.ungetchar(simbolo)
                    self.ungetchar(simbolo)
                    # lexema += simbolo
                    lexema = lexema[: - 1]
                    return TOKEN.numInteger, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.erro, lexema, lin, col
            elif estado == 32:
                # parte real do numero
                if simbolo.isdigit():
                    estado = 32
                elif simbolo.isalpha():
                    lexema += simbolo
                    return TOKEN.erro, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.numReal, lexema, lin, col
                    
            elif estado == 4:
                # strings
                while True:
                    if simbolo == '"':
                        lexema += simbolo
                        return TOKEN.string, lexema, lin, col
                    if simbolo in ['\n', '\0']:
                        return TOKEN.erro, lexema, lin, col
                    if simbolo == '\\':  # isso é por causa do python
                        lexema += simbolo
                        simbolo = self.getchar()
                        if simbolo in ['\n', '\0']:
                            return TOKEN.erro, lexema, lin, col

                    lexema = lexema + simbolo
                    simbolo = self.getchar()
            
            elif estado == 5:
                if simbolo == '.':  # tratando de casos que sejam '..' ou '.'
                    lexema = lexema + simbolo
                    return TOKEN.ptoPto, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.pto, lexema, lin, col
                
            elif estado == 6:
                if simbolo == '=':  # tratando de casos que sejam ':= ' ou ':'
                    lexema = lexema + simbolo
                    return TOKEN.assignop, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.doisPontos, lexema, lin, col

            elif estado == 7:
                if simbolo == '=':  # tratando casos de > ou >=
                    lexema = lexema + simbolo
                    return TOKEN.relop, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.relop, lexema, lin, col

            elif estado == 8:
                if simbolo == '=':  # tratando casos de < ou <=
                    lexema = lexema + simbolo
                    return TOKEN.relop, lexema, lin, col
                else:
                    self.ungetchar(simbolo)
                    return TOKEN.relop, lexema, lin, col
                
            elif estado == 9:
                return TOKEN.MULOP, '/', lin, col
            else:
                print('BUG!!!')

            lexema = lexema + simbolo
            simbolo = self.getchar()
