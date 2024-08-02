# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (ago-2024)
# ---------------------------------------------------
from ttoken import TOKEN

class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte  # objeto file
        self.fonte = self.arqFonte.read()  # string contendo file
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None  # (token, lexema, linha, coluna)
        self.linha = 1  # linha atual no fonte
        self.coluna = 0  # coluna atual no fonte

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    def getchar(self):
        if self.fimDoArquivo():
            return 'eof'
        caractere = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
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

        if self.indiceFonte > 0:
            self.indiceFonte -= 1

        self.coluna -= 1

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    def getToken(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''
        while simbolo in ['//', ' ', '\n']:
            # descarta comentario que iniciam com //
            if simbolo == '//': # DEFININDO COMENTARIOS COMO //
                simbolo = self.getchar()
                while simbolo != '\n':
                    simbolo = self.getchar()
            # descarta lnhas em branco
            while simbolo in [' ', '\n']:
                simbolo = self.getchar()
        # aqui vai começar a pegar um token...
        lin = self.linha # onde inicia o token, para msgs
        col = self.coluna # onde inicia o token, para msgs

        while(True):
            if estado == 1:
                # inicio do automato
                if simbolo.isalpha():
                    estado = 2 # identificadores e palavras reservadas
                elif simbolo.isdigit():
                    estado = 3 # números
                elif simbolo == '"':
                    estado = 4 #strings
                elif simbolo == "(":
                    return (TOKEN.abreParentese, "(", lin, col)
                elif simbolo == ")":
                    return (TOKEN.fechaParentese, ")", lin, col)
                elif simbolo == ",":
                    return(TOKEN.virg, ",", lin, col)
                elif simbolo == ";":
                    return(TOKEN.ptoVirg, ";", lin, col)
                elif simbolo == ":":
                    return (TOKEN.doisPontos, ":", lin, col)
                elif simbolo == "..":
                    return(TOKEN.ptoPto, "..", lin, col)
                elif simbolo == "[":
                    return(TOKEN.abreColchete, "[", lin, col)
                elif simbolo == "]":
                    return(TOKEN.fechaColchete, "]", lin, col)
                elif simbolo == 'eof':
                    return(TOKEN.eof, '<eof>', lin, col)
                elif simbolo == ".": # pode ser . ou ..
                    estado = 5
                elif simbolo == "=": # pode ser =, >=, =<,
                    estado = 6

            elif estado == 2:
                #identificadores e palavras reservadas
                if simbolo.isalnum():
                    estado = 2
                else:
                    self.ungetchar(simbolo)
                    token = TOKEN.reservada(lexema)
                    return (token, lexema, lin, col)

            elif estado == 3:
                # numeros
                if simbolo.isdigit():
                    estado = 3
                elif simbolo == '.':
                    estado = 31
                elif simbolo.isalpha():
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.num, lexema, lin, col)
                
            
            elif estado == 4:
                # strings
                while True:
                    if simbolo == '"':
                        lexema += simbolo
                        return (TOKEN.string, lexema, lin, col)
                    if simbolo in ['\n', 'eof']:
                        return (TOKEN.erro, lexema, lin, col)
                    if simbolo == '\\':  # isso é por causa do python
                        lexema += simbolo
                        simbolo = self.getchar()
                        if simbolo in ['\n', '\0']:
                            return (TOKEN.erro, lexema, lin, col)

                    lexema = lexema + simbolo
                    simbolo = self.getchar()
            
            elif estado == 5: 
                if simbolo == '.':
                    lexema = lexema + simbolo
                    return (TOKEN.ptoPto, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.pto, lexema, lin, col)
                
            elif estado == 6:
                if simbolo == '=':
                    lexema = lexema + simbolo
                    return (TOKEN.RELOP, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return(TOKEN.assignop, lexema, lin, col)
                
            else:
                print('BUG!!!')

            lexema = lexema + simbolo
            simbolo = self.getchar()