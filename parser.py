import ply.yacc as yacc
from lexer import tokens

# Regla inicial
start = 'programa'

errores_sintacticos = []

def p_programa(p):
    '''programa : TAG_INICIO sentencias TAG_FIN
                | TAG_INICIO sentencias'''
    p[0] = ('programa_php', p[2])

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_sentencia(p):
    '''sentencia : asignacion
                 | declaracion_define
                 | sentencia_echo
                 | asignacion_array
                 | sentencia_if
                 | sentencia_foreach
                 | sentencia_funcion
                 | sentencia_return
                 | sentencia_llamada_funcion
                 | sentencia_incremento
                 | sentencia_comentario'''
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNAR expresion PUNTO_COMA'''
    p[0] = ('asignacion', p[1], p[3])

def p_asignacion_array(p):
    '''asignacion_array : VARIABLE CORCHETE_IZQ CORCHETE_DER ASIGNAR expresion PUNTO_COMA'''
    p[0] = ('asignacion_array', p[1], p[5])

def p_declaracion_define(p):
    '''declaracion_define : DEFINE PAREN_IZQ CADENA COMA expresion PAREN_DER PUNTO_COMA'''
    p[0] = ('define', p[3], p[5])

def p_sentencia_echo(p):
    '''sentencia_echo : ECHO expresion PUNTO_COMA'''
    p[0] = ('echo', p[2])

def p_sentencia_if(p):
    '''sentencia_if : IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
                    | IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE LLAVE_IZQ sentencias LLAVE_DER'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6], None)  # if sin else
    else:
        p[0] = ('if_else', p[3], p[6], p[10])  # if con else

def p_condicion(p):
    '''condicion : expresion IGUAL expresion
                 | expresion NO_IGUAL expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion'''
    p[0] = ('condicion', p[2], p[1], p[3])

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

# Expresión para llamada a función sin punto y coma, para uso dentro de expresiones
def p_expresion_llamada_funcion(p):
    '''expresion : IDENTIFICADOR PAREN_IZQ lista_argumentos PAREN_DER'''
    p[0] = ('llamada_funcion', p[1], p[3])

def p_expresion_array(p):
    '''expresion : CORCHETE_IZQ elementos_array_coma_opt CORCHETE_DER'''
    p[0] = ('array', p[2])

def p_elementos_array_coma_opt(p):
    '''elementos_array_coma_opt : elementos_array
                               | elementos_array COMA
                               | '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = []

def p_elementos_array(p):
    '''elementos_array : elemento_array
                      | elementos_array COMA elemento_array'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_elemento_array(p):
    '''elemento_array : expresion
                     | CADENA ARRAY_ASOCIATIVO expresion'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('asociativo', p[1], p[3])

def p_expresion_acceso_array(p):
    '''expresion : VARIABLE CORCHETE_IZQ expresion CORCHETE_DER'''
    p[0] = ('acceso_array', p[1], p[3])

def p_expresion_concatenacion(p):
    '''expresion : expresion PUNTO expresion'''
    p[0] = ('concatenacion', p[1], p[3])

def p_sentencia_incremento(p):
    '''sentencia_incremento : VARIABLE MAS MAS PUNTO_COMA'''
    p[0] = ('incremento', p[1])

def p_sentencia_foreach(p):
    '''sentencia_foreach : FOREACH PAREN_IZQ VARIABLE AS VARIABLE PAREN_DER LLAVE_IZQ sentencias LLAVE_DER'''
    p[0] = ('foreach', p[3], p[5], p[8])

def p_sentencia_funcion(p):
    '''sentencia_funcion : FUNCTION IDENTIFICADOR PAREN_IZQ parametros_funcion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER'''
    p[0] = ('funcion', p[2], p[4], p[7])

def p_parametros_funcion(p):
    '''parametros_funcion : VARIABLE
                         | parametros_funcion COMA VARIABLE
                         | '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = []

def p_sentencia_return(p):
    '''sentencia_return : RETURN expresion PUNTO_COMA'''
    p[0] = ('return', p[2])

def p_sentencia_llamada_funcion(p):
    '''sentencia_llamada_funcion : IDENTIFICADOR PAREN_IZQ lista_argumentos PAREN_DER PUNTO_COMA'''
    p[0] = ('llamada_funcion', p[1], p[3])

def p_lista_argumentos(p):
    '''lista_argumentos : expresion
                       | lista_argumentos COMA expresion
                       | '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = []

def p_sentencia_comentario(p):
    '''sentencia_comentario : '''
    pass

def p_error(p):
    global errores_sintacticos
    if p:
        print(f"Contexto: {p.lexer.lexdata[max(0, p.lexpos-20):p.lexpos+20]}")
        error_msg = f"Error sintáctico en token {p.type} ('{p.value}') en línea {p.lineno}"
        print(error_msg)
        errores_sintacticos.append(error_msg)
    else:
        error_msg = "Error sintáctico: final de archivo inesperado"
        print(error_msg)
        errores_sintacticos.append(error_msg)

def limpiar_errores():
    global errores_sintacticos
    errores_sintacticos = []

def obtener_errores():
    global errores_sintacticos
    return errores_sintacticos.copy()

parser = yacc.yacc()
