# hololive.exe

No es un virus. Es un concierto de Hololive disfrazado de hackeo.

Un script (o ejecutable) de broma que abre una "terminal de hacker", la
anima un rato, enciende el navegador, y luego suelta un monton de ventanas
emergentes con GIFs de tus vtubers favoritas mientras suena un "espiar al
cursor" de Sakura Miko que se cree el dueño de tu mouse.

**Es 100% inofensivo:** no modifica el registro, no instala nada, no roba
datos, no es malicioso. Solo usa librerias estandar de Python y GIFs que se
descargan de Tenor.

## Que hace (el "hack")

1. Crea una ventana estilo terminal negra con texto verde.
2. Escribe linea a linea un "acceso a una base de datos" falsa: bypass de
   firewall, escaneo de puertos, decryption de archivos clasificados de
   Marine-chan, el famoso PEKOPEKOPEKO.exe...
3. Al terminar abre tu navegador en [github.com/Sureshum](https://github.com/Sureshum).
4. Convierte la ventana en un **Panel de Control**.
5. Empieza a lanzar pop-ups random con GIFs de Hololive y mensajes absurdos
   ("Gura te vigila", "Calli necesita otro cafe antes de streamear"...).
6. Y por si fuera poco, un GIF de Sakura Miko empieza a perseguir tu cursor.
   Si lo tocas, se enoja, se mueve solo y **arrastra tu mouse detrás de él**
   durante unos segundos. Despues te devuelve el control. Mala mia, Miko.

Bonus: si intentas cerrar un pop-up, te responde con un mensaje troll y
aparece otro pop-up: "No puedes cerrarme :v".

## Como ejecutarlo

### Opcion facil: el .exe (recomendada)

1. Descarga `hololive.exe` desde [Releases](https://github.com/Sureshum/hololive.exe/releases).
2. Haz doble click. Eso es todo.
3. La primera vez descarga los GIFs a una carpeta `gifs/` que se crea al lado
   del exe. La segunda vez ya va rapido.

### Opcion de velocidad: python

Necesitas Python 3 con tkinter (viene incluido en Windows).

```bash
python simulacion_hack.pyw
```

o, si quieres ver la consola:

```bash
python simulacion_hack.py
```

## Como CERRAR TODO (importante)

- **Boton `CERRAR TODO`** en el Panel de Control. Es el boton rojo, no te equivoques.
- **Tecla `Escape`**.
- **Codigo Konami**: `arriba, abajo, arriba, abajo, izquierda, derecha, izquierda, derecha`.
- **X de la ventana** del Panel de Control (esto cierra todo, incluidas las Miko furiosas).
- Y el clasico de emergencia: `Ctrl+Shift+Esc` para matar el proceso si acaso
  se vuelve un show (no deberia, pero que se note que lo puedes cerrar).

## Es realmente seguro?

- Solo librerias estandar de Python (tkinter, os, random, threading, ctypes...).
- Los GIFs son fotos, no codigo: se descargan, se muestran, y listo. Nunca se ejecutan.
- No hay tokens ni datos personales en el repo.
- Secret scanning y push protection activados por si alguien intenta colar algo.

## Cosas tecnicas (si te importa)

- `simulacion_hack.py` — el codigo completo.
- `simulacion_hack.pyw` — launcher sin consola para Windows.
- El exe se compila con PyInstaller: `pyinstaller --onefile --noconsole simulacion_hack.py`.
- Los GIFs se cachean en memoria: cada uno se decodifica una sola vez.

Hubo una vez que el archivo se corrompio a bytes nulos y se recupero desde el
`.pyc` byte a byte. Ya no, eso queda en la leyenda.