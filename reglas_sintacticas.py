from parser import parser, limpiar_errores, obtener_errores
import os
from datetime import datetime

def analizar_sintactico(archivo_php, github_user):
    """
    Analiza sintácticamente un archivo PHP y genera un log

    Args:
        archivo_php (str): Ruta del archivo PHP a analizar
        github_user (str): Nombre de usuario de GitHub del contribuidor

    Returns:
        dict: Resultado del análisis con información de éxito/errores
    """
    # Limpiar errores de análisis previos
    limpiar_errores()

    try:
        # Leer el archivo PHP
        with open(archivo_php, 'r', encoding='utf-8') as file:
            codigo = file.read()

        print(f"\n=== ANÁLISIS SINTÁCTICO DE {archivo_php} ===")

        # Crear timestamp para el archivo log
        timestamp = datetime.now().strftime("%d%m%Y-%Hh%M")
        log_filename = f"logs/sintactico-{github_user}-{timestamp}.txt"

        # Asegurar que la carpeta logs existe
        os.makedirs('logs', exist_ok=True)

        # ✅ CREAR LEXER NUEVO PARA CADA ARCHIVO (SOLUCIÓN)
        import ply.lex as lex
        from lexer import tokens, reserved, t_VARIABLE, t_NUMERO, t_CADENA, t_IDENTIFICADOR
        from lexer import t_TAG_INICIO, t_TAG_FIN, t_MAS, t_MENOS, t_MULTIPLICAR, t_DIVIDIR
        from lexer import t_ASIGNAR, t_IGUAL, t_NO_IGUAL, t_MAYOR, t_MENOR, t_MAYOR_IGUAL, t_MENOR_IGUAL
        from lexer import t_PAREN_IZQ, t_PAREN_DER, t_LLAVE_IZQ, t_LLAVE_DER, t_CORCHETE_IZQ, t_CORCHETE_DER
        from lexer import t_PUNTO_COMA, t_COMA, t_PUNTO, t_FLECHA, t_DOBLE_DOS_PUNTOS, t_ARRAY_ASOCIATIVO
        from lexer import t_ignore, t_newline, t_comment, t_error

        # Crear nuevo lexer independiente
        lexer_local = lex.lex()
        lexer_local.input(codigo)

        # Realizar análisis sintáctico con lexer local
        resultado = parser.parse(codigo, lexer=lexer_local)

        # Obtener errores encontrados
        errores_sintacticos = obtener_errores()

        # Determinar estado del análisis
        if errores_sintacticos:
            estado_analisis = "❌ ANÁLISIS FALLIDO"
            print(f" Se encontraron {len(errores_sintacticos)} errores sintácticos")
            for error in errores_sintacticos:
                print(f"  - {error}")
        else:
            estado_analisis = "✅ ANÁLISIS EXITOSO"
            print("✅ Análisis sintáctico completado sin errores")

        # Generar log del análisis sintáctico
        _generar_log_sintactico(
            log_filename,
            archivo_php,
            github_user,
            estado_analisis,
            errores_sintacticos,
            codigo,
            resultado
        )

        print(f"📁 Log sintáctico generado: {log_filename}")

        return {
            'exito': len(errores_sintacticos) == 0,
            'errores': errores_sintacticos,
            'log_archivo': log_filename,
            'ast': resultado,
            'total_errores': len(errores_sintacticos)
        }

    except FileNotFoundError:
        error_msg = f"❌ Error: No se encontró el archivo '{archivo_php}'"
        print(error_msg)
        return {'exito': False, 'errores': [error_msg], 'total_errores': 1}
    except Exception as e:
        error_msg = f"❌ Error durante el análisis: {e}"
        print(error_msg)
        return {'exito': False, 'errores': [error_msg], 'total_errores': 1}

