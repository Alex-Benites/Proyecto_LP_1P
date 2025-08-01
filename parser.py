import ply.yacc as yacc
from lexer import tokens

start = 'programa'

errores_sintacticos = []
errores_semanticos = []

tabla_simbolos = {}
tabla_tipos_arrays = {}
pila_simbolos = [tabla_simbolos]  # Manejamos scopes con una pila

# Conjunto para almacenar nombres de funciones definidas
funciones_definidas = set()
# Diccionario para almacenar funciones y sus cuerpos
firma_funciones = {}

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
                 | sentencia_comentario
                 | operacion_pila'''  # ✅ AGREGAR ESTA LÍNEA
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNAR expresion PUNTO_COMA'''
    var = p[1]
    expr = p[3]
    tipo = tipo_expresion(expr)
    tabla_simbolos[var] = tipo  # <-- Guarda el tipo, no el valor
    p[0] = ('asignacion', var, expr)

    if len(p) == 5:  # Asignación simple: $var = expresion;
        expr = p[3]
        if isinstance(expr, tuple) and expr[0] == 'binaria':
            # Si es una expresión binaria como 0 - 1
            operador = expr[1]
            izq = expr[2]
            der = expr[3]

            if (operador == '-' and
                isinstance(izq, tuple) and izq[0] == 'literal' and
                isinstance(der, tuple) and der[0] == 'literal'):

                val_izq = izq[1]
                val_der = der[1]

                if isinstance(val_izq, (int, float)) and isinstance(val_der, (int, float)):
                    resultado = val_izq - val_der
                    tabla_simbolos[var] = resultado
                else:
                    tabla_simbolos[var] = 'mixed'

        # REGISTRO DE CLAVES PARA ARRAYS ASOCIATIVOS
        if isinstance(expr, tuple) and expr[0] == 'array':
            tabla_tipos_arrays[var] = {}
            for elemento in expr[1]:
                if isinstance(elemento, tuple) and elemento[0] == 'asociativo':
                    clave = elemento[1]
                    valor = elemento[2]
                    tabla_tipos_arrays[var][clave] = tipo_expresion(valor)
        p[0] = ('asignacion', var, expr)

    elif len(p) == 7 and p[3] == 'array_pop':  # $var = array_pop($array);
        array_var = p[5]
        tabla_simbolos[var] = 'mixed'  # Resultado de array_pop
        p[0] = ('asignacion_array_pop', var, array_var)

    elif len(p) == 8:  # Asignación con llamada a función: $var = funcion(args);
        nombre_funcion = p[3]
        argumentos = p[5]
        tabla_simbolos[var] = 'mixed'
        p[0] = ('asignacion_funcion', var, nombre_funcion, argumentos)

    elif len(p) == 9 and p[3] == 'array_push':  # $var = array_push($array, elemento);
        array_var = p[5]
        elemento = p[7]
        tabla_simbolos[var] = 'mixed'  # Resultado de array_push
        p[0] = ('asignacion_array_push', var, array_var, elemento)


def p_asignacion_array(p):
    '''asignacion_array : VARIABLE CORCHETE_IZQ CORCHETE_DER ASIGNAR expresion PUNTO_COMA'''
    var = p[1]
    expr = p[5]
    tipo = tipo_expresion(expr)
    if var not in tabla_simbolos:
        tabla_simbolos[var] = 'array'
        tabla_tipos_arrays[var] = {}
        # Si expr es un array asociativo, registra sus claves
        if isinstance(expr, tuple) and expr[0] == 'array':
            for elemento in expr[1]:
                if isinstance(elemento, tuple) and elemento[0] == 'asociativo':
                    clave = elemento[1]
                    valor = elemento[2]
                    tabla_tipos_arrays[var][clave] = tipo_expresion(valor)
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

    expresion_binaria = ('binaria', p[2], p[1], p[3])

    t1 = tipo_expresion(p[1])
    t2 = tipo_expresion(p[3])

    tipos_validos = ('int', 'float', 'string', 'array')
    # Solo reporta error si ambos tipos son válidos y distintos, y no son ambos numéricos
    if t1 in tipos_validos and t2 in tipos_validos and t1 != t2:
        # int y float son compatibles
        if not (t1 in ('int', 'float') and t2 in ('int', 'float')):
            registrar_error_semantico(f"Error semántico: operación '{p[2]}' entre tipos incompatibles ({t1}, {t2})")

    validar_division_por_cero(expresion_binaria)

    p[0] = expresion_binaria

