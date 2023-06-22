import os, sys

if len(sys.argv) < 2:
    print("Faltan argumentos")

path_python = sys.argv[1].replace('"', '')
os.system('virtualenv --python="{}" .venv'.format(path_python));

print("Entorno creado con python:")
os.system('{} --version'.format(path_python));