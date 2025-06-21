from lexer import lexer
from reglas_sintacticas import analizar_sintactico, analizar_multiples_archivos

def analizar_archivo_completo(archivo_php, github_user):
    """
    Realiza análisis léxico y sintáctico completo de un archivo PHP
    """
    try:
        with open(archivo_php, 'r', encoding='utf-8') as file:
            codigo = file.read()
        
        print("="*70)
        print(f"ANÁLISIS COMPLETO DE: {archivo_php}")
        print(f"CONTRIBUIDOR: {github_user}")
        print("="*70)
        
        # === ANÁLISIS LÉXICO ===
        print("\n🔍 INICIANDO ANÁLISIS LÉXICO...")
        tokens = []
        lexer.input(codigo)
        
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
            print(f"Token: {tok.type:15} | Valor: '{tok.value}' | Línea: {tok.lineno}")
        
        print(f"\n✅ Análisis léxico completado: {len(tokens)} tokens encontrados")
        
        # === ANÁLISIS SINTÁCTICO ===
        print("\n🔍 INICIANDO ANÁLISIS SINTÁCTICO...")
        resultado_sintactico = analizar_sintactico(archivo_php, github_user)
        
        # === RESUMEN FINAL ===
        print("\n" + "="*70)
        print("📊 RESUMEN DEL ANÁLISIS")
        print("="*70)
        print(f"📄 Archivo: {archivo_php}")
        print(f"👤 Contribuidor: {github_user}")
        print(f"🔤 Tokens encontrados: {len(tokens)}")
        
        if resultado_sintactico['exito']:
            print("✅ Análisis sintáctico: EXITOSO")
        else:
            print(f"❌ Análisis sintáctico: FALLIDO ({len(resultado_sintactico['errores'])} errores)")
            
        print(f"📝 Log sintáctico: {resultado_sintactico.get('log_archivo', 'No generado')}")
        print("="*70)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Análisis individual
    analizar_archivo_completo('algoritmos/algoritmo_Nehemias.php', 'NLindao2004')
    
