with open('algoritmos/algoritmo_Alex.php', 'r', encoding='utf-8') as file:
    lineas = file.readlines()

print(f"Total de líneas: {len(lineas)}")
print("\n=== LÍNEAS ALREDEDOR DEL ERROR (línea 63) ===")

# Mostrar líneas 58-68 para ver el contexto del error en línea 63
for i in range(max(0, 58), min(len(lineas), 68)):
    linea_num = i + 1
    marcador = ">>> ERROR AQUÍ <<<" if linea_num == 63 else ""
    print(f"{linea_num:2d}: {lineas[i].rstrip()} {marcador}")

# Buscar todas las líneas que contienen paréntesis
print("\n=== TODAS LAS LÍNEAS CON PARÉNTESIS ===")
for i, linea in enumerate(lineas, 1):
    if '(' in linea or ')' in linea:
        print(f"Línea {i}: {linea.strip()}")

# Buscar líneas con echo o cadenas sin cerrar
print("\n=== LÍNEAS CON ECHO Y CADENAS ===")
for i, linea in enumerate(lineas, 1):
    if 'echo' in linea.lower() or '"' in linea:
        print(f"Línea {i}: {linea.strip()}")

print("\n=== CONTENIDO COMPLETO DEL ARCHIVO ===")
for i, linea in enumerate(lineas, 1):
    print(f"{i:2d}: {linea.rstrip()}")

