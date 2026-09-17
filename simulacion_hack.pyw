""

import os
import runpy
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
os.chdir(CARPETA)
sys.path.insert(0, CARPETA)

route = os.path.join(CARPETA, "simulacion_hack.py")
runpy.run_path(route, run_name="__main__")