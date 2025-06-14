# Analizador Léxico PHP - Proyecto LP 1P

## 📝 Descripción
Este proyecto implementa un **analizador léxico** para el lenguaje **PHP** utilizando **PLY (Python Lex-Yacc)**. El analizador reconoce tokens básicos, operadores, delimitadores y palabras reservadas del lenguaje PHP.

## 👥 Integrantes del Equipo
- **Alex** - Delimitadores y estructuras
- **Fernando** - Tokens básicos y variables
- **Nehemias** - Operadores y expresiones

## 📁 Estructura del Proyecto
```
Proyecto_LP_1P/
├── lexer.py              # Analizador léxico principal
├── algoritmos/           # Algoritmos de prueba en PHP
│   ├── algortimo_Alex.php
│   ├── algoritmo_Fernando.php
│   └── algoritmo_Nehemias.php
├── logs/                 # Logs generados por el analizador
│   └── lexico-[usuario]-[fecha]-[hora].txt
└── README.md             # Este archivo
```

## 🔧 Requisitos
- Python 3.x
- PLY (Python Lex-Yacc)

### Instalación de dependencias
```bash
pip install ply
```

## 🚀 Uso del Analizador

### Analizar un algoritmo específico
```bash
# Analizar algoritmo de Alex
python lexer.py alex

# Analizar algoritmo de Fernando
python lexer.py fernando

# Analizar algoritmo de Nehemias
python lexer.py nehemias
```

### Analizar todos los algoritmos
```bash
python lexer.py
```

## 📊 Tokens Reconocidos

### Tokens Básicos
- `VARIABLE` - Variables PHP ($variable)
- `NUMERO` - Números enteros y decimales
- `CADENA` - Cadenas de texto entre comillas
- `IDENTIFICADOR` - Identificadores y nombres de funciones

### Operadores
- `MAS` (+), `MENOS` (-), `MULTIPLICAR` (*), `DIVIDIR` (/)
- `ASIGNAR` (=), `IGUAL` (==), `NO_IGUAL` (!=)
- `MAYOR` (>), `MENOR` (<), `MAYOR_IGUAL` (>=), `MENOR_IGUAL` (<=)

### Delimitadores (Contribución de Alex)
- `PAREN_IZQ` ((), `PAREN_DER` ())
- `LLAVE_IZQ` ({), `LLAVE_DER` (})
- `CORCHETE_IZQ` ([), `CORCHETE_DER` (])
- `PUNTO_COMA` (;), `COMA` (,), `PUNTO` (.)
- `FLECHA` (->), `DOBLE_DOS_PUNTOS` (::)
- `ARRAY_ASOCIATIVO` (=>), `CONCATENAR` (.)

### Palabras Reservadas
`if`, `else`, `elseif`, `while`, `for`, `foreach`, `as`, `function`, `class`, `public`, `private`, `protected`, `return`, `new`, `echo`, `print`, `array`, `define`, `count`

## 📋 Algoritmos de Prueba

### algoritmo_Alex.php
- **Tema**: Arrays asociativos y análisis de datos
- **Características**:
  - Uso de arrays asociativos (`=>`)
  - Constantes con `define()`
  - Estructuras de control (`if`, `foreach`)
  - Funciones integradas (`count()`)

### algoritmo_Fernando.php
- **Tema**: [Pendiente - será completado por Fernando]

### algoritmo_Nehemias.php
- **Tema**: [Pendiente - será completado por Nehemias]

## 📄 Logs Generados
Cada ejecución genera un archivo log en la carpeta `logs/` con el formato:
```
lexico-[usuario]-[dd-mm-yyyy]-[HHhMM].txt
```

El log contiene:
- Información del archivo analizado
- Fecha y hora del análisis
- Lista completa de tokens reconocidos
- Estadísticas de tokens por contribuidor

## 💻 Ejemplo de Ejecución
```bash
$ python lexer.py alex
Analizando archivo: algoritmos/algortimo_Alex.php
Contribuidor: Alex
Token: MENOR, Valor: '<', Línea: 1
Token: IDENTIFICADOR, Valor: 'php', Línea: 1
Token: MAYOR, Valor: '>', Línea: 1
...
Log generado: logs/lexico-Alex-13-06-2025-16h45.txt
```

## 🤝 Contribuciones
Cada integrante contribuyó con componentes específicos del analizador:

### Alex - Delimitadores y Estructuras
- Paréntesis, llaves y corchetes
- Signos de puntuación
- Operadores especiales de PHP (=>, ->)

### Fernando - Tokens Básicos
- Variables PHP
- Números y cadenas
- Identificadores básicos

### Nehemias - Operadores
- Operadores aritméticos
- Operadores de comparación
- Operadores de asignación

## 📝 Notas Técnicas
- El analizador ignora comentarios de línea (`//`)
- Maneja errores léxicos mostrando caracteres ilegales
- Soporta tanto comentarios como código PHP estándar
- Compatible con sintaxis PHP moderna

## 📧 Contacto
Para dudas o consultas sobre el proyecto, contactar a los integrantes del equipo.

---
**Curso**: Lenguajes de Programación
**Entrega**: 14/06/2025 23:55 PM