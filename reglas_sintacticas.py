import ply.yacc as yacc
from lexer import tokens

# Regla inicial
start = 'programa'

# 1. REGLAS PARA IMPRESIÓN
def p_sentencia_impresion(p):
    '''sentencia : ECHO expresion PUNTO_COMA
                 | PRINT expresion PUNTO_COMA'''
    p[0] = ('impresion', p[1], p[2])

# 2. REGLAS PARA INGRESO DE DATOS
def p_sentencia_input(p):
    '''sentencia : VARIABLE ASIGNAR READLINE PAREN_IZQ PAREN_DER PUNTO_COMA
                 | VARIABLE ASIGNAR READLINE PAREN_IZQ CADENA PAREN_DER PUNTO_COMA'''
    if len(p) == 7:
        p[0] = ('input_simple', p[1])
    else:
        p[0] = ('input_prompt', p[1], p[5])

# 3. REGLAS PARA EXPRESIONES ARITMÉTICAS
def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICAR expresion
                 | expresion DIVIDIR expresion'''
    p[0] = ('operacion_binaria', p[2], p[1], p[3])

def p_expresion_parentesis(p):
    '''expresion : PAREN_IZQ expresion PAREN_DER'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : NUMERO'''
    p[0] = ('numero', p[1])

def p_expresion_variable(p):
    '''expresion : VARIABLE'''
    p[0] = ('variable', p[1])

# 4. REGLA PRINCIPAL DEL PROGRAMA
def p_programa(p):
    '''programa : MENOR IDENTIFICADOR MAYOR sentencias MENOR DIVIDIR IDENTIFICADOR MAYOR'''
    p[0] = ('programa_php', p[4])

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

# Manejo de errores
def p_error(p):
    if p:
        print(f"Error sintáctico en token {p.type} ('{p.value}') en línea {p.lineno}")
    else:
        print("Error sintáctico: final de archivo inesperado")

# Construir el parser
parser = yacc.yacc()