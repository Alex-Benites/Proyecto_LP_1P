from lexer import lexer

def analizar_archivo(archivo_php):
    try:
        with open(archivo_php, 'r', encoding='utf-8') as file:
            codigo = file.read()
        
        print("=== ANÁLISIS LÉXICO ===")
        tokens = []
        lexer.input(codigo)
        
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
            print(f"Token: {tok.type}, Valor: '{tok.value}', Línea: {tok.lineno}")
        
        print(f"\n✅ Análisis léxico completado: {len(tokens)} tokens encontrados")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analizar_archivo('algoritmos/algoritmo_Nehemias.php')