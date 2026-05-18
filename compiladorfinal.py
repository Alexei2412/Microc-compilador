import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

class UnidadesLexicas:
    """Tabla de símbolos: mapea lexemas a sus tokens numéricos."""

    def __init__(self):
        # Diccionario de Palabras Reservadas y Librerías 
        self.Palabra = {
            "auto": 1, "break": 2, "case": 3, "char": 4, "const": 5,
            "continue": 6, "default": 7, "do": 8, "double": 9, "else": 10,
            "enum": 11, "extern": 12, "float": 13, "for": 14, "goto": 15,
            "if": 16, "int": 17, "long": 18, "register": 19, "return": 20,
            "short": 21, "signed": 22, "sizeof": 23, "static": 24, "struct": 25,
            "switch": 26, "typedef": 27, "union": 28, "unsigned": 29, "void": 30,
            "volatile": 31, "while": 32, "main": 33,
            "include": 40, "define": 41, "stdio.h": 42, "stdlib.h": 43,
            "string.h": 44, "conio.h": 45, "math.h": 46,
            "printf": 50, "scanf": 51
        }

        # Diccionario de Símbolos
        self._simbolos = {
            "+": 60, "-": 61, "*": 62, "/": 63, "%": 64,
            "=": 65, "==": 66, "<": 67, ">": 68, "<=": 69, ">=": 70, "!=": 71,
            "&&": 72, "||": 73, "!": 74,
            "(": 75, ")": 76, "{": 77, "}": 78, "[": 79, "]": 80,
            ";": 92, ",": 93, ".": 94, ":": 95, "#": 96, "'": 97
        }

    def GetTokenPalabra(self, lexema: str) -> int:
        """Retorna token de la palabra; 98 si es identificador."""
        return self.Palabra.get(lexema, 98)

    def GetTokenSimbolo(self, lexema: str) -> int:
        """Retorna token del símbolo; -1 si no fue encontrado."""
        return self._simbolos.get(lexema, -1)

    def GetDescripcionToken(self, token: int) -> str:
        """Retorna descripción legible del rango de token respetando límite 100."""
        rangos = [
            (1,  33, "PALABRA RESERVADA"),
            (40, 41, "DIRECTIVA PREPROCESADOR"),
            (42, 46, "LIBRERÍA ESTÁNDAR"),
            (50, 59, "FUNCIÓN INTEGRADA"),
            (60, 64, "OP. ARITMÉTICO"),
            (65, 65, "OP. ASIGNACIÓN"),
            (66, 71, "OP. RELACIONAL"),
            (72, 74, "OP. LÓGICO"),
            (75, 80, "OP. AGRUPACIÓN"),
            (92, 97, "DELIMITADOR")
        ]
        for lo, hi, desc in rangos:
            if lo <= token <= hi:
                return desc
        
        # Elementos dinámicos en los últimos valores
        mapping = {
            98:  "IDENTIFICADOR",
            99:  "NÚMERO",
            100: "CADENA"
        }
        return mapping.get(token, "DESCONOCIDO")
        
        # Elementos dinámicos en los últimos valores
        mapping = {
            98: "IDENTIFICADOR", 
            99: "NÚMERO", 
            100: "CADENA / CARACTER LITERAL"
        }
        return mapping.get(token, "DESCONOCIDO")

class AnalizadorLexico:
    """Analizador léxico de MicroC Carlos """

    def __init__(self):
        self.Lista = []      
        self._cont  = 0      
        self._Linea = 1      
    # ── Alfabetos ───────────────────────────────────────────────
    def GetAlfabetoAlfanumerico(self, c: str) -> int:
        """Retorna 1 si el carácter es letra o es un guión bajo."""
        return 1 if (c.isalpha() or c == '_') else 0

    def GetAlfabetoNumero(self, c: str) -> int:
        return 1 if c.isdigit() else 0

    def GetAlfabetoSimbolo(self, c: str) -> int:
        """Retorna 1 si el carácter es un símbolo reconocido del lenguaje."""
        return 1 if c in '+-*/=<>!&|%^~(){}[];,.' else 0

    # ── Autómatas de reconocimiento ─────────────────────────────
    def IdentificadorPalabraReservada(self, archivo: str, cont: int, linea: int, UL) -> int:
    
        lexema = ""
        while cont < len(archivo) and (archivo[cont].isalnum() or archivo[cont] == '_'):
            lexema += archivo[cont]
            cont += 1
        token = UL.GetTokenPalabra(lexema)
        tipo  = "IDENTIFICADOR" if token == 98 else "RESERVADA"
        self.Lista.append((linea, lexema, token, tipo))
        return cont

    def EnteroReal(self, archivo: str, cont: int, linea: int) -> int:

        lexema   = ""
        es_real  = False
        while cont < len(archivo) and (archivo[cont].isdigit() or archivo[cont] == '.'):
            if archivo[cont] == '.':
                if es_real:
                    break
                es_real = True
            lexema += archivo[cont]
            cont   += 1
        if lexema and lexema != '.':
            tipo  = "NUMERO_REAL" if es_real else "NUMERO_ENTERO"
            token = 99           
            self.Lista.append((linea, lexema, token, tipo))
        return cont

    def AutomataComentario(self, archivo: str, cont: int, linea: int):
        
        if cont + 1 < len(archivo):
            if archivo[cont + 1] == '/':          # Comentario en modo de linea 
                while cont < len(archivo) and archivo[cont] != '\n':
                    cont += 1
            elif archivo[cont + 1] == '*':         # Comentario de  modo de bloque
                cont += 2
                while cont + 1 < len(archivo):
                    if archivo[cont] == '\n':
                        linea += 1
                    if archivo[cont] == '*' and archivo[cont + 1] == '/':
                        cont += 2
                        break
                    cont += 1
        return cont, linea

   
    def AnalisisLexico(self, archivo: str):
        self.Lista = []
        errores    = []
        UL         = UnidadesLexicas()
        cont       = 0
        linea      = 1

        while cont < len(archivo):
            c = archivo[cont]

            # Salto de línea
            if c == '\n':
                linea += 1
                cont  += 1
                continue

            
            if c in ' \t\r':
                cont += 1
                continue

            
            if c == '"':
                lexema = '"'
                cont  += 1
                while cont < len(archivo) and archivo[cont] != '"' and archivo[cont] != '\n':
                    lexema += archivo[cont]
                    cont   += 1
                if cont < len(archivo) and archivo[cont] == '"':
                    lexema += '"'
                    cont   += 1
                self.Lista.append((linea, lexema, 100, "CADENA")) 
                continue

            
            if c == "'":
                lexema = "'"
                cont  += 1
                while cont < len(archivo) and archivo[cont] != "'" and archivo[cont] != '\n':
                    lexema += archivo[cont]
                    cont   += 1
                if cont < len(archivo) and archivo[cont] == "'":
                    lexema += "'"
                    cont   += 1
                self.Lista.append((linea, lexema, 100, "CARACTER"))
                continue

           
            if self.GetAlfabetoAlfanumerico(c):
                cont = self.IdentificadorPalabraReservada(archivo, cont, linea, UL)
                continue

            # entero o real
            if self.GetAlfabetoNumero(c):
                cont = self.EnteroReal(archivo, cont, linea)
                continue

            # comentario o división
            if c == '/':
                if cont + 1 < len(archivo) and archivo[cont + 1] in '/*':
                    cont, linea = self.AutomataComentario(archivo, cont, linea)
                else:
                    t = UL.GetTokenSimbolo('/')
                    self.Lista.append((linea, '/', t, "ARITMÉTICO"))
                    cont += 1
                continue

            # '#' → preprocesador
            if c == '#':
                lexema = '#'
                cont  += 1
                while cont < len(archivo) and archivo[cont].isalpha():
                    lexema += archivo[cont]
                    cont   += 1
                t = UL.GetTokenPalabra(lexema)
                self.Lista.append((linea, lexema, t, "PREPROCESADOR"))
                continue

            # Símbolos (intenta doble carácter primero)
            if self.GetAlfabetoSimbolo(c):
                sig    = archivo[cont + 1] if cont + 1 < len(archivo) else ''
                doble  = c + sig
                t_doble = UL.GetTokenSimbolo(doble)
                if t_doble != -1:
                    lexema = doble
                    cont  += 2
                    token  = t_doble
                else:
                    lexema = c
                    cont  += 1
                    token  = UL.GetTokenSimbolo(c)

                if token == -1:
                    errores.append((linea, lexema))
                else:
                    self.Lista.append((linea, lexema, token, self._cat_simbolo(lexema)))
                continue

            # Carácter desconocido → error léxico
            errores.append((linea, c))
            cont += 1

        return self.Lista, errores

    def _cat_simbolo(self, sym: str) -> str:
        """Clasifica un símbolo en su categoría."""
        cats = {
            frozenset(['+','-','*','/','%'])            : "ARITMÉTICO",
            frozenset(['=','++','--','+=','-=','*=','/=']): "ASIGNACIÓN",
            frozenset(['==','!=','<','>','<=','>='])     : "RELACIONAL",
            frozenset(['&&','||','!'])                   : "LÓGICO",
            frozenset(['(',')','{','}','[',']'])          : "AGRUPACIÓN",
            frozenset([';',',','.','->','::','#'])        : "MISCELÁNEO",
            frozenset(['&','|','^','~','<<','>>'])        : "BIT",
        }
        for s, t in cats.items():
            if sym in s:
                return t
        return "SÍMBOLO"



class frmEditor:

    # ── Paleta de colores ────────────────────────────────────────
    BG        = "#1e1e1e"   # Fondo del editor
    FG        = "#d4d4d4"   # Texto normal
    UI_BG     = "#252526"   # Fondo de paneles
    PANEL_BG  = "#2d2d30"   # Fondo de barras / cabeceras
    ACCENT    = "#264f78"   # Azul oscuro
    # Colores pastel para tokens
    C_RESERV  = "#9dc4e8"   # reservadas
    C_STRING  = "#f0c8a0"   # cadenas
    C_COMMENT = "#a8d8a8"   #comentarios
    C_NUMBER  = "#c8a8e8"   # números
    C_PREPROC = "#f0e0a0"   # preprocesador
    C_ERROR   = "#f08080"   # errores

    def __init__(self, root):
        self.root = root
        self.root.title("MicroC Compilador CCarlos Maldonado –  Sin Título")
        self.root.geometry("1150x820")
        self.root.configure(bg=self.UI_BG)

        self.archivo_actual    = None
        self.contenido_guardado = ""
        self._al = AnalizadorLexico()

        self._build_menu()
        self._build_ui()
        self.configurar_tags()

    
    # MENÚ 
    
    def _build_menu(self):
        mb = tk.Menu(self.root, bg=self.PANEL_BG, fg=self.FG,
                     activebackground=self.ACCENT, activeforeground="#ffffff",
                     relief="flat", bd=0)
        self.root.config(menu=mb)

        # Archivo
        m_arch = tk.Menu(mb, tearoff=0, bg=self.PANEL_BG, fg=self.FG,
                         activebackground=self.ACCENT, activeforeground="#ffffff")
        m_arch.add_command(label="Nuevo",         command=self.OpcNuevo_Click)
        m_arch.add_command(label="Abrir…",        command=self.OpcAbrir_Click)
        m_arch.add_command(label="Guardar",        command=self.OpcGuardar_Click)
        m_arch.add_command(label="Guardar como…", command=self.OpcGuardarComo_Click)
        m_arch.add_separator()
        m_arch.add_command(label="Salir",          command=self.OpcSalir_Click)
        mb.add_cascade(label="Archivos", menu=m_arch)

        # Editar
        m_edit = tk.Menu(mb, tearoff=0, bg=self.PANEL_BG, fg=self.FG,
                         activebackground=self.ACCENT, activeforeground="#ffffff")
        m_edit.add_command(label="Habilitar edición", command=self.habilitar_edicion)
        mb.add_cascade(label="Editar", menu=m_edit)

        # Compilar
        m_comp = tk.Menu(mb, tearoff=0, bg=self.PANEL_BG, fg=self.FG,
                         activebackground=self.ACCENT, activeforeground="#ffffff")
        m_comp.add_command(label="Compilar Código (F5)",
                           command=self.compilarToolStripMenuItem_Click)
        mb.add_cascade(label="Compilar", menu=m_comp)

        # Ayuda
        m_help = tk.Menu(mb, tearoff=0, bg=self.PANEL_BG, fg=self.FG,
                         activebackground=self.ACCENT, activeforeground="#ffffff")
        m_help.add_command(label="Acerca de…", command=self.mostrar_ayuda)
        mb.add_cascade(label="Ayuda", menu=m_help)

        # Atajo F5
        self.root.bind('<F5>', lambda e: self.compilarToolStripMenuItem_Click())

    
    # INTERFAZ GRÁFICA
    
    def _build_ui(self):
        # ── Etiqueta de archivo ──────────────────────────────────
        self.lbl_archivo = tk.Label(
            self.root, text="  Archivo: [Nuevo]",
            bg=self.PANEL_BG, fg="#cccccc", anchor="w",
            font=("Consolas", 9))
        self.lbl_archivo.pack(fill=tk.X, side=tk.TOP)

        # ── Panel principal (PanedWindow vertical) ───────────────
        paned = tk.PanedWindow(self.root, orient=tk.VERTICAL,
                               bg=self.UI_BG, sashwidth=4,
                               sashrelief="flat")
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # ─ Bloque EDITOR ────────────────────────────────────────
        editor_outer = tk.Frame(paned, bg=self.UI_BG)
        paned.add(editor_outer, minsize=260)

        editor_frame = tk.Frame(editor_outer, bg=self.UI_BG)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        # Números de línea
        self.line_numbers = tk.Text(
            editor_frame, width=4, padx=4, takefocus=0, border=0,
            background="#1a1a1a", foreground="#555555",
            state='disabled', font=("Consolas", 11))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Editor de código
        self.text_editor = tk.Text(
            editor_frame, undo=True, wrap="none",
            bg=self.BG, fg=self.FG, insertbackground="#aeafad",
            selectbackground=self.ACCENT, selectforeground="#ffffff",
            font=("Consolas", 12), relief="flat", bd=0)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        vsb = tk.Scrollbar(editor_frame, command=self._sync_yview,
                           bg=self.PANEL_BG, troughcolor=self.UI_BG)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.config(yscrollcommand=vsb.set)

        # Scrollbar horizontal
        hsb = tk.Scrollbar(editor_outer, orient=tk.HORIZONTAL,
                           command=self.text_editor.xview,
                           bg=self.PANEL_BG, troughcolor=self.UI_BG)
        hsb.pack(fill=tk.X)
        self.text_editor.config(xscrollcommand=hsb.set)

        self.text_editor.bind('<KeyRelease>', self._on_key)
        self.text_editor.bind('<MouseWheel>', self._actualizar_lineas)
        self.text_editor.bind('<Button-4>',   self._actualizar_lineas)
        self.text_editor.bind('<Button-5>',   self._actualizar_lineas)

        # ─ Bloque RESULTADOS (Notebook) ────────────────────────
        nb_frame = tk.Frame(paned, bg=self.UI_BG)
        paned.add(nb_frame, minsize=220)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Dark.TNotebook",
                        background=self.UI_BG, borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                        background=self.PANEL_BG, foreground="#aaaaaa",
                        padding=[10, 4], font=("Consolas", 9))
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", self.BG)],
                  foreground=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(nb_frame, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._build_tab_tokens()
        self._build_tab_errores()

       
        self.lbl_status = tk.Label(
            self.root, text="  Listo",
            bg="#007acc", fg="#ffffff", anchor="w",
            font=("Consolas", 9))
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_tab_tokens(self):
        frame = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(frame, text="  Tokens Válidos  ")

        cols = ("linea", "lexema", "token", "tipo")
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=self.BG, foreground=self.FG,
                        fieldbackground=self.BG,
                        rowheight=22, font=("Consolas", 10))
        style.configure("Dark.Treeview.Heading",
                        background=self.PANEL_BG, foreground="#9dc4e8",
                        font=("Consolas", 10, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", self.ACCENT)],
                  foreground=[("selected", "#ffffff")])

        self.tree_tokens = ttk.Treeview(frame, columns=cols,
                                        show="headings",
                                        style="Dark.Treeview")
        for col, ancho, txt in [
            ("linea",  70,  "Línea"),
            ("lexema", 200, "Lexema"),
            ("token",  80,  "Token"),
            ("tipo",   200, "Tipo / Categoría"),
        ]:
            self.tree_tokens.heading(col, text=txt)
            self.tree_tokens.column(col, width=ancho, anchor="center")

        vsb2 = ttk.Scrollbar(frame, orient="vertical",
                              command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscrollcommand=vsb2.set)
        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb2.pack(side=tk.RIGHT, fill=tk.Y)

        # Tags de color por tipo de token
        self.tree_tokens.tag_configure("reservada",   foreground=self.C_RESERV)
        self.tree_tokens.tag_configure("identificador",foreground=self.FG)
        self.tree_tokens.tag_configure("cadena",      foreground=self.C_STRING)
        self.tree_tokens.tag_configure("numero",      foreground=self.C_NUMBER)
        self.tree_tokens.tag_configure("preprocesador",foreground=self.C_PREPROC)
        self.tree_tokens.tag_configure("operador",    foreground="#a8e8e8")
        self.tree_tokens.tag_configure("agrupacion",  foreground="#c8e8c8")


    def _build_tab_errores(self):
        frame = tk.Frame(self.notebook, bg=self.BG)
        self.notebook.add(frame, text="  Errores Léxicos  ")

        cols = ("linea", "caracter", "detalle")
        self.tree_errores = ttk.Treeview(frame, columns=cols,show="headings",style="Dark.Treeview")
        for col, ancho, txt in [
            ("linea",   80,  "Línea"),
            ("caracter",120, "Carácter"),
            ("detalle", 400, "Detalle"),
        ]:
            self.tree_errores.heading(col, text=txt)
            self.tree_errores.column(col, width=ancho, anchor="center")

        vsb3 = ttk.Scrollbar(frame, orient="vertical", command=self.tree_errores.yview)
        self.tree_errores.configure(yscrollcommand=vsb3.set)
        self.tree_errores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb3.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_errores.tag_configure("error", foreground=self.C_ERROR)


    def OpcNuevo_Click(self):
        self.archivo_actual = None
        self.text_editor.delete(1.0, tk.END)
        self.habilitar_edicion()
        self.actualizar_info_archivo("[Nuevo]")
        self._set_status("Nuevo archivo creado.")

    def OpcAbrir_Click(self):
        path = filedialog.askopenfilename(
            filetypes=[("Archivos C/C++","*.c *.cpp *.h"),("Todos","*.*")])
        if not path:
            return
        self.archivo_actual = path
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        self.text_editor.config(state='normal')
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, content)
        self.contenido_guardado = content
        self.text_editor.config(state='disabled')
        self.actualizar_info_archivo(path)
        self._set_status(f"Archivo cargado: {path}  |  Modo LECTURA — pulse Editar para modificar.")
        self.resaltar_sintaxis()
        self._actualizar_lineas()

    def OpcGuardar_Click(self):
        if self.archivo_actual:
            with open(self.archivo_actual, 'w', encoding='utf-8') as f:
                content = self.text_editor.get(1.0, tk.END)
                f.write(content)
            self.contenido_guardado = content
            self._set_status(f"Guardado: {self.archivo_actual}")
        else:
            self.OpcGuardarComo_Click()

    def OpcGuardarComo_Click(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[("Archivos C","*.c"),("Archivos C++","*.cpp"),("Todos","*.*")])
        if path:
            self.archivo_actual = path
            with open(path, 'w', encoding='utf-8') as f:
                content = self.text_editor.get(1.0, tk.END)
                f.write(content)
            self.contenido_guardado = content
            self.actualizar_info_archivo(path)
            self._set_status(f"Guardado como: {path}")

    def OpcSalir_Click(self):
        actual = self.text_editor.get(1.0, tk.END).strip()
        if self.archivo_actual and actual != self.contenido_guardado.strip():
            r = messagebox.askyesnocancel("Salir","¿Desea guardar los cambios antes de salir?")
            if r is True:
                self.OpcGuardar_Click(); self.root.destroy()
            elif r is False:
                self.root.destroy()
        elif not self.archivo_actual and actual:
            r = messagebox.askyesnocancel("Salir","El archivo no está guardado. ¿Desea guardarlo?")
            if r is True:
                self.OpcGuardarComo_Click(); self.root.destroy()
            elif r is False:
                self.root.destroy()
        else:
            self.root.destroy()

    def habilitar_edicion(self):
        self.text_editor.config(state='normal')
        self._set_status("Modo EDICIÓN activado.")

    # }
    def compilarToolStripMenuItem_Click(self):
        codigo = self.text_editor.get("1.0", tk.END)

        for row in self.tree_tokens.get_children():
            self.tree_tokens.delete(row)
        for row in self.tree_errores.get_children():
            self.tree_errores.delete(row)

        al = AnalizadorLexico()
        tokens_validos, errores = al.AnalisisLexico(codigo)
        UL = UnidadesLexicas()

        # Llenar tabla de tokens
        for (linea, lexema, token, tipo) in tokens_validos:
            tag = self._tag_token(tipo)
            self.tree_tokens.insert("", tk.END,
                values=(linea, lexema, token, UL.GetDescripcionToken(token)),
                tags=(tag,))

        # Llenar tabla de errores
        for (linea, caracter) in errores:
            self.tree_errores.insert("", tk.END,
                values=(linea, repr(caracter), f"Carácter '{caracter}' no pertenece al lenguaje"),
                tags=("error",))

        n_tok = len(tokens_validos)
        n_err = len(errores)
        self._set_status(f"Análisis completado  |  Tokens válidos: {n_tok}  |  " f"Errores léxicos: {n_err}  |  Presione F5 para recompilar")

       
        self.notebook.select(0)

    def _tag_token(self, tipo: str) -> str:
        tipo = tipo.upper()
        if "RESERVADA" in tipo:        return "reservada"
        if "IDENTIFICADOR" in tipo:    return "identificador"
        if "CADENA" in tipo or "CARACTER" in tipo: return "cadena"
        if "NUMERO" in tipo:           return "numero"
        if "PREPROCESADOR" in tipo:    return "preprocesador"
        if any(x in tipo for x in ["ARITMÉTICO","ASIGNACIÓN","RELACIONAL","LÓGICO","BIT"]):
            return "operador"
        if "AGRUPACIÓN" in tipo or "MISCELÁNEO" in tipo:
            return "agrupacion"
        return ""

    
    # RESALTADO DE SINTAXIS
    
    def configurar_tags(self):
        self.text_editor.tag_config("keyword",   foreground=self.C_RESERV)
        self.text_editor.tag_config("string",    foreground=self.C_STRING)
        self.text_editor.tag_config("comment",   foreground=self.C_COMMENT)
        self.text_editor.tag_config("number",    foreground=self.C_NUMBER)
        self.text_editor.tag_config("preproc",   foreground=self.C_PREPROC)

    def resaltar_sintaxis(self):
        for tag in ["keyword","string","comment","number","preproc"]:
            self.text_editor.tag_remove(tag, "1.0", tk.END)
        texto = self.text_editor.get("1.0", tk.END)

        def marcar(pattern, tag):
            for m in re.finditer(pattern, texto):
                self.text_editor.tag_add(tag,
                    f"1.0+{m.start()}c", f"1.0+{m.end()}c")

        marcar(r'#\s*\w+',                                     "preproc")
        marcar(r'//.*',                                         "comment")
        marcar(r'/\*[\s\S]*?\*/',                               "comment")
        marcar(r'"(?:[^"\\]|\\.)*"',                            "string")
        marcar(r"'(?:[^'\\]|\\.)*'",                            "string")
        marcar(r'\b\d+\.?\d*\b',                                "number")
        marcar(
            r'\b(auto|break|case|char|const|continue|default|do|double|'
            r'else|enum|extern|float|for|goto|if|int|long|register|return|'
            r'short|signed|sizeof|static|struct|switch|typedef|union|'
            r'unsigned|void|volatile|while)\b', "keyword")

    def _on_key(self, event=None):
        self._actualizar_lineas()
        self.resaltar_sintaxis()

    def _sync_yview(self, *args):
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)

    def _actualizar_lineas(self, event=None):
        lines = self.text_editor.get('1.0', 'end-1c').count('\n') + 1
        nums  = "\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', nums)
        self.line_numbers.config(state='disabled')
        self.line_numbers.yview_moveto(self.text_editor.yview()[0])

    def actualizar_info_archivo(self, nombre):
        self.root.title(f"MicroC Compilador  –  {nombre}")
        self.lbl_archivo.config(text=f"  Archivo: {nombre}")

    def _set_status(self, msg: str):
        self.lbl_status.config(text=f"  {msg}")

    def mostrar_ayuda(self):
        messagebox.showinfo(
            "Acerca de MicroC Compilador",
            "MicroC Compilador de CArlos Maldonadon v2.0\n"
            "Curso:  Autómatas y Lenguajes\n"
            "Año:    2026  |  Semestre V\n"
            "Carrera: Ingeniería en Sistemas\n"
            "Catedrático: Ing. Baudilio Boteo\n"
            "Universidad Mesoamericana de Guatemala\n"
             "Gracias Por Utilizar el compilador, Saludos \n"
             
        )


#
if __name__ == "__main__":
    root = tk.Tk()
    app  = frmEditor(root)
    root.mainloop()