def p_expresion_parentesis(p):
    '''expresion : PAREN_IZQ expresion PAREN_DER'''
    p[0] = p[2]

def p_expresion_simple(p):
    '''expresion : NUMERO
                 | CADENA
                 | VARIABLE
                 | IDENTIFICADOR'''
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
        # NO REGISTRES AQUÍ, solo retorna el elemento
        p[0] = ('asociativo', clave, valor)

def p_expresion_count(p):
    '''expresion : COUNT PAREN_IZQ VARIABLE PAREN_DER'''
    p[0] = ('count', p[3])


def p_expresion_acceso_array(p):
    '''expresion : VARIABLE CORCHETE_IZQ expresion CORCHETE_DER'''

    # ✅ LLAMAR a la validación de acceso seguro de Alex
    validar_acceso_array_seguro(p[1], p[3])

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
    cuerpo = p[7]

    # Crear nuevo ámbito local
    nuevo_ambito = {}
    pila_simbolos.append(nuevo_ambito)

    # Guardar firma de la función
    firma_funciones[nombre_funcion] = len(parametros)

    # Regla semántica: No permitir redefinir funciones (Nehemias Lindao)
    if nombre_funcion in funciones_definidas:
        registrar_error_semantico(f"Error semántico: La función '{nombre_funcion}' ya está definida.")
    else:
        funciones_definidas.add(nombre_funcion)



    # Registrar los parámetros en el ámbito local
    for param in parametros:
        if param.startswith('$'):
            nuevo_ambito[param] = 'mixed'  # tipo genérico; puedes inferir si lo deseas

    # Análisis semántico del cuerpo de la función usando el nuevo ámbito
    for stmt in cuerpo:
        if isinstance(stmt, tuple):
            if stmt[0] == 'asignacion':
                _, var, expr = stmt
                tipo = tipo_expresion(expr, simbolos=nuevo_ambito)
                if tipo is None:
                    registrar_error_semantico(f"Error semántico: No se puede determinar el tipo de {var} en la función {nombre_funcion}")
                    tipo = 'mixed'
                nuevo_ambito[var] = tipo
            elif stmt[0] == 'return':
                tipo_expresion(stmt[1], simbolos=nuevo_ambito)

    # Salimos del ámbito local
    pila_simbolos.pop()

    # Guardamos el resultado en la estructura del árbol sintáctico
    p[0] = ('funcion', nombre_funcion, parametros, cuerpo)

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
    nombre_funcion = p[1]
    argumentos = p[3]

    # Regla semántica: Verificar número de argumentos (Nehemias Lindao)
    if nombre_funcion in firma_funciones:
        esperados = firma_funciones[nombre_funcion]
        recibidos = len(argumentos)
        if esperados != recibidos:
            registrar_error_semantico(
                f"Error semántico: La función '{nombre_funcion}' espera {esperados} argumentos, pero se recibieron {recibidos}."
            )

    # Regla semántica: Underflow de cola (Nehemias Lindao)
    if nombre_funcion == "desencolar":
        # Busca el valor de $contador en el ámbito global
        contador_val = tabla_simbolos.get("$contador", None)
        if contador_val == 0:
            registrar_error_semantico("Error semántico: No se puede desencolar, la cola está vacía (underflow).")

    # Regla semántica: Overflow de cola (Nehemias Lindao)
    if nombre_funcion == "encolar":
        contador_val = tabla_simbolos.get("$contador", None)
        max_val = tabla_simbolos.get("TAMAÑO_MAXIMO", 5)  # ✅ Buscar directamente

        if contador_val is not None and contador_val >= max_val:  # ✅ Cambiar == por >=
            registrar_error_semantico("Error semántico: No se puede encolar, la cola está llena (overflow).")

    p[0] = ('llamada_funcion', nombre_funcion, argumentos)


def p_lista_argumentos(p):
    '''lista_argumentos : expresion
                        | lista_argumentos COMA expresion
                        | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

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
    print("SEMANTIC ERROR:", msg)  # <-- temporal
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

def tipo_expresion(expr, simbolos=None):
    if simbolos is None:
        simbolos = tabla_simbolos
    if isinstance(expr, str) and expr.startswith('$'):
        return simbolos.get(expr, None)
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
                # Busca el tipo en la tabla de símbolos
                return simbolos.get(valor, None)
        elif expr[0] == 'binaria':
            t1 = tipo_expresion(expr[2], simbolos)
            t2 = tipo_expresion(expr[3], simbolos)
            if expr[1] == '/' and t1 in ('int', 'float') and t2 in ('int', 'float'):
                pass
            return t1 if t1 == t2 and t1 is not None else 'mixed'
        elif expr[0] == 'array':
            return 'array'
        elif expr[0] == 'llamada_funcion':
            return 'mixed'
        elif expr[0] == 'acceso_array':
            return 'mixed'
    elif isinstance(expr, str) and expr.startswith('$'):
        return simbolos.get(expr, None)
    elif isinstance(expr, int):
        return 'int'
    elif isinstance(expr, float):
        return 'float'
    return None



# === INICIO CONTRIBUCIÓN ALEX - Reglas sintácticas para PILA ===

# Regla sintactica 1: Verificar que la pila existe
def p_operacion_pila(p):
    '''operacion_pila : operacion_push
                     | operacion_pop'''
    p[0] = p[1]


# Regla sintactica 2
def p_operacion_push(p):
    '''operacion_push : ARRAY_PUSH PAREN_IZQ VARIABLE COMA expresion PAREN_DER PUNTO_COMA
                     | PUSH PAREN_IZQ VARIABLE COMA expresion PAREN_DER PUNTO_COMA'''
    # Validar sintaxis de operación push
    p[0] = ('push', p[3], p[5])

# Regla sintactica 3
def p_operacion_pop(p):
    '''operacion_pop : ARRAY_POP PAREN_IZQ VARIABLE PAREN_DER PUNTO_COMA
                    | POP PAREN_IZQ VARIABLE PAREN_DER PUNTO_COMA'''
    # Verificar underflow de pila
    validar_underflow_pila(p[3])
    p[0] = ('pop', p[3])


# === FIN CONTRIBUCIÓN ALEX ===

# === REGLAS SEMÁNTICAS ESPECÍFICAS PARA PILA DE ALEX ===

def validar_underflow_pila(pila_var):
    """
    Primera regla semántica de Alex: Verificar underflow en operaciones pop
    """
    tamaño_actual = tabla_simbolos.get(f"{pila_var}_tamaño", 0)

    if isinstance(tamaño_actual, int) and tamaño_actual <= 0:
        registrar_error_semantico(f"Error semántico: Underflow de pila {pila_var} - no se puede hacer pop en pila vacía.")
        return True
    return False


def validar_division_por_cero(expr):
    """
    Segunda regla semántica de Alex: Detectar división por cero
    """
    if isinstance(expr, tuple) and expr[0] == 'binaria':
        operador = expr[1]
        operando_izq = expr[2]
        operando_der = expr[3]

        if operador == '/':
            if isinstance(operando_der, tuple) and operando_der[0] == 'literal':
                valor = operando_der[1]
                if valor == 0 or valor == 0.0:
                    registrar_error_semantico("Error semántico: División por cero detectada.")
                    return True
    return False

def validar_acceso_array_seguro(variable_array, indice_expr):
    """
    Tercera regla semántica de Alex: Validar acceso seguro a arrays
    SOLO SE APLICA a la variable $pila (específica de Alex)
    """

    # VALIDACIÓN PARA ARRAYS ASOCIATIVOS
    if variable_array in tabla_tipos_arrays:
        # Solo si el índice es una cadena
        if isinstance(indice_expr, tuple) and indice_expr[0] == 'literal':
            clave = indice_expr[1]
            if isinstance(clave, str) and clave.startswith('"') and clave.endswith('"'):
                clave = clave.strip('"')
                if clave not in tabla_tipos_arrays[variable_array]:
                    registrar_error_semantico(f"Error semántico: la clave '{clave}' no existe en el array {variable_array}.")
                    print("SEMANTIC ERROR:", f"la clave '{clave}' no existe en el array {variable_array}.")
                    return True

    # Validación especial para $pila (mantén si lo necesitas)
    if variable_array == '$pila':
        # ...tu código de validación para $pila aquí...
        return False

# === CREACIÓN DEL PARSER ===
def crear_parser():
    """Crea y retorna el objeto parser"""
    return yacc.yacc()

# Crear el parser global
parser = crear_parser()