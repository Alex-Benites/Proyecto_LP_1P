with open('algoritmos/algoritmo_Fernando.php', 'r', encoding='utf-8') as file:
    lineas = file.readlines()

print(f"Total de líneas: {len(lineas)}")
print("\n=== LÍNEAS ALREDEDOR DEL ERROR ===")

# Cambia aquí el rango para ver las líneas cercanas al error,
# si te dice que es la línea 62, puedes poner 55 a 65, por ejemplo
for i in range(max(0, 55), min(len(lineas), 65)):
    linea_num = i + 1
    marcador = ">>> ERROR AQUÍ <<<" if linea_num == 62 else ""
    print(f"{linea_num:2d}: {lineas[i].rstrip()} {marcador}")

# Buscar todas las líneas que contienen corchetes
print("\n=== TODAS LAS LÍNEAS CON CORCHETES ===")
for i, linea in enumerate(lineas, 1):
    if '[' in linea or ']' in linea:
        print(f"Línea {i}: {linea.strip()}")

print("\n=== CONTENIDO COMPLETO DEL ARCHIVO ===")
for i, linea in enumerate(lineas, 1):
    print(f"{i:2d}: {linea.rstrip()}")