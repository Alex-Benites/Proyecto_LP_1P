import ply.lex as lex
import os
from datetime import datetime

# Definir tokens para PHP
tokens = [
    # === INICIO CONTRIBUCIÓN FERNANDO - Tokens básicos ===
    'VARIABLE',
    'NUMERO',
    'CADENA',
    'IDENTIFICADOR',
    # === FIN CONTRIBUCIÓN FERNANDO ===

    # === INICIO CONTRIBUCIÓN NEHEMIAS - Operadores ===
    'MAS',
    'MENOS',
    'MULTIPLICAR',
    'DIVIDIR',
    'ASIGNAR',
    'IGUAL',
    'NO_IGUAL',
    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'TAG_INICIO',
    'TAG_FIN',      # ← CORREGIDO: TAG_FIN en lugar de TAG_FINAL
    # === FIN CONTRIBUCIÓN NEHEMIAS ===

    # === INICIO CONTRIBUCIÓN ALEX - Delimitadores y estructura ===
    'PAREN_IZQ',
    'PAREN_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'PUNTO_COMA',
    'COMA',
    'PUNTO',
    'FLECHA',
    'DOBLE_DOS_PUNTOS',
    'ARRAY_ASOCIATIVO',
    # === FIN CONTRIBUCIÓN ALEX ===
]

# Definicion de palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'while': 'WHILE',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'as': 'AS',
    'function': 'FUNCTION',
    'class': 'CLASS',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'return': 'RETURN',
    'new': 'NEW',
    'echo': 'ECHO',
    'print': 'PRINT',
    'readline': 'READLINE',  # Agregar esta línea
    'define': 'DEFINE'
}

tokens += list(reserved.values())

# === INICIO CONTRIBUCIÓN FERNANDO - Tokens básicos ===
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value) if '.' in t.value else int(t.value)
    except ValueError:
        t.value = 0
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t
# === FIN CONTRIBUCIÓN FERNANDO ===

# === INICIO CONTRIBUCIÓN NEHEMIAS - Operadores ===
t_TAG_INICIO = r'<\?php'

def t_TAG_FIN(t):  # ← CORREGIDO: Mantener solo esta regla
    r'\?>'
    return t

t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICAR = r'\*'
t_DIVIDIR = r'/'
t_ASIGNAR = r'='
t_IGUAL = r'=='
t_NO_IGUAL = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
# === FIN CONTRIBUCIÓN NEHEMIAS ===

# === INICIO CONTRIBUCIÓN ALEX - Delimitadores y estructura ===
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_PUNTO_COMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_FLECHA = r'->'
t_DOBLE_DOS_PUNTOS = r'::'
t_ARRAY_ASOCIATIVO = r'=>'
# === FIN CONTRIBUCIÓN ALEX ===

# === INICIO CONTRIBUCIÓN DANIEL ZAVALA ===
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'//.*'
    pass

errores_lexicos = []

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    errores_lexicos.append(f"{t.value[0]} en línea {t.lineno}")
    t.lexer.skip(1)
# === FIN CONTRIBUCIÓN DANIEL ZAVALA ===

# CREAR EL LEXER GLOBAL
lexer = lex.lex(debug=True)

# Función de análisis
def analyze_file(filename, github_user):
    local_lexer = lex.lex()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()

        timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_filename = f"logs/lexico-{github_user}-{timestamp}.txt"

        os.makedirs('logs', exist_ok=True)
        local_lexer.input(data)
        tokens_reconocidos = []

        print(f"Analizando archivo: {filename}")
        print(f"github_user: {github_user}")

        while True:
            token = local_lexer.token()
            if token is None:
                break
            tokens_reconocidos.append(f"Token: {token.type}, Valor: '{token.value}', Línea: {token.lineno}")

        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write(f"ANÁLISIS LÉXICO - {filename}\n")
            log_file.write(f"Contribución de: {github_user}\n")
            log_file.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            log_file.write("="*50 + "\n\n")

            log_file.write("TOKENS RECONOCIDOS:\n")
            for token in tokens_reconocidos:
                log_file.write(token + "\n")

            log_file.write("\nERRORES LÉXICOS:\n")
            if errores_lexicos:
                for error in errores_lexicos:
                    log_file.write(f"{error}\n")
            else:
                log_file.write("No se encontraron errores léxicos.\n")

            log_file.write(f"\nTotal tokens reconocidos: {len(tokens_reconocidos)}\n")
            log_file.write(f"Total errores léxicos: {len(errores_lexicos)}\n")
            errores_lexicos.clear()

        print(f"Log generado: {log_filename}")
        return log_filename

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# COMENTAR O ELIMINAR ESTA SECCIÓN:
"""
if __name__ == "__main__":
    algoritmos = {
        "Nehemias": {
            "archivo": "algoritmos/algoritmo_Nehemias.php",
            "github":"NLindao2004"
        }
    }

    for nombre, config in algoritmos.items():
        if os.path.exists(config["archivo"]):
            print(f"\n--- ANALIZANDO {nombre.upper()} ---")
            analyze_file(config["archivo"], config["github"])
        else:
            print(f"Archivo no encontrado: {config['archivo']}")
"""