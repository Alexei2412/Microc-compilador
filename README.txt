# MicroC preCompiler

**Versión:** 1.0 (Release v1.0-precompilador)
**Curso:** Autómatas y Lenguajes | Universidad Mesoamericana
**Catedrático:** Ing. Baudilio Boteo

---

# Compilador MicroC

## 1. Portada
* **Nombre completo:** [Carlos Alexei Maldonado Barrios ]
* **Número de carné:** [202425512]
* **Curso:** Autómatas y Lenguajes
* **Proyecto:** Compilador MicroC

## 2. Descripción del Proyecto
CyberLex es la interfaz gráfica de un pre-compilador diseñado para el lenguaje MicroC. Permite la edición de código fuente con características modernas como resaltado de sintaxis, numeración de líneas automática y gestión segura de archivos (lectura/escritura).

## 3. Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Librerías:** `tkinter` (para la interfaz gráfica), `re` (para el análisis de expresiones regulares en el resaltado de sintaxis).

## 4. Instrucciones de Ejecución
1. Clonar este repositorio.
2. Asegurarse de tener Python instalado en el sistema.
3. Navegar a la carpeta `/src/` y ejecutar el archivo principal: `python MicroC.py`.

## 5. Enlace Drive
https://drive.google.com/drive/folders/1eJHqyPEzfrORzTe8QS3_anLo2ei0rD5o?usp=sharing

## 6. Enlace al Video Demostrativo
https://youtu.be/2ykPBbnnLfo?si=FxdjByYm4WWUIh5w

Video demostrativo
Ver el video del proyecto en YouTube

https://youtu.be/S3vFUKr6pTc


Funcionalidad completa del compilador
Implementación de (palabras reservadas, números, comentarios)


Identificación
Campo Valor 
Curso Autómatas y LenguajesAño2026 — Semestre v
 Carrera Ingeniería en Sistemas 
Catedrático Ing. Baudilio Boteo 
Universidad Mesoamericana de Guatemala
Desarrollado por Carlos Maldonado


 Implementar un analizador léxico funcional que procese código fuente
 Generar una lista estructurada de tokens
 Identificar lexemas válidos del lenguaje
 Clasificar tokens por tipo
 Respetar el límite máximo de 100 tokens


Clases implementadas Unidades Lexicas
Tabla de símbolos del lenguaje. Mapea cada lexema a su token numérico.
Método DescripciónGetTokenPalabra(lexema)Retorna token de la palabra; 98 si es identificadorGetTokenSimbolo(lexema)Retorna token del símbolo; -1 si no fue encontradoGetDescripcionToken(token)Retorna descripción legible del token
AnalizadorLexico
Implementa el análisis léxico carácter a carácter.
MétodoDescripciónGetAlfabetoAlfanumerico(c)Verifica si el char es letra o _GetAlfabetoNumero(c)Verifica si el char es un dígitoGetAlfabetoSimbolo(c)Verifica si el char es un símbolo del lenguajeIdentificadorPalabraReservada(...)Autómata 1 — Reconoce reservadas e identificadoresEnteroReal(...)Autómata 2 — Reconoce números enteros y realesAutomataComentario(...)Autómata 3 — Omite comentarios // y /* */AnalisisLexico(archivo)Función principal — Contiene el árbol de decisión
frmEditor
Frame principal de la interfaz gráfica.
FunciónAcciónOpcNuevo_Click()Nuevo archivoOpcAbrir_Click()Abrir archivo .c/.cppOpcGuardar_Click()Guardar archivo actualOpcGuardarComo_Click()Guardar como nuevo archivoOpcSalir_Click()Salir con verificación de cambioscompilarToolStripMenuItem_Click()Ejecuta el análisis léxico

El corazón del compilador es la función AnalisisLexico, un conjunto de if que valida el símbolo, encerrado en un while que existe mientras hayan caracteres en el archivo.
pythonwhile cont < len(archivo):
    c = archivo[cont]
    
    if c == '\n':                              
    elif c in ' \t\r':                         
    elif self.GetAlfabetoAlfanumerico(c):      
    elif self.GetAlfabetoNumero(c):            
    elif c == '/':                             
    elif self.GetAlfabetoSimbolo(c):           
    else:                                      

Tabla de tokens 
RangoCategoría1 – 33Palabras reservadas40 – 41Directivas preprocesador42 – 46Librerías estándar50 – 51Funciones integradas60 – 64Op. aritméticos65Op. asignación66 – 71Op. relacionales72 – 74Op. lógicos75 – 80Op. agrupación92 – 97Delimitadores98Identificador99Número100Cadena

 Cómo ejecutar
Requisitos

Python 3.6 o superior (tkinter incluido en la instalación estándar)


# Ejecutar
python Precompilador1.py
Atajos de teclado
AtajoAcciónF5Compilar / Analizar código

Bibliotecas utilizadas
Todas son parte de la librería estándar de Python 3 — no se requiere instalar nada externo.
BibliotecaUsotkinterInterfaz gráficatkinter.ttkWidgets temáticos (Treeview, Notebook)tkinter.filedialogDiálogos de archivostkinter.messageboxMensajes emergentesreExpresiones regulares (resaltado de sintaxis)webbrowserAbrir documentación desde la app

Características de la interfaz

Tema oscuro con algunos tonos de colores pastel
Editor de código con números de línea y resaltado de sintaxis
Tabla de tokens (Línea, Lexema, Token, Categoría)
Tabla de errores léxicos con ubicación de línea
Gestión completa de archivos (nuevo, abrir, guardar)
Modo lectura al abrir archivos


Fases del proyecto
Fase I — Tareas básicas

Generar lista de tokens
Eliminar espacios en blanco
Eliminar tabuladores y saltos de línea
Relacionar líneas de código con el análisis
Identificar lexemas simples

Fase II — Lista completa de tokens

Identificar palabras reservadas
Identificar números (enteros y reales)
Identificar comentarios

