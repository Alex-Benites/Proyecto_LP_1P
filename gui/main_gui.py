import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
from datetime import datetime

# Importar tus módulos existentes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import analizar_archivo_completo
from lexer import lexer

class AnalizadorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analizador Léxico-Sintáctico-Semántico - Alex Benites")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')

        # Variables
        self.archivo_actual = None
        self.contenido_modificado = False
        self.historial_corridas = []  # Historial de corridas (código ejecutado)

        self.crear_interfaz()

    def crear_interfaz(self):
        # ✅ BARRA DE HERRAMIENTAS
        self.crear_toolbar()

        # ✅ ÁREA DE TRABAJO DIVIDIDA
        self.crear_area_trabajo()

    def crear_toolbar(self):
        """Crear barra de herramientas con botones Save, Upload, Clean Editor, Historial y Run (a la derecha)"""
        toolbar = tk.Frame(self.root, bg='#34495e', height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        # Botón Save (azul oscuro)
        btn_save = tk.Button(toolbar, text="💾 Save", command=self.guardar_archivo,
                            bg='#2980b9', fg='white', font=('Arial', 10, 'bold'),
                            padx=15, pady=5)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        # Botón Upload (verde)
        btn_upload = tk.Button(toolbar, text="📁 Upload", command=self.subir_archivo,
                              bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                              padx=15, pady=5)
        btn_upload.pack(side=tk.LEFT, padx=5, pady=5)

        # Botón Clean Editor (rojo)
        btn_clean_editor = tk.Button(toolbar, text="🧹 Clean Editor", command=self.limpiar_editor,
                                    bg='#c0392b', fg='white', font=('Arial', 10, 'bold'),
                                    padx=15, pady=5)
        btn_clean_editor.pack(side=tk.LEFT, padx=5, pady=5)

        # Botón Historial de Corridas (gris)
        btn_historial = tk.Menubutton(toolbar, text="🕑 Historial", bg='#7f8c8d', fg='white',
                                      font=('Arial', 10, 'bold'), padx=15, pady=5, relief=tk.RAISED)
        self.menu_historial = tk.Menu(btn_historial, tearoff=0)
        btn_historial.config(menu=self.menu_historial)
        btn_historial.pack(side=tk.LEFT, padx=5, pady=5)

        # Separador
        separator = tk.Frame(toolbar, width=2, bg='#7f8c8d')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Etiqueta de estado
        self.label_estado = tk.Label(toolbar, text="Listo", bg='#34495e', fg='white',
                                    font=('Arial', 10))
        self.label_estado.pack(side=tk.LEFT, padx=10)

        # Botón Run (naranja) - alineado a la derecha
        btn_run = tk.Button(toolbar, text="▶️ Run", command=self.ejecutar_analisis,
                           bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                           padx=15, pady=5)
        btn_run.pack(side=tk.RIGHT, padx=5, pady=5)

    def agregar_a_historial_corridas(self, codigo):
        """Agrega el código ejecutado al historial de corridas"""
        if codigo.strip():
            # Limitar a 10 corridas recientes
            self.historial_corridas.insert(0, codigo.strip())
            self.historial_corridas = self.historial_corridas[:10]
            self.actualizar_menu_historial()

    def actualizar_menu_historial(self):
        """Actualiza el menú de historial de corridas"""
        self.menu_historial.delete(0, tk.END)
        for idx, codigo in enumerate(self.historial_corridas, 1):
            resumen = codigo[:40].replace('\n', ' ') + ('...' if len(codigo) > 40 else '')
            self.menu_historial.add_command(
                label=f"{idx}: {resumen}",
                command=lambda c=codigo: self.cargar_codigo_historial(c)
            )
        if not self.historial_corridas:
            self.menu_historial.add_command(label="Sin historial", state=tk.DISABLED)

    def cargar_codigo_historial(self, codigo):
        """Carga código desde el historial al editor"""
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, codigo)
        self.actualizar_estado("Código cargado desde historial")

    def limpiar_editor(self):
        """Limpiar el área de edición de PHP"""
        self.text_editor.delete(1.0, tk.END)
        self.actualizar_estado("Editor limpio")

    def crear_area_trabajo(self):
        """Crear área dividida: Editor (izquierda) y Consola (derecha)"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ✅ EDITOR (Lado izquierdo)
        self.crear_editor(main_frame)

        # ✅ CONSOLA (Lado derecho)
        self.crear_consola(main_frame)

    def crear_editor(self, parent):
        """Crear área de edición de código"""
        # Frame del editor
        editor_frame = tk.Frame(parent, bg='#34495e')
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Título
        title_editor = tk.Label(editor_frame, text="📝 Editor de Código PHP",
                               bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        title_editor.pack(pady=5)

        # Área de texto con scroll
        text_frame = tk.Frame(editor_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar vertical
        scrollbar_v = tk.Scrollbar(text_frame)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal
        scrollbar_h = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        # Área de texto
        self.text_editor = tk.Text(text_frame, bg='#1e1e1e', fg='#ffffff',
                                  font=('Consolas', 11), insertbackground='white',
                                  yscrollcommand=scrollbar_v.set,
                                  xscrollcommand=scrollbar_h.set,
                                  wrap=tk.NONE)
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        # Configurar scrollbars
        scrollbar_v.config(command=self.text_editor.yview)
        scrollbar_h.config(command=self.text_editor.xview)

        # Ejemplo inicial
        codigo_ejemplo = """Ingrese su código PHP aquí... y presione '▶️ Run' para analizarlo."""

        self.text_editor.insert(tk.END, codigo_ejemplo)

        # Detectar cambios
        self.text_editor.bind('<KeyRelease>', self.on_text_changed)

    def crear_consola(self, parent):
        """Crear área de consola para mostrar resultados"""
        # Frame de la consola
        console_frame = tk.Frame(parent, bg='#34495e')
        console_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Título
        title_console = tk.Label(console_frame, text="🖥️ Consola de Resultados",
                                bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        title_console.pack(pady=5)

        # Área de texto con scroll
        console_text_frame = tk.Frame(console_frame)
        console_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar
        console_scrollbar = tk.Scrollbar(console_text_frame)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Área de texto de la consola
        self.text_console = tk.Text(console_text_frame, bg='#000000', fg='#00ff00',
                                   font=('Consolas', 10), state=tk.DISABLED,
                                   yscrollcommand=console_scrollbar.set)
        self.text_console.pack(fill=tk.BOTH, expand=True)

        console_scrollbar.config(command=self.text_console.yview)

        # Mensaje inicial
        self.escribir_consola("🚀 Analizador Léxico-Sintáctico-Semántico - Alex Benites")
        self.escribir_consola("="*60)
        self.escribir_consola("Presiona '▶️ Run' para ejecutar el análisis")

    def escribir_consola(self, mensaje):
        """Escribir mensaje en la consola"""
        self.text_console.config(state=tk.NORMAL)
        self.text_console.insert(tk.END, mensaje + "\n")
        self.text_console.config(state=tk.DISABLED)
        self.text_console.see(tk.END)

    def limpiar_consola(self):
        """Limpiar contenido de la consola"""
        self.text_console.config(state=tk.NORMAL)
        self.text_console.delete(1.0, tk.END)
        self.text_console.config(state=tk.DISABLED)

    def on_text_changed(self, event):
        """Detectar cambios en el editor"""
        self.contenido_modificado = True
        self.actualizar_estado("Modificado")

    def actualizar_estado(self, estado):
        """Actualizar etiqueta de estado"""
        self.label_estado.config(text=estado)

    def guardar_archivo(self):
        """Guardar archivo actual"""
        if not self.archivo_actual:
            self.guardar_como()
        else:
            try:
                with open(self.archivo_actual, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.get(1.0, tk.END))
                self.contenido_modificado = False
                self.actualizar_estado("Guardado")
                messagebox.showinfo("Éxito", "Archivo guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def guardar_como(self):
        """Guardar archivo con nuevo nombre"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".php",
            filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
        )
        if archivo:
            self.archivo_actual = archivo
            self.guardar_archivo()

    def subir_archivo(self):
        """Subir archivo desde el sistema o elegir desde la carpeta algoritmos"""
        # Mostrar opciones al usuario
        opcion = messagebox.askquestion(
            "Subir archivo",
            "¿Quieres cargar un archivo desde la carpeta 'algoritmos'?",
            icon="question"
        )

        if opcion == "yes":
            # ✅ Cargar desde la carpeta 'algoritmos'
            carpeta_algoritmos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../algoritmos")
            archivo = filedialog.askopenfilename(
                initialdir=carpeta_algoritmos,
                title="Selecciona un archivo PHP",
                filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
            )
        else:
            # ✅ Cargar desde cualquier ubicación
            archivo = filedialog.askopenfilename(
                title="Selecciona un archivo PHP",
                filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
            )

        # Si se seleccionó un archivo, cargarlo en el editor
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, contenido)
                self.archivo_actual = archivo
                self.contenido_modificado = False
                self.actualizar_estado(f"Cargado: {os.path.basename(archivo)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {str(e)}")

    def descargar_archivo(self):
        """Descargar archivo actual"""
        if not self.text_editor.get(1.0, tk.END).strip():
            messagebox.showwarning("Advertencia", "No hay contenido para descargar")
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".php",
            filetypes=[("PHP files", "*.php"), ("All files", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.get(1.0, tk.END))
                messagebox.showinfo("Éxito", f"Archivo descargado: {os.path.basename(archivo)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al descargar: {str(e)}")

    def ejecutar_analisis(self):
        """Ejecutar análisis del código"""
        self.limpiar_consola()
        self.actualizar_estado("Ejecutando...")

        # Crear archivo temporal
        codigo = self.text_editor.get(1.0, tk.END)
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        # Guardar en historial de corridas
        self.agregar_a_historial_corridas(codigo)

        # Ejecutar en hilo separado para no bloquear la interfaz
        threading.Thread(target=self._ejecutar_analisis_thread, args=(codigo,), daemon=True).start()

    def _ejecutar_analisis_thread(self, codigo):
        """Ejecutar análisis en hilo separado"""
        try:
            # ✅ DETECTAR AUTOMÁTICAMENTE EL AUTOR DEL CÓDIGO
            github_user = self.detectar_autor_codigo(codigo)

            # Guardar archivo temporal
            archivo_temp = f"temp_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.php"
            with open(archivo_temp, 'w', encoding='utf-8') as file:
                file.write(codigo)

            # Ejecutar análisis con el autor correcto
            resultado = analizar_archivo_completo(archivo_temp, github_user)

            # Mostrar resultados en la consola
            self.root.after(0, self.mostrar_resultados, resultado)

            # Limpiar archivo temporal
            if os.path.exists(archivo_temp):
                os.remove(archivo_temp)

        except Exception as e:
            self.root.after(0, self.mostrar_error, str(e))

    def detectar_autor_codigo(self, codigo):
        """
        Detecta automáticamente el autor del código basándose en patrones característicos
        """
        codigo_lower = codigo.lower()

        # ✅ DETECTAR POR COMENTARIOS ESPECÍFICOS (más preciso)
        if any(nombre in codigo_lower for nombre in ['nehemias', 'lindao', 'nlindao']):
            return 'NLindao2004'
        elif any(nombre in codigo_lower for nombre in ['fernando', 'zavala', 'fzavala']):
            return 'fzavala2003'
        elif any(nombre in codigo_lower for nombre in ['alex', 'benites']):
            return 'Alex-Benites-GUI'

        # ✅ DETECTAR CÓDIGO DE NEHEMIAS (COLA) - Muy específico
        elif ('cola' in codigo_lower and 'encolar' in codigo_lower and 'desencolar' in codigo_lower):
            return 'NLindao2004'

        # ✅ DETECTAR CÓDIGO DE FERNANDO (ARRAY ASOCIATIVO) - Muy específico
        elif ('$persona' in codigo and '"nombre"' in codigo and '"edad"' in codigo):
            return 'fzavala2003'

        # ✅ DETECTAR CÓDIGO DE ALEX (PILA) - Muy específico
        elif ('$pila' in codigo and 'array_push' in codigo and 'array_pop' in codigo):
            return 'Alex-Benites-GUI'

        # ✅ DETECTAR POR ESTRUCTURAS MUY ESPECÍFICAS
        elif ('function encolar' in codigo_lower and 'function desencolar' in codigo_lower):
            return 'NLindao2004'
        elif ('simulación de pila' in codigo_lower and 'stack' in codigo_lower):
            return 'Alex-Benites-GUI'

        # ✅ PARA CÓDIGOS GENÉRICOS O DE PRUEBA
        else:
            return 'Usuario-Prueba'

    def mostrar_resultados(self, resultado):
        """Mostrar resultados del análisis"""
        self.escribir_consola("🔍 ANÁLISIS COMPLETADO")
        self.escribir_consola("="*60)

        if isinstance(resultado, dict):
            # Mostrar información del análisis léxico
            if 'lexico' in resultado:
                lexico = resultado['lexico']
                self.escribir_consola(f"📊 Análisis Léxico:")
                self.escribir_consola(f"  - Tokens encontrados: {lexico.get('tokens', 'N/A')}")
                self.escribir_consola(f"  - Estado: {'✅ EXITOSO' if lexico.get('exito', False) else '❌ FALLIDO'}")

            # Mostrar información del análisis sintáctico
            if 'sintactico' in resultado:
                sintactico = resultado['sintactico']
                self.escribir_consola(f"📝 Análisis Sintáctico:")
                self.escribir_consola(f"  - Estado: {'✅ EXITOSO' if sintactico.get('exito', False) else '❌ FALLIDO'}")

                if sintactico.get('errores'):
                    self.escribir_consola(f"  - Errores encontrados: {len(sintactico['errores'])}")
                    # ✅ MOSTRAR TODOS LOS ERRORES SINTÁCTICOS (sin límite)
                    for i, error in enumerate(sintactico['errores'], 1):
                        self.escribir_consola(f"    {i}. {error}")

            # Mostrar análisis semántico
            if sintactico.get('errores_semanticos'):
                self.escribir_consola(f"🧠 Análisis Semántico:")
                self.escribir_consola(f"  - Errores semánticos: {len(sintactico['errores_semanticos'])}")
                # ✅ MOSTRAR TODOS LOS ERRORES SEMÁNTICOS (sin límite)
                for i, error in enumerate(sintactico['errores_semanticos'], 1):
                    self.escribir_consola(f"    {i}. {error}")
            else:
                self.escribir_consola(f"🧠 Análisis Semántico: ✅ SIN ERRORES")

        self.escribir_consola("="*60)
        self.actualizar_estado("Análisis completado")

    def mostrar_error(self, error):
        """Mostrar error en la consola"""
        self.escribir_consola(f"❌ ERROR: {error}")
        self.actualizar_estado("Error en análisis")

    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = AnalizadorGUI()
    app.ejecutar()

if __name__ == "__main__":
    main()