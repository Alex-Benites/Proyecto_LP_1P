# Analizador Léxico-Sintáctico-Semántico PHP - Proyecto LP 1P

## 📝 Descripción
Este proyecto implementa un *analizador completo* para el lenguaje *PHP* que incluye:
- *Análisis Léxico*: Reconocimiento de tokens
- *Análisis Sintáctico*: Verificación de estructura gramatical  
- *Análisis Semántico*: Validación de reglas semánticas
- *Interfaz Gráfica*: Editor de código con análisis en tiempo real

Utiliza *PLY (Python Lex-Yacc)* y *Tkinter* para crear una experiencia completa de desarrollo.

## 👥 Integrantes del Equipo
- *Alex* - Delimitadores, estructuras, reglas semánticas (división por cero, acceso a arrays)
- *Fernando* - Tokens básicos, variables, declaración de variables, verificación de tipos
- *Nehemias* - Operadores, expresiones, redefinición de funciones, parámetros, métodos de cola

## 📁 Estructura del Proyecto

Proyecto_LP_1P/
├── lexer.py                    # Analizador léxico principal
├── parser.py                   # Analizador sintáctico y semántico
├── main.py                     # Punto de entrada principal
├── reglas_sintacticas.py       # Reglas sintácticas
├── gui_launcher.py             # Lanzador de la interfaz gráfica
├── algoritmos/                 # Algoritmos de prueba en PHP
│   ├── algoritmo_Alex.php
│   ├── algoritmo_Fernando.php
│   └── algoritmo_Nehemias.php
├── gramaticas/                 # Gramática en formato BNF
│   └── expresiones.bnf
├── gui/                        # Interfaz gráfica
│   ├── __init__.py
│   └── main_gui.py
├── logs/                       # Logs generados por el analizador
│   └── [lexico|sintactico|semantico]-[usuario]-[fecha]-[hora].txt
└── README.md                   # Este archivo


## 🔧 Requisitos
- Python 3.8 o superior
- PLY (Python Lex-Yacc)
- Tkinter (incluido por defecto en Python)

### Instalación de dependencias
bash
pip install ply


## 🚀 Formas de Ejecutar el Proyecto

### 🖥️ Interfaz Gráfica (Recomendado)
bash
python gui_launcher.py

*Características de la interfaz:*
- *💾 Save*: Guardar cambios en el archivo actual
- *📁 Upload*: Subir archivo desde tu computadora o carpeta algoritmos/
- *▶️ Run*: Ejecutar análisis léxico, sintáctico y semántico
- *💾 Download*: Descargar el archivo actual
- *Editor de código*: Panel izquierdo con syntax highlighting
- *Consola de resultados*: Panel derecho mostrando análisis completo

### 📝 Línea de Comandos
bash
# Analizar un archivo específico
python main.py

# El programa te pedirá seleccionar:
# 1. Alex - analiza algoritmo_Alex.php
# 2. Fernando - analiza algoritmo_Fernando.php  
# 3. Nehemias - analiza algoritmo_Nehemias.php


## 📊 Análisis Implementados

### 🔤 Análisis Léxico
*Tokens Reconocidos:*
- VARIABLE - Variables PHP ($variable)
- NUMERO - Números enteros y decimales
- CADENA - Cadenas de texto entre comillas
- IDENTIFICADOR - Identificadores y nombres de funciones
- *Operadores*: +, -, *, /, =, ==, !=, >, <, >=, <=
- *Delimitadores*: (, ), {, }, [, ], ;, ,, ., ->, ::, =>
- *Palabras reservadas*: if, else, while, for, function, echo, etc.

### 📝 Análisis Sintáctico
*Reglas gramaticales implementadas:*
- Declaraciones de variables
- Expresiones aritméticas y lógicas
- Estructuras de control (if, while, for)
- Definición y llamada de funciones
- Acceso a arrays
- Operaciones con objetos

### 🧠 Análisis Semántico

#### Reglas de Alex:
1. *División por cero*: Detecta x / 0 en cualquier expresión
2. *Acceso seguro a arrays*: Valida índices negativos y tipos incorrectos

#### Reglas de Fernando:
1. *Declaración de variables*: Verifica que las variables estén declaradas antes de usarse
2. *Verificación de tipos*: Valida compatibilidad de tipos en asignaciones

#### Reglas de Nehemias:
1. *Redefinición de funciones*: Evita definir la misma función múltiples veces
2. *Validación de parámetros*: Verifica número correcto de argumentos en llamadas
3. *Operaciones de cola*: Detecta underflow/overflow en estructuras de datos

## 📋 Algoritmos de Prueba

### algoritmo_Alex.php
- *Tema*: Sistema de gestión de cola de clientes
- *Casos semánticos*:
  - División por cero intencional: $promedio = 100 / 0
  - Acceso con índices negativos: $error = $cola[-1]
  - Índices string en arrays: $error = $cola["texto"]

### algoritmo_Fernando.php
- *Tema*: Sistema de registro de personas
- *Casos semánticos*:
  - Variables no declaradas
  - Incompatibilidad de tipos en asignaciones

### algoritmo_Nehemias.php
- *Tema*: Implementación de cola con funciones
- *Casos semánticos*:
  - Redefinición de funciones
  - Parámetros incorrectos en llamadas
  - Operaciones inválidas en cola vacía

## 📄 Logs Generados
Cada análisis genera logs detallados:

### Formato de archivos:

logs/lexico-[usuario]-[ddmmyyyy]-[HHhMM].txt
logs/sintactico-[usuario]-[ddmmyyyy]-[HHhMM].txt  
logs/semantico-[usuario]-[ddmmyyyy]-[HHhMM].txt


### Contenido de logs:
- *Léxico*: Lista completa de tokens reconocidos
- *Sintáctico*: Estructura del árbol sintáctico y errores
- *Semántico*: Errores semánticos detectados por cada regla

## 💻 Ejemplo de Ejecución

### Interfaz Gráfica:
1. Ejecutar: python gui_launcher.py
2. Hacer clic en "📁 Upload"
3. Elegir "Sí" para cargar desde carpeta algoritmos/
4. Seleccionar algoritmo_Alex.php
5. Hacer clic en "▶️ Run"
6. Ver resultados en la consola

### Resultado esperado:

🔍 ANÁLISIS COMPLETADO
============================================================
📊 Análisis Léxico:
  - Tokens encontrados: 156
  - Estado: ✅ EXITOSO
📝 Análisis Sintáctico:
  - Estado: ✅ EXITOSO
🧠 Análisis Semántico:
  - Errores semánticos: 4
    1. Error semántico: División por cero detectada.
    2. Error semántico: Variable $indice_negativo contiene índice negativo (-1).
    3. Error semántico: Índice string 'texto' usado en array simple $cola.
============================================================


## 🎨 Interfaz Gráfica

### Características principales:
- *Editor de código*: Syntax highlighting básico, numeración de líneas
- *Consola en tiempo real*: Muestra resultados del análisis paso a paso
- *Gestión de archivos*: Carga, guarda y descarga archivos PHP
- *Análisis completo*: Ejecuta los tres niveles de análisis simultáneamente

### Controles disponibles:
- *💾 Save*: Guarda el archivo actual
- *📁 Upload*: Carga archivos (con opción de carpeta algoritmos/)
- *▶️ Run*: Ejecuta análisis completo
- *💾 Download*: Descarga el código actual

## 🤝 Contribuciones Específicas

### Alex - Delimitadores y Reglas Semánticas
- Delimitadores: (, ), {, }, [, ], ;, ,, .
- Operadores PHP: =>, ->
- *Regla semántica 1*: Detección de división por cero
- *Regla semántica 2*: Validación de acceso seguro a arrays
- *Interfaz gráfica*: Diseño y implementación completa

### Fernando - Tokens y Validación de Variables
- Variables PHP, números, cadenas, identificadores
- *Regla semántica 1*: Declaración obligatoria de variables
- *Regla semántica 2*: Verificación de compatibilidad de tipos

### Nehemias - Operadores y Funciones
- Operadores aritméticos, comparación, asignación
- *Regla semántica 1*: Prevención de redefinición de funciones
- *Regla semántica 2*: Validación de parámetros en funciones
- *Regla semántica 3*: Operaciones seguras en estructuras de datos

## 🔧 Desarrollo y Testing

### Para desarrolladores:
bash
# Ejecutar análisis individual
python lexer.py          # Solo análisis léxico
python parser.py         # Análisis sintáctico y semántico
python main.py           # Análisis completo via terminal

# Lanzar interfaz gráfica
python gui_launcher.py   # Interfaz completa


### Archivos temporales (ignorados por Git):
- __pycache__/ - Cache de Python
- logs/ - Logs generados
- parser.out - Archivo temporal de PLY
- parsetab.py - Tablas de análisis generadas

## 📧 Contacto
Para dudas o consultas sobre el proyecto, contactar a los integrantes del equipo:
- *Alex*: Interfaz gráfica y reglas semánticas
- *Fernando*: Análisis de variables y tipos  
- *Nehemias*: Análisis de funciones y operadores

---
*Curso*: Lenguajes de Programación  
*Profesor*: [Nombre del profesor]  
*Universidad*: ESPOL  
*Semestre*: Séptimo Semestre  
*Entrega*: [Fecha de entrega]

## 🏆 Características Destacadas
- ✅ Análisis léxico, sintáctico y semántico completo
- ✅ 6 reglas semánticas implementadas (2 por integrante)
- ✅ Interfaz gráfica funcional con editor de código
- ✅ Logs detallados para debugging
- ✅ Compatibilidad con sintaxis PHP moderna
- ✅ Gestión de errores robusta
- ✅ Documentación completa