def _generar_log_sintactico(log_filename, archivo_php, github_user, estado_analisis, errores_sintacticos, codigo, resultado):
    """
    Genera el archivo de log del análisis sintáctico

    Args:
        log_filename (str): Nombre del archivo de log
        archivo_php (str): Archivo PHP analizado
        github_user (str): Usuario de GitHub
        estado_analisis (str): Estado del análisis
        errores_sintacticos (list): Lista de errores encontrados
        codigo (str): Código fuente analizado
        resultado: AST generado
    """
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        # Encabezado
        log_file.write(f"ANÁLISIS SINTÁCTICO - {archivo_php}\n")
        log_file.write(f"Contribución de: {github_user}\n")
        log_file.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log_file.write("="*60 + "\n\n")

        # Estado del análisis
        log_file.write(f"ESTADO DEL ANÁLISIS: {estado_analisis}\n\n")

        # Errores o éxito
        if errores_sintacticos:
            log_file.write("ERRORES SINTÁCTICOS ENCONTRADOS:\n")
            log_file.write("-" * 40 + "\n")
            for i, error in enumerate(errores_sintacticos, 1):
                log_file.write(f"{i}. {error}\n")
            log_file.write(f"\nTotal de errores sintácticos: {len(errores_sintacticos)}\n\n")

            # Sugerencias para corregir errores
            log_file.write("SUGERENCIAS PARA CORREGIR:\n")
            log_file.write("-" * 30 + "\n")
            log_file.write("1. Verificar que todas las sentencias terminen con ';'\n")
            log_file.write("2. Revisar que los paréntesis y llaves estén balanceados\n")
            log_file.write("3. Asegurar que las variables empiecen con '$'\n")
            log_file.write("4. Verificar la sintaxis de arrays y asignaciones\n")
        else:
            log_file.write(" NO SE ENCONTRARON ERRORES SINTÁCTICOS\n")
            log_file.write("El código cumple con las reglas gramaticales definidas.\n")
            log_file.write("Todas las construcciones sintácticas son válidas.\n")

        # Información adicional
        log_file.write("\n" + "="*60 + "\n")
        log_file.write("INFORMACIÓN ADICIONAL:\n")
        log_file.write("-" * 25 + "\n")
        log_file.write(f"Archivo analizado: {archivo_php}\n")
        log_file.write(f"Tamaño del código: {len(codigo)} caracteres\n")
        log_file.write(f"Líneas de código: {codigo.count(chr(10)) + 1}\n")

        if resultado:
            log_file.write("AST generado exitosamente\n")
            log_file.write("Estructura sintáctica válida\n")
        else:
            log_file.write("No se pudo generar AST completo\n")
            log_file.write("Revisar errores sintácticos arriba\n")

        # Estadísticas
        log_file.write(f"\nESTADÍSTICAS:\n")
        log_file.write("-" * 15 + "\n")
        log_file.write(f"Errores encontrados: {len(errores_sintacticos)}\n")
        log_file.write(f"Tasa de éxito: {0 if errores_sintacticos else 100}%\n")

def analizar_multiples_archivos(archivos_y_usuarios):
    """
    Analiza múltiples archivos PHP

    Args:
        archivos_y_usuarios (list): Lista de tuplas (archivo, usuario)

    Returns:
        dict: Resumen del análisis de todos los archivos
    """
    resultados = {}
    total_errores = 0
    archivos_exitosos = 0

    print("\n" + "="*70)
    print(" ANÁLISIS SINTÁCTICO MÚLTIPLE")
    print("="*70)

    for archivo, usuario in archivos_y_usuarios:
        print(f"\n Analizando: {archivo} (por {usuario})")
        resultado = analizar_sintactico(archivo, usuario)
        resultados[archivo] = resultado

        if resultado['exito']:
            archivos_exitosos += 1
        else:
            total_errores += resultado.get('total_errores', 0)

    # Resumen final
    print("\n" + "="*70)
    print(" RESUMEN FINAL")
    print("="*70)
    print(f" Archivos analizados: {len(archivos_y_usuarios)}")
    print(f" Archivos exitosos: {archivos_exitosos}")
    print(f" Archivos con errores: {len(archivos_y_usuarios) - archivos_exitosos}")
    print(f" Total errores: {total_errores}")
    print("="*70)

    return resultados