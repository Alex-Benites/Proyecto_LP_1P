import ply.yacc as yacc
from lexer import tokens

# Regla inicial
start = 'programa'

# Lista global para almacenar errores sintácticos
errores_sintacticos = []

# === REGLAS GRAMATICALES PARA EL ALGORITMO DE NEHEMIAS ===

# 1. PROGRAMA PRINCIPAL
def p_programa(p):
    '''programa : TAG_INICIO sentencias TAG_FIN
                | TAG_INICIO sentencias'''
    if len(p) == 4:
        p[0] = ('programa_php', p[2])
    else:
        p[0] = ('programa_php', p[2])

# 2. LISTA DE SENTENCIAS
def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

# 3. TIPOS DE SENTENCIAS
def p_sentencia(p):
    '''sentencia : asignacion
                 | declaracion_define
                 | sentencia_echo
                 | asignacion_array'''
    p[0] = p[1]

# 4. ASIGNACIÓN DE VARIABLES
def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNAR expresion PUNTO_COMA'''
    p[0] = ('asignacion', p[1], p[3])

# 5. ASIGNACIÓN A ARRAYS (para $pila[] = $elemento1;)
def p_asignacion_array(p):
    '''asignacion_array : VARIABLE CORCHETE_IZQ CORCHETE_DER ASIGNAR expresion PUNTO_COMA'''
    p[0] = ('asignacion_array', p[1], p[5])

# 6. DECLARACIÓN DEFINE
def p_declaracion_define(p):
    '''declaracion_define : DEFINE PAREN_IZQ CADENA COMA expresion PAREN_DER PUNTO_COMA'''
    p[0] = ('define', p[3], p[5])

# 7. SENTENCIA ECHO
def p_sentencia_echo(p):
    '''sentencia_echo : ECHO expresion PUNTO_COMA'''
    p[0] = ('echo', p[2])

# 8. EXPRESIONES ARITMÉTICAS
def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULTIPLICAR expresion
                 | expresion DIVIDIR expresion'''
    p[0] = ('binaria', p[2], p[1], p[3])

def p_expresion_parentesis(p):
    '''expresion : PAREN_IZQ expresion PAREN_DER'''
    p[0] = p[2]

def p_expresion_simple(p):
    '''expresion : NUMERO
                 | CADENA
                 | VARIABLE
                 | IDENTIFICADOR'''
    p[0] = ('literal', p[1])

# 9. ARRAYS VACÍOS (para $pila = [];)
def p_expresion_array_vacio(p):
    '''expresion : CORCHETE_IZQ CORCHETE_DER'''
    p[0] = ('array_vacio', [])

# 10. ARRAYS CON ELEMENTOS
def p_expresion_array(p):
    '''expresion : CORCHETE_IZQ lista_elementos CORCHETE_DER'''
    p[0] = ('array', p[2])

def p_lista_elementos(p):
    '''lista_elementos : expresion
                      | lista_elementos COMA expresion'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

# === MANEJO DE ERRORES ===
def p_error(p):
    global errores_sintacticos
    if p:
        error_msg = f"Error sintáctico en token {p.type} ('{p.value}') en línea {p.lineno}"
        print(error_msg)
        errores_sintacticos.append(error_msg)
    else:
        error_msg = "Error sintáctico: final de archivo inesperado"
        print(error_msg)
        errores_sintacticos.append(error_msg)

# === FUNCIONES AUXILIARES ===
def limpiar_errores():
    """Limpia la lista de errores sintácticos"""
    global errores_sintacticos
    errores_sintacticos = []

def obtener_errores():
    """Obtiene la lista actual de errores sintácticos"""
    global errores_sintacticos
    return errores_sintacticos.copy()

# === CREAR EL PARSER ===
parser = yacc.yacc()