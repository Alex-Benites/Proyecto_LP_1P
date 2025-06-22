with open('algoritmos/algoritmo_Nehemias.php', 'r', encoding='utf-8') as file:
    lineas = file.readlines()

print(f"Total de líneas: {len(lineas)}")
print("\n=== LÍNEAS ALREDEDOR DEL ERROR ===")

# Mostrar líneas 75-85 para ver el contexto
for i in range(max(0, 75), min(len(lineas), 85)):
    linea_num = i + 1
    marcador = ">>> ERROR AQUÍ <<<" if linea_num == 81 else ""
    print(f"{linea_num:2d}: {lineas[i].rstrip()} {marcador}")

# Buscar todas las líneas que contienen corchetes
print("\n=== TODAS LAS LÍNEAS CON CORCHETES ===")
for i, linea in enumerate(lineas, 1):
    if '[' in linea or ']' in linea:
        print(f"Línea {i}: {linea.strip()}")

print("\n=== CONTENIDO COMPLETO DEL ARCHIVO ===")
for i, linea in enumerate(lineas, 1):
    print(f"{i:2d}: {linea.rstrip()}")