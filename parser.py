import ply.yacc as yacc
from lexer import tokens

start = 'programa'

errores_sintacticos = []
errores_semanticos = []

tabla_simbolos = {}
tabla_tipos_arrays = {}

def p_programa(p):
    '''programa : TAG_INICIO sentencias TAG_FIN
                | TAG_INICIO sentencias'''
    p[0] = ('programa_php', p[2])

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

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
    var = p[1]
    expr = p[3]
    tipo = tipo_expresion(expr)
    if tipo is None:
        registrar_error_semantico(f"Error semántico: No se puede determinar el tipo de la expresión para {var}")
        tipo = 'mixed'
    if var in tabla_simbolos:
        if (tabla_simbolos[var], tipo) in [('int', 'float'), ('float', 'int')]:
            tabla_simbolos[var] = tipo
        elif tabla_simbolos[var] != tipo:
            registrar_error_semantico(f"Error semántico: Asignación incompatible para {var}. Esperado {tabla_simbolos[var]}, encontrado {tipo}")
        else:
            tabla_simbolos[var] = tipo
    else:
        tabla_simbolos[var] = tipo
    p[0] = ('asignacion', var, expr)

def p_asignacion_array(p):
    '''asignacion_array : VARIABLE CORCHETE_IZQ CORCHETE_DER ASIGNAR expresion PUNTO_COMA'''
    var = p[1]
    expr = p[5]
    tipo = tipo_expresion(expr)
    if var not in tabla_simbolos:
        tabla_simbolos[var] = 'array'
        tabla_tipos_arrays[var] = {}
    elif tabla_simbolos[var] != 'array':
        registrar_error_semantico(f"Error semántico: {var} ya fue declarado con un tipo incompatible con array.")
    p[0] = ('asignacion_array', var, expr)

def p_declaracion_define(p):
    '''declaracion_define : DEFINE PAREN_IZQ CADENA COMA expresion PAREN_DER PUNTO_COMA'''
    p[0] = ('define', p[3], p[5])

def p_sentencia_echo(p):
    '''sentencia_echo : ECHO expresion PUNTO_COMA'''
    p[0] = ('echo', p[2])

def p_sentencia_if(p):
    '''sentencia_if : IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER
                    | IF PAREN_IZQ condicion PAREN_DER LLAVE_IZQ sentencias LLAVE_DER ELSE LLAVE_IZQ sentencias LLAVE_DER'''
    p[0] = ('if', p[3], p[6], None) if len(p) == 8 else ('if_else', p[3], p[6], p[10])

def p_condicion(p):
    '''condicion : expresion IGUAL expresion
                 | expresion NO_IGUAL expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion
                 | IDENTIFICADOR PAREN_IZQ lista_argumentos PAREN_DER'''
    if len(p) == 4:
        p[0] = ('condicion', p[2], p[1], p[3])
    else:
        p[0] = ('condicion_funcion', p[1], p[3])

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
    if isinstance(p[1], str) and p[1].startswith('$'):
        if p[1] not in tabla_simbolos:
            registrar_error_semantico(f"Error semántico: Variable {p[1]} no declarada. Debe asignarse antes de usarse.")
        p[0] = ('literal', p[1])
    else:
        p[0] = ('literal', p[1])

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
    p[0] = p[1] if len(p) in [2, 3] else []

def p_elementos_array(p):
    '''elementos_array : elemento_array
                      | elementos_array COMA elemento_array'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_elemento_array(p):
    '''elemento_array : expresion
                     | CADENA ARRAY_ASOCIATIVO expresion'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        clave = p[1].strip('"')
        valor = p[3]
        tipo_valor = tipo_expresion(valor)
        array_name = '$persona'  # <- Puedes hacer esto dinámico si lo deseas
        if array_name not in tabla_tipos_arrays:
            tabla_tipos_arrays[array_name] = {}
        tabla_tipos_arrays[array_name][clave] = tipo_valor
        p[0] = ('asociativo', clave, valor)


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
    
    nombre_funcion = p[2]
    parametros = p[4]

    # Guardamos el estado de la tabla de símbolos (ámbito global)
    tabla_simbolos_global = tabla_simbolos.copy()

    # Creamos ámbito local y registramos los parámetros como variables válidas
    for param in parametros:
        if param.startswith('$'):
            tabla_simbolos[param] = 'mixed'  # Tipo por defecto

    cuerpo = p[7]
    p[0] = ('funcion', nombre_funcion, parametros, cuerpo)

    # Restauramos el estado global del ámbito
    tabla_simbolos.clear()
    tabla_simbolos.update(tabla_simbolos_global)


def p_parametros_funcion(p):
    '''parametros_funcion : VARIABLE
                         | parametros_funcion COMA VARIABLE
                         | '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
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
    p[0] = [p[1]] if len(p) == 2 else (p[1] + [p[3] if len(p) == 4 else []])

def p_sentencia_comentario(p):
    '''sentencia_comentario : '''
    pass

def p_error(p):
    if p:
        contexto = p.lexer.lexdata[max(0, p.lexpos - 20):p.lexpos + 20]
        error_msg = f"Error sintáctico en token {p.type} ('{p.value}') en línea {p.lineno}"
        print("Contexto:", contexto)
        print(error_msg)
        errores_sintacticos.append(error_msg)
    else:
        error_msg = "Error sintáctico: final de archivo inesperado"
        print(error_msg)
        errores_sintacticos.append(error_msg)

def registrar_error_semantico(msg):
    errores_semanticos.append(msg)

def obtener_errores():
    return errores_sintacticos.copy()

def obtener_errores_semanticos():
    return errores_semanticos.copy()

def limpiar_errores():
    errores_sintacticos.clear()

def limpiar_errores_semanticos():
    errores_semanticos.clear()

def limpiar_tabla_simbolos():
    tabla_simbolos.clear()

def limpiar_tabla_tipos_arrays():
    tabla_tipos_arrays.clear()

def tipo_expresion(expr):
    if isinstance(expr, tuple):
        if expr[0] == 'literal':
            valor = expr[1]
            if isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit()):
                return 'int'
            elif isinstance(valor, float):
                return 'float'
            elif isinstance(valor, str) and valor.startswith('"') and valor.endswith('"'):
                return 'string'
            elif isinstance(valor, str) and valor.startswith('$'):
                return tabla_simbolos.get(valor, None)
        elif expr[0] == 'binaria':
            t1 = tipo_expresion(expr[2])
            t2 = tipo_expresion(expr[3])
            if expr[1] == '/' and t1 in ('int', 'float') and t2 in ('int', 'float'):
                return 'float'
            return t1 if t1 == t2 and t1 is not None else 'mixed'
        elif expr[0] == 'array':
            return 'array'
        elif expr[0] == 'llamada_funcion':
            if expr[1] == 'count':
                return 'int'
            if expr[1] == 'array_shift':
                return 'string'
            return 'mixed'
        elif expr[0] == 'acceso_array':
            array_var = expr[1]
            clave_expr = expr[2]
            clave = None
            if isinstance(clave_expr, tuple) and clave_expr[0] == 'literal':
                clave = clave_expr[1]
                if isinstance(clave, str) and clave.startswith('"') and clave.endswith('"'):
                    clave = clave.strip('"')
            if clave and array_var in tabla_tipos_arrays and clave in tabla_tipos_arrays[array_var]:
                return tabla_tipos_arrays[array_var][clave]
            return 'mixed'
    elif isinstance(expr, str) and expr.startswith('$'):
        return tabla_simbolos.get(expr, None)
    elif isinstance(expr, int):
        return 'int'
    elif isinstance(expr, float):
        return 'float'
    return None

parser = yacc.yacc()
