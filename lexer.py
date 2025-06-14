# clase de introduccion nomas

import ply.lex as lex
import ply.yacc as yacc

# Definir tokens
tokens = ['NUMBER', 'PLUS', 'MINUS']

# Reglas del lexer
t_PLUS = r'\+'
t_MINUS = r'-'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabs
t_ignore = ' \t'

# Manejo de errores (obligatorio en PLY)
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Probar el lexer
if __name__ == "__main__":
    data = "3 + 5 - 2"
    lexer.input(data)

    print(f"Analizando: {data}")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Token: {tok.type}, Valor: {tok.value}")