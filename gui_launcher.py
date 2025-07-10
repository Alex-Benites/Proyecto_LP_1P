#!/usr/bin/env python3
"""
Lanzador de la interfaz gráfica
Analizador Léxico-Sintáctico-Semántico - Alex Benites
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_gui import main

if __name__ == "__main__":
    main()