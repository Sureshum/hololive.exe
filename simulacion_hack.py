"""
Simulacion de hackeo educativo e inofensivo: terminal hacker con GIFs de
Hololive, pop-ups, panel de control y un GIF que persigue y secuestra el cursor.

Librerias: solo estandar (tkinter, webbrowser, threading, time, random,
sys, os, math, urllib, hashlib, ctypes).

Los GIFs se descargan de Tenor a la carpeta gifs/ y se reproducen frame a
frame con tk.PhotoImage. NO modifica el registro ni instala nada.
"""
import tkinter as tk
import webbrowser
import threading
import time
import random
import sys
import os
import math
import urllib.request
import hashlib

try:
    import ctypes
    _user32 = ctypes.windll.user32
except Exception:
    _user32 = None


URL_OBJETIVO = "https://github.com/Sureshum"

GIFS_URLS = [
    "https://media.tenor.com/bL43BZiZnXEAAAAi/oozaru-subaru-hololive.gif",
    "https://media1.tenor.com/m/WrxBjnWiMV4AAAAC/watame-hololive.gif",
    "https://media1.tenor.com/m/_hreEWGoWC4AAAAC/holo-live-mococo-abyssgard.gif",
    "https://media1.tenor.com/m/R-a5-cXSVe0AAAAC/fuwamoco-hololive.gif",
    "https://media.tenor.com/b3K63KIGLoMAAAAi/omaru-polka-hololive.gif",
    "https://media.tenor.com/RqoW_pqn8G4AAAAi/hololive-headpat.gif",
    "https://media.tenor.com/fV7feGHnwp0AAAAi/nekomata-okayu-okayu-nekomata.gif",
    "https://media.tenor.com/90baPaupRTIAAAAi/sakura-miko-hololive.gif",
]

GIF_SIGUE_CURSOR_URL = "https://media.tenor.com/90baPaupRTIAAAAi/sakura-miko-hololive.gif"

MENSAJES_HOLOLIVE = [
    "¡ATENCION! Se detecto una cantidad rara de streams de Hololive EN",
    "EXTRAYENDO datos... Gura te vigila",
    "ADVERTENCIA: ina hackeo las galletas de la abuela",
    "SCANNING... Se encontro algo interesante en la base de datos",
    "Filtracion de datos: Calli necesita otro cafe antes de streamear",
    "ALERTA: Pekora esta provocando destruccion masiva con sus planes",
    "ACCESO CONCEDIDO a la carpeta [CLASIFICADO]",
    "DECRYPTANDO... El secreto de Watame: siempre llora",
    "SISTEMA COMPROMETIDO por 1000 grems de Gigi",
    "BYPASS exitoso: Mococo esta gritando demasiado fuerte",
]

MENSAJES_TROLEO = [
    "No puedes cerrarme :v",
    "Intentalo de nuevo >:D",
    "Ja, pensaste que me habias cerrado?",
    "Ese boton no hace nada",
    "ERROR 404: la boton de cerrar no existe",
    "no te rindas, cierra otra vez",
    "eso no funciona",
    "La mejor jugada de Pekora: nunca cerrarse",
    "Esto no es un virus, es un concierto de Hololive",
]

LINEAS_BOOT = [
    "> __________________________________________________",
    "[+] Iniciando protocolo de acceso...",
    "[*] Bypass de firewall... OK",
    "[+] Escaneando puertos virtuales... 80, 443, 8080",
    "[*] Extrayendo metadatos del sistema...",
    "[!] Detectado: fans de Hololive en red local",
    "[+] Cargando base de datos de memes...",
    "[*] Decryptando archivos clasificados de Marine-chan...",
    "[!] ADVERTENCIA: Gura dijo 'a' 1,247 veces en el sistema",
    "[+] Compilando datos de vtubers...",
    "[*] Inyeccion de codigo: PEKOPEKOPEKO.exe",
    "[!] SISTEMA COMPROMETIDO (en buen plan)",
    "[+] Accediendo a GitHub de Sureshum...",
    "[v] HACK COMPLETADO EXITOSAMENTE - Modo Hololive activado",
    "> __________________________________________________",
    "",
    "  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^",
    "  | | | | DALE UN CLICK A CERRAR TODO | | | | | |",
    "  v v v v v v v v v v v v v v v v v v v v v v v v",
    "",
]


GIFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gifs")

VERDE = "#39FF14"
VERDE_OSC = "#0a3d0a"
NEGRO = "#050505"
ROJO = "#FF0040"

CACHE_GIFS = {}


def _obtener_gif_cacheado(ruta_archivo):
    """Devuelve (frames, delays) de un GIF, decodificandolo una sola vez.

    Los frames quedan en caché a nivel de módulo y son compartidos por
    todos los pop-up, así cada GIF solo se procesa una vez por ejecución.
    """
    if ruta_archivo not in CACHE_GIFS:
        CACHE_GIFS[ruta_archivo] = cargar_frames_gif(ruta_archivo)
    return CACHE_GIFS[ruta_archivo]


def descargar_gifs():
    """Descarga los GIFs de Tenor a la carpeta local si no existen."""
    os.makedirs(GIFS_DIR, exist_ok=True)
    descargados = 0

    for i, url in enumerate(GIFS_URLS):
        nombre = hashlib.md5(url.encode()).hexdigest()[:8] + ".gif"
        ruta = os.path.join(GIFS_DIR, nombre)

        if os.path.isfile(ruta):
            continue

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                datos = resp.read()
            with open(ruta, "wb") as f:
                f.write(datos)
                descargados += 1
        except Exception:
            continue

    return descargados


def listar_gifs_locales():
    """Retorna la lista de rutas de los GIFs descargados en la carpeta local."""
    if not os.path.isdir(GIFS_DIR):
        return []
    return [
        os.path.join(GIFS_DIR, f)
        for f in os.listdir(GIFS_DIR)
        if f.lower().endswith(".gif")
    ]


def _parsear_delays_gif(ruta_archivo):
    """Extrae el delay (en ms) de cada frame de un archivo GIF."""
    delays = []
    try:
        with open(ruta_archivo, "rb") as f:
            datos = f.read()
    except Exception:
        return delays

    i = 0
    longitud = len(datos)

    if longitud < 13 or datos[0:6] not in (b"GIF87a", b"GIF89a"):
        return delays

    i = 6 + 7
    if i >= longitud:
        return delays

    if datos[i] == 0x21:
        Netscape = datos[i + 1] if i + 1 < longitud else 0
        if Netscape == 0xFF and i + 18 < longitud:
            bloq = datos[i + 15]
            if bloq == 3:
                i += 19

    while i < longitud - 1:
        byte = datos[i]
        if byte == 0x2C:
            i += 9
            if i >= longitud:
                break
            if datos[i] & 0x80:
                tam_p = 3 * (2 ** ((datos[i] & 0x07) + 1))
                i += tam_p
            i += 1

            while i < longitud and datos[i] != 0:
                tam_bloq = datos[i]
                i += 1 + tam_bloq

        elif byte == 0x21:
            i += 1
            if i >= longitud:
                break
            etiqueta = datos[i]
            i += 1

            if etiqueta == 0xF9 and i + 5 < longitud:
                delay_cs = datos[i + 2] | (datos[i + 3] << 8)
                delays.append(max(delay_cs * 10, 10))
                tam = datos[i + 4]
                i += 1 + tam + 1

            else:
                while i < longitud and datos[i] != 0:
                    tam_bloq = datos[i]
                    i += 1 + tam_bloq

        elif byte == 0x3B:
            break
        else:
            i += 1

    return delays


def cargar_frames_gif(ruta_archivo, max_ancho=180, max_alto=150):
    """Carga los frames de un GIF animado y los retorna como (frames, delays).

    Cada frame es un tk.PhotoImage ya redimensionado. Cada delay es el
    tiempo en ms que debe esperarse antes de mostrar el siguiente frame.
    """

    delays_raw = _parsear_delays_gif(ruta_archivo)

    frames = []
    delays = []
    indice = 0
    try:
        while True:
            frame = tk.PhotoImage(file=ruta_archivo, format=f"gif -index {indice}")
            ancho, alto = frame.width(), frame.height()

            factor = max(1, math.ceil(max(ancho / max_ancho, alto / max_alto)))
            if factor > 1:
                frame = frame.subsample(factor, factor)

            frames.append(frame)
            if indice < len(delays_raw):
                delays.append(max(delays_raw[indice], 30))
            else:
                delays.append(80)
            indice += 1
    except tk.TclError:
        pass

    if not delays:
        delays = [80] * len(frames)

    return frames, delays


class PerseguidorGif:
    """GIF regalón que persigue al cursor.

    Fase persecución: la ventanita (sin bordes y con fondo transparente)
    sigue al mouse con suavizado, como un gato espiando un puntero láser.

    Fase captura: si el cursor toca el GIF, este se enoja, se mueve solo
    por la pantalla y ARRASTRA el cursor real detrás de él (control total
    del movimiento del ratón) durante unos segundos.
    """

    FANTASMA = "#FF00FE"

    def __init__(self, root):
        self.root = root
        self.activo = True
        self.capturado = False
        self.tiempo_libertad = time.time() + 2.0
        self.tiempo_captura = 0.0
        self.indice_frame = 0
        self.vx = random.uniform(-9, 9) or 6
        self.vy = random.uniform(-9, 9) or 6
        self.ref_imagen = None

        gifs = listar_gifs_locales()
        if not gifs:
            self.activo = False
            return
        ruta_cursor = os.path.join(
            GIFS_DIR,
            hashlib.md5(GIF_SIGUE_CURSOR_URL.encode()).hexdigest()[:8] + ".gif",
        )
        if os.path.isfile(ruta_cursor):
            gifs = [ruta_cursor]
        self.frames, self.delays = cargar_frames_gif(gifs[0], 64, 64)
        if not self.frames:
            self.activo = False
            return

        self.gw = self.frames[0].width()
        self.gh = self.frames[0].height()

        self._obtener_escala()

        ancho_scr = self.root.winfo_screenwidth()
        alto_scr = self.root.winfo_screenheight()
        x = random.randint(0, max(ancho_scr - self.gw, 0))
        y = random.randint(0, max(alto_scr - self.gh, 0))

        self.ventana = tk.Toplevel(root)
        self.ventana.overrideredirect(True)
        self.ventana.attributes("-topmost", True)
        self.ventana.attributes("-transparentcolor", self.FANTASMA)
        self.ventana.configure(bg=self.FANTASMA, cursor="crosshair")
        self.ventana.geometry(f"+{x}+{y}")

        self.etiqueta = tk.Label(
            self.ventana, bg=self.FANTASMA, bd=0,
            highlightthickness=0, cursor="crosshair"
        )
        self.etiqueta.pack()

        self._animar()
        self._seguir()

    def _obtener_escala(self):
        self.sx = 1.0
        self.sy = 1.0
        if _user32 is None:
            return
        try:
            ancho_f = _user32.GetSystemMetrics(0)
            alto_f = _user32.GetSystemMetrics(1)
            ancho_l = self.root.winfo_screenwidth()
            alto_l = self.root.winfo_screenheight()
            self.sx = ancho_f / ancho_l if ancho_l else 1.0
            self.sy = alto_f / alto_l if alto_l else 1.0
        except Exception:
            pass

    def _mover_cursor(self, x, y):
        if _user32 is None:
            return
        try:
            _user32.SetCursorPos(int(x * self.sx), int(y * self.sy))
        except Exception:
            pass

    def _animar(self):
        if not self.activo:
            return
        try:
            if not self.ventana.winfo_exists():
                self.activo = False
                return
        except tk.TclError:
            self.activo = False
            return
        frame = self.frames[self.indice_frame % len(self.frames)]
        self.etiqueta.config(image=frame)
        self.ref_imagen = frame
        self.indice_frame += 1
        delay = self.delays[self.indice_frame % len(self.delays)]
        self.ventana.after(delay, self._animar)

    def _seguir(self):
        if not self.activo:
            return
        try:
            if not self.ventana.winfo_exists():
                self.activo = False
                return
        except tk.TclError:
            self.activo = False
            return

        ahora = time.time()
        mx = self.ventana.winfo_pointerx()
        my = self.ventana.winfo_pointery()
        gx = self.ventana.winfo_x()
        gy = self.ventana.winfo_y()
        lim_x = max(self.root.winfo_screenwidth() - self.gw, 0)
        lim_y = max(self.root.winfo_screenheight() - self.gh, 0)

        dist_cursor = math.hypot(
            mx - (gx + self.gw / 2),
            my - (gy + self.gh / 2),
        )

        if self.capturado:
            if ahora < self.tiempo_captura:
                self.vx += random.uniform(-2, 2)
                self.vy += random.uniform(-2, 2)
                nx = gx + self.vx
                ny = gy + self.vy
                if nx < 0 or nx > lim_x:
                    self.vx = -self.vx
                    nx = max(0, min(nx, lim_x))
                if ny < 0 or ny > lim_y:
                    self.vy = -self.vy
                    ny = max(0, min(ny, lim_y))
                self.ventana.geometry(f"+{int(nx)}+{int(ny)}")
                self._mover_cursor(nx + self.gw / 2, ny + self.gh / 2)
            else:
                self.capturado = False
                self.tiempo_libertad = ahora + 1.0
        else:
            if dist_cursor < 20 and ahora >= self.tiempo_libertad:
                self.capturado = True
                self.tiempo_captura = ahora + random.uniform(3.0, 5.0)
                self.vx = random.uniform(-9, 9) or 6
                self.vy = random.uniform(-9, 9) or 6
            else:
                objetivo_x = mx - self.gw / 2
                objetivo_y = my - self.gh / 2
                gx += (objetivo_x - gx) * 0.05
                gy += (objetivo_y - gy) * 0.05
                gx = max(0, min(int(gx), lim_x))
                gy = max(0, min(int(gy), lim_y))
                self.ventana.geometry(f"+{int(gx)}+{int(gy)}")

        self.ventana.after(15, self._seguir)

    def cerrar(self):
        self.activo = False
        try:
            if self.ventana.winfo_exists():
                self.ventana.destroy()
        except Exception:
            pass


class HololivePopup:
    """Ventana emergente flotante con GIF animado y mensaje de Hololive."""

    def __init__(self, master, mensaje, indice, simulador=None):
        self.simulador = simulador
        self.ventana = tk.Toplevel(master)
        self.ventana.title(f"Hackeo #{indice + 1}")
        self.ventana.configure(bg="#1a1a2e", cursor="crosshair")
        self.ventana.resizable(False, False)
        self.ventana.attributes("-topmost", True)

        pos_x = random.randint(60, 750)
        pos_y = random.randint(40, 420)
        self.ventana.geometry(f"360x300+{pos_x}+{pos_y}")

        marco = tk.Frame(self.ventana, bg="#0d0d1a", bd=3, relief="ridge")
        marco.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            marco, text="  HACKED  ",
            font=("Consolas", 16, "bold"), fg=ROJO, bg="#0d0d1a"
        ).pack(pady=(8, 0))

        self.frames, self.delays = self._elegir_gif()
        self.label_gif = tk.Label(marco, bg="#0d0d1a")
        self.label_gif.pack(pady=4)
        self.after_id = None

        if self.frames:
            self._animar_gif(0)
        else:
            self.label_gif.config(
                text="(>.<)", font=("Consolas", 22, "bold"), fg=VERDE
            )

        tk.Label(
            marco, text=mensaje, font=("Consolas", 9),
            fg=VERDE, bg="#0d0d1a", wraplength=320, justify="center"
        ).pack(pady=4, padx=6)

        tk.Label(
            marco, text="~ Hololive Security Division ~",
            font=("Arial", 8, "italic"), fg="#888888", bg="#0d0d1a"
        ).pack(pady=(0, 4))

        tk.Button(
            marco, text="CERRAR", font=("Consolas", 10, "bold"),
            fg="#FFFFFF", bg="#AA0000",
            activebackground="#FF0000", activeforeground="#FFFFFF",
            relief="raised", bd=2, command=self.cerrar,
            cursor="hand2", padx=18, pady=4
        ).pack(pady=(0, 6))

        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

    def _elegir_gif(self):
        gifs_disponibles = listar_gifs_locales()
        if not gifs_disponibles:
            return [], []
        return _obtener_gif_cacheado(random.choice(gifs_disponibles))

    def _animar_gif(self, indice):
        if not self.frames or not self.ventana.winfo_exists():
            return
        frame = self.frames[indice % len(self.frames)]
        self.label_gif.config(image=frame)
        self.ref_imagen = frame
        delay = self.delays[indice % len(self.delays)]
        self.after_id = self.ventana.after(
            delay, lambda: self._animar_gif(indice + 1)
        )

    def cerrar(self):
        if self.after_id is not None:
            try:
                self.ventana.after_cancel(self.after_id)
                self.after_id = None
            except Exception:
                pass
        if self.ventana.winfo_exists():
            self.ventana.destroy()
        if self.simulador and not self.simulador.cerrando_todo:
            self.simulador._spawn_troleo()


class SimuladorHack:
    """Coordina la pantalla de arranque, el navegador y las ventanas emergentes."""

    KONAMI = ["Up", "Down", "Up", "Down", "Left", "Right", "Left", "Right"]

    def __init__(self):
        self.root = None
        self.ventanas = []
        self.cerrando_todo = False
        self.konami_buffer = []
        self.perseguidor = None

    def iniciar(self):

        nuevos = descargar_gifs()

        self.root = tk.Tk()
        self.root.title("Inicializando sistema...")
        self.root.configure(bg=NEGRO, cursor="crosshair")
        self.root.geometry("680x460")
        self.root.attributes("-topmost", True)

        self.pantalla = tk.Text(
            self.root, bg=NEGRO, fg=VERDE, font=("Consolas", 12),
            insertbackground=VERDE, relief="flat", padx=12, pady=8,
            state="disabled", wrap="none", cursor="crosshair"
        )
        self.pantalla.pack(fill="both", expand=True)

        self.root.protocol("WM_DELETE_WINDOW", self._cerrar_todas)
        self.perseguidor = PerseguidorGif(self.root)

        self._precalentar_gifs()

        gifs_total = len(listar_gifs_locales())
        LINEAS_BOOT.insert(7, f"[+] GIFs cargados: {gifs_total} ({nuevos} nuevos descargados)")

        self._escribir_linea(0)
        self.root.mainloop()

    def _precalentar_gifs(self):
        """Decodifica los GIFs una sola vez antes del boot para que los pop-ups abran al instante."""
        gifs = listar_gifs_locales()
        if not gifs:
            return
        self.pantalla.configure(state="normal")
        self.pantalla.insert("end", "[*] Optimizando GIFs de animacion...\n")
        self.pantalla.configure(state="disabled")
        self.root.update_idletasks()
        for ruta in gifs:
            if self.cerrando_todo:
                return
            _obtener_gif_cacheado(ruta)
            self.pantalla.configure(state="normal")
            self.pantalla.insert("end", f"[+] GIF listo: {os.path.basename(ruta)}\n")
            self.pantalla.configure(state="disabled")
            self.root.update()

    def _escribir_linea(self, indice):

        if indice >= len(LINEAS_BOOT):
            self._fin_boot()
            return

        self.pantalla.configure(state="normal")
        self.pantalla.insert("end", LINEAS_BOOT[indice] + "\n")
        self.pantalla.configure(state="disabled")
        self.pantalla.see("end")

        if "COMPLETADO" in LINEAS_BOOT[indice]:
            delay = 800
        else:
            delay = random.randint(120, 450)
        self.root.after(delay, lambda: self._escribir_linea(indice + 1))

    def _fin_boot(self):

        webbrowser.open(URL_OBJETIVO)

        self.pantalla.destroy()
        self.root.geometry("360x220")
        self.root.title("Panel de control")
        self._crear_panel_control()

        self.root.bind("<Escape>", lambda e: self._cerrar_todas())
        for tecla in ["Up", "Down", "Left", "Right"]:
            self.root.bind(f"<{tecla}>", self._konami_handler)

        hilo = threading.Thread(target=self._lanzar_popups, daemon=True)
        hilo.start()

    def _crear_panel_control(self):
        tk.Label(
            self.root, text="> PANEL DE CONTROL <",
            font=("Consolas", 12, "bold"), fg=VERDE, bg=NEGRO
        ).pack(pady=(14, 4))

        tk.Label(
            self.root, text="Esc / Konami / Boton = cerrar todo",
            font=("Arial", 9), fg="#AAAAAA", bg=NEGRO
        ).pack(pady=2)

        tk.Button(
            self.root, text="CERRAR TODO", font=("Consolas", 11, "bold"),
            fg="#FFFFFF", bg="#AA0000",
            activebackground="#FF0000", activeforeground="#FFFFFF",
            command=self._cerrar_todas, relief="raised", bd=3,
            cursor="hand2", padx=20, pady=6
        ).pack(pady=12)

        tk.Label(
            self.root, text="secreto:  up down up down left right left right",
            font=("Consolas", 8), fg="#39FF14", bg=NEGRO
        ).pack(pady=(0, 8))

    def _konami_handler(self, event):
        self.konami_buffer.append(event.keysym)
        if len(self.konami_buffer) > len(self.KONAMI):
            self.konami_buffer = self.konami_buffer[-len(self.KONAMI):]

        if self.konami_buffer == self.KONAMI:
            print("[!] Codigo Konami! Cerrando todo...")
            self._cerrar_todas()

    def _lanzar_popups(self):
        for i, mensaje in enumerate(MENSAJES_HOLOLIVE):
            if self.cerrando_todo:
                return
            self.root.after(0, lambda m=mensaje, i=i: self._crear_popup(m, i))
            time.sleep(random.uniform(1.5, 3.0))

    def _crear_popup(self, mensaje, indice):
        if self.cerrando_todo or not (self.root and self.root.winfo_exists()):
            return
        popup = HololivePopup(self.root, mensaje, indice, self)
        self.ventanas.append(popup)

    def _spawn_troleo(self):
        if self.cerrando_todo or not (self.root and self.root.winfo_exists()):
            return
        mensaje = random.choice(MENSAJES_TROLEO)
        self.root.after(400, lambda: self._crear_popup_troleo(mensaje))

    def _crear_popup_troleo(self, mensaje):
        if self.cerrando_todo or not (self.root and self.root.winfo_exists()):
            return
        self._crear_popup(mensaje, len(self.ventanas) + 1)

    def _cerrar_todas(self):
        if self.cerrando_todo:
            return
        self.cerrando_todo = True
        if self.perseguidor is not None:
            try:
                self.perseguidor.cerrar()
            except Exception:
                pass
            self.perseguidor = None
        for popup in self.ventanas:
            try:
                popup.cerrar()
            except Exception:
                pass
        self.ventanas.clear()
        if self.root and self.root.winfo_exists():
            self.root.destroy()


if __name__ == "__main__":
    simulador = SimuladorHack()
    simulador.iniciar()
