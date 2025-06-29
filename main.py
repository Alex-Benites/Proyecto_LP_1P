from lexer import lexer
from reglas_sintacticas import analizar_sintactico, analizar_multiples_archivos
import os
from datetime import datetime
from parser import obtener_errores_semanticos, limpiar_errores_semanticos, limpiar_tabla_simbolos,limpiar_tabla_tipos_arrays

def generar_log_lexico(archivo_php, github_user, tokens):
    """
    Genera el log del análisis léxico
    """
    timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
    log_filename = f"logs/lexico-{github_user}-{timestamp}.txt"

    # Asegurar que la carpeta logs existe
    os.makedirs('logs', exist_ok=True)

    with open(log_filename, 'w', encoding='utf-8') as log_file:
        # Encabezado
        log_file.write(f"ANÁLISIS LÉXICO - {archivo_php}\n")
        log_file.write(f"Contribución de: {github_user}\n")
        log_file.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log_file.write("="*60 + "\n\n")

        # Estado del análisis
        log_file.write("ESTADO DEL ANÁLISIS:  ANÁLISIS EXITOSO\n\n")

        # Lista de tokens encontrados
        log_file.write("TOKENS ENCONTRADOS:\n")
        log_file.write("-" * 40 + "\n")
        for i, token in enumerate(tokens, 1):
            log_file.write(f"{i:3d}. Token: {token.type:15} | Valor: '{token.value}' | Línea: {token.lineno}\n")

        # Estadísticas
        log_file.write(f"\nESTADÍSTICAS LÉXICAS:\n")
        log_file.write("-" * 25 + "\n")
        log_file.write(f"Total de tokens: {len(tokens)}\n")

        # Contar tipos de tokens
        tipos_tokens = {}
        for token in tokens:
            tipos_tokens[token.type] = tipos_tokens.get(token.type, 0) + 1

        log_file.write(f"Tipos únicos de tokens: {len(tipos_tokens)}\n")
        log_file.write("\nFRECUENCIA DE TOKENS:\n")
        log_file.write("-" * 20 + "\n")
        for tipo, cantidad in sorted(tipos_tokens.items()):
            log_file.write(f"{tipo:15}: {cantidad}\n")

        # Información adicional
        log_file.write(f"\n" + "="*60 + "\n")
        log_file.write("INFORMACIÓN ADICIONAL:\n")
        log_file.write("-" * 25 + "\n")
        log_file.write(f"Archivo analizado: {archivo_php}\n")
        log_file.write("Análisis léxico completado sin errores\n")
        log_file.write("Todos los tokens fueron reconocidos correctamente\n")

    return log_filename

def realizar_analisis_lexico(codigo, archivo_php, github_user):
    """
    Realiza SOLO el análisis léxico y genera su log
    """
    print(" INICIANDO ANÁLISIS LÉXICO...")
    tokens = []

    # Crear una nueva instancia del lexer para evitar conflictos
    from lexer import lexer
    lexer.input(codigo)

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
        print(f"Token: {tok.type:15} | Valor: '{tok.value}' | Línea: {tok.lineno}")

    print(f" Análisis léxico completado: {len(tokens)} tokens encontrados")

    # Generar log léxico INMEDIATAMENTE
    log_lexico = generar_log_lexico(archivo_php, github_user, tokens)
    print(f" Log léxico generado: {log_lexico}")

    return tokens, log_lexico

def analizar_archivo_completo(archivo_php, github_user):
    """
    Realiza análisis léxico y sintáctico completo de un archivo PHP
    """
    try:
        # Limpiar errores y tabla de símbolos antes de cada análisis
        limpiar_errores_semanticos()
        limpiar_tabla_simbolos()
        limpiar_tabla_tipos_arrays()
        with open(archivo_php, 'r', encoding='utf-8') as file:
            codigo = file.read()

        print("="*70)
        print(f"ANÁLISIS COMPLETO DE: {archivo_php}")
        print(f"CONTRIBUIDOR: {github_user}")
        print("="*70)

        # === ANÁLISIS LÉXICO SEPARADO ===
        tokens, log_lexico = realizar_analisis_lexico(codigo, archivo_php, github_user)

        # === ANÁLISIS SINTÁCTICO SEPARADO ===
        print("\n INICIANDO ANÁLISIS SINTÁCTICO Y SEMÁNTICO...")
        resultado_sintactico_semantico = analizar_sintactico(archivo_php, github_user)

        # === ANÁLISIS SEMÁNTICO ===
        # === RESUMEN FINAL ===
        print("\n" + "="*70)
        print(" RESUMEN DEL ANÁLISIS")
        print("="*70)
        print(f" Archivo: {archivo_php}")
        print(f" Contribuidor: {github_user}")
        print(f" Tokens encontrados: {len(tokens)}")

        if resultado_sintactico_semantico['exito_sintactico']:
            print(" Análisis sintáctico: EXITOSO")
        else:
            print(f" Análisis sintáctico: FALLIDO ({len(resultado_sintactico_semantico['errores'])} errores)")

        if resultado_sintactico_semantico['exito_semantico']:
            print(" Análisis semántico: EXITOSO")
        else:
            print(" Análisis semántico: FALLIDO")
        

        print(f" Log léxico: {log_lexico}")
        print(f" Log sintáctico: {resultado_sintactico_semantico.get('log_archivo_sintactico', 'No generado')}")
        print(f" Log semántico: {resultado_sintactico_semantico.get('log_archivo_semantico', 'No generado')}")
        print("="*70)

        return {
            'lexico': {'exito': True, 'tokens': len(tokens), 'log': log_lexico},
            'sintactico': resultado_sintactico_semantico
        }

    except Exception as e:
        print(f" Error: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    print(" INICIANDO ANALIZADOR LÉXICO-SINTÁCTICO")
    print("="*70)

    # Análisis individual del algoritmo de Nehemias
    analizar_archivo_completo('algoritmos/algoritmo_Nehemias.php', 'NLindao2004')
    analizar_archivo_completo('algoritmos/algoritmo_Fernando.php', 'fzavala2003')
    analizar_archivo_completo('algoritmos/algoritmo_Alex.php', 'Alex-Benites')


    print("\n ANÁLISIS COMPLETADO")