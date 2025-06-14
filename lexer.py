import ply.lex as lex
import os
import sys
from datetime import datetime

# Definir tokens para PHP
tokens = [
    # Definicion de Tokens básicos para mi analizador lexico
    'VARIABLE',
    'NUMERO',
    'CADENA',
    'IDENTIFICADOR',

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
    'CONCATENAR',
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
    'array': 'ARRAY',
    'define': 'DEFINE',
    'count': 'COUNT',
}

tokens += list(reserved.values())

# Implementacion de mis Tokens básicos
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

# Definicion de mis tokens para los operadores básicos
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
t_CONCATENAR = r'\.'
# === FIN CONTRIBUCIÓN ALEX ===

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

# Este es un token para ignorar espacios, tabs y saltos de línea y su implementación
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Este es un token para ignorar comentarios de una línea y su implementacion
def t_comment(t):
    r'//.*'
    pass

# implementacion de mi token para el manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

def analyze_file(filename, contributor_name="Alex"):
    """Analiza un archivo PHP y genera log de tokens"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()

        # Generar nombre del log con el nombre del contribuidor

        timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_filename = f"logs/lexico-{contributor_name}-{timestamp}.txt"

        os.makedirs('logs', exist_ok=True)

        lexer.input(data)

        tokens_found = []

        print(f"Analizando archivo: {filename}")
        print(f"Contribuidor: {contributor_name}")

        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens_found.append(f"Token: {tok.type}, Valor: '{tok.value}', Línea: {tok.lineno}")
            print(f"Token: {tok.type}, Valor: '{tok.value}', Línea: {tok.lineno}")

        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write(f"ANÁLISIS LÉXICO - {filename}\n")
            log_file.write(f"Contribución de: {contributor_name}\n")
            log_file.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            log_file.write("="*50 + "\n\n")

            log_file.write("TOKENS RECONOCIDOS:\n")
            for token in tokens_found:
                log_file.write(token + "\n")

            log_file.write(f"\nTotal tokens: {len(tokens_found)}\n")

            alex_tokens = [t for t in tokens_found if any(delim in t for delim in ['PAREN_IZQ', 'PAREN_DER', 'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'PUNTO_COMA', 'COMA', 'PUNTO', 'FLECHA', 'DOBLE_DOS_PUNTOS', 'CONCATENAR', 'ARRAY_ASOCIATIVO'])]
            log_file.write(f"Tokens de delimitadores (contribución Alex): {len(alex_tokens)}\n")

        print(f"Log generado: {log_filename}")
        return log_filename

    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    # Mapeo de archivos y contribuidores
    algoritmos = {
        "alex": {
            "archivo": "algoritmos/algortimo_Alex.php",
            "contribuidor": "Alex"
        },
        "fernando": {
            "archivo": "algoritmos/algoritmo_Fernando.php",
            "contribuidor": "Fernando"
        },
        "nehemias": {
            "archivo": "algoritmos/algoritmo_Nehemias.php",
            "contribuidor": "Nehemias"
        }
    }

    if len(sys.argv) > 1:
        nombre = sys.argv[1].lower()
        if nombre in algoritmos:
            config = algoritmos[nombre]
            if os.path.exists(config["archivo"]):
                analyze_file(config["archivo"], config["contribuidor"])
            else:
                print(f"Archivo no encontrado: {config['archivo']}")
        else:
            print(f"Nombre no válido. Usa: {', '.join(algoritmos.keys())}")
    else:
        print("Uso:")
        print("python lexer.py alex      # Para probar algoritmo de Alex")
        print("python lexer.py fernando  # Para probar algoritmo de Fernando")
        print("python lexer.py nehemias  # Para probar algoritmo de Nehemias")
        print("\nO ejecuta todos:")

        for nombre, config in algoritmos.items():
            if os.path.exists(config["archivo"]):
                print(f"\n--- Analizando {nombre.upper()} ---")
                analyze_file(config["archivo"], config["contribuidor"])
            else:
                print(f"Archivo no encontrado: {config['archivo']}")