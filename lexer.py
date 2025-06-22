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
    # Definicion de operadores básicos
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
    'TAG_FINAL',
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
    'FUNCION'
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
    'readline': 'READLINE',
}

tokens += list(reserved.values())

# === INICIO CONTRIBUCIÓN FERNANDO - Tokens básicos ===
# Implementacion de los tokens básicos
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
# Definicion de mis tokens para los operadores básicos
t_FUNCTION = r'function'
t_TAG_INICIO=r'<\?php'
t_TAG_FINAL=r'\?>'
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



# ====Inicio contribucion Daniel Zavala====

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_comment(t):
    r'//.*'
    pass

errores_lexicos=[]
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    errores_lexicos.append(f"{t.value[0]} en línea {t.lineno}")
    t.lexer.skip(1)

#===Fin contribucion Daniel Zavala====

# CREAR EL LEXER GLOBAL 
lexer = lex.lex(debug=True)

#Todos contribuimos
def analyze_file(filename, github_user):
    local_lexer = lex.lex()  # Usar lexer local para esta función
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()

        timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_filename = f"logs/lexico-{github_user}-{timestamp}.txt"

        os.makedirs('logs', exist_ok=True)
        local_lexer.input(data)  # Cambiar a local_lexer
        tokens_reconocidos = []

        print(f"Analizando archivo: {filename}")
        print(f"github_user: {github_user}")

        condicion=True
        while condicion:
            token = local_lexer.token()  # Cambiar a local_lexer
            if token is not None:
                tokens_reconocidos.append(f"Token: {token.type}, Valor: '{token.value}', Línea: {token.lineno}")
            else:
                condicion=False

        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write(f"ANÁLISIS LÉXICO - {filename}\n")
            log_file.write(f"Contribución de: {github_user}\n")
            log_file.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            log_file.write("="*50 + "\n\n")

            log_file.write("TOKENS RECONOCIDOS:\n")
            for token in tokens_reconocidos:
                log_file.write(token + "\n")
            log_file.write("\nERRORES LÉXICOS:\n")
            if errores_lexicos != []:
                for error in errores_lexicos:
                    log_file.write(f"{error}\n")
            
            log_file.write(f"\nTotal tokens reconocidos: {len(tokens_reconocidos)}\n")
            log_file.write(f"Total errores léxicos: {len(errores_lexicos)}\n")
            errores_lexicos.clear()  

        print(f"Log generado: {log_filename}")
        return log_filename

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    # Mapeo de archivos y contribuidores
    algoritmos = {
        "Alex": {
            "archivo": "algoritmos/algortimo_Alex.php",
            "github":"Alex-Benites"
        },
        "Fernando": {
            "archivo": "algoritmos/algoritmo_Fernando.php",
            "github":"fzavala2003" 

        },
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
