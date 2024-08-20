# ---------------------------------------------------
# Tradutor para a linguagem MiniPascal
#
# versao 1a (ago-2024)
# ---------------------------------------------------

from enum import IntEnum


class TOKEN(IntEnum):
    erro = 1 
    eof = 2
    id = 3
    VAR = 4
    numInteger = 5
    numReal = 6
    REAL = 7
    PROGRAM = 8
    FUNCTION = 9
    PROCEDURE = 10  # FUNCÃO VOID
    assignop = 11  # operador de atribuição
    INTEGER = 12

    BEGIN = 13
    END = 14
    ARRAY = 15
    WHILE = 16
    DO = 17
    IF = 18
    THEN = 19
    ELSE = 20
    NOT = 21

    virg = 22
    ptoVirg = 23
    pto = 24
    ptoPto = 25
    abreColchete = 26
    fechaColchete = 27
    abreParentese = 28
    fechaParentese = 29
    doisPontos = 30

    relop = 31  # menor ou igual, menor, igual, maior ou igual, maior
    mulop = 32  # multiplicacao, divisao e mod
    addop = 33  # adição e subtração
    OF = 34  # array de um tipo

    string = 35
    WRITE = 36
    WRITELN = 37
    READ = 38
    READLN = 39
    RETURN = 40

    @classmethod
    def msg(cls, token):
        nomes = {
            1: 'erro',
            2: '<eof>',
            3: 'identificador',
            4: 'variavel',
            5: 'numero inteiro',
            6: 'número real',
            7: 'real',
            8: 'program',
            9: 'function',
            10: 'procedure',
            11: ':=',
            12: 'inteiro',
            13: 'begin',
            14: 'end',
            15: 'array',
            16: 'while',
            17: 'do',
            18: 'if',
            19: 'then',
            20: 'else',
            21: 'not',
            22: ',',
            23: ';',
            24: '.',
            25: '..',
            26: '[',
            27: ']',
            28: '(',
            29: ')',
            30: ':',
            31: 'operador relacional (<=, <, =, >, =>)',
            32: 'operador de multiplicação (*, /, mod)',
            33: 'operador de soma (+, -)',
            34: 'of',
            35: 'string',
            36: 'write',
            37: 'writeln',
            38: 'read',
            39: 'readln',
            40: 'return'
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'program': TOKEN.PROGRAM,
            'if': TOKEN.IF,
            'while': TOKEN.WHILE,
            'begin': TOKEN.BEGIN,
            'end': TOKEN.END,
            'else': TOKEN.ELSE,
            'var': TOKEN.VAR,
            'not': TOKEN.NOT,
            'real': TOKEN.REAL,
            'function': TOKEN.FUNCTION,
            'procedure': TOKEN.PROCEDURE,
            'integer': TOKEN.INTEGER,
            'array': TOKEN.ARRAY,
            'do': TOKEN.DO,
            'then': TOKEN.THEN,
            'mod': TOKEN.mulop,
            'div': TOKEN.mulop,
            'of': TOKEN.OF,
            'read': TOKEN.READ,
            'readln': TOKEN.READLN,
            'write': TOKEN.WRITE,
            'writeln': TOKEN.WRITELN,
            'return': TOKEN.RETURN

        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.id
