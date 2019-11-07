## Iniciar ambiente

### Requisitos

- python3
- virtualenv

### Ejecución (sobre Linux)

```bash
# Para crear el entorno virtual
$ virtualenv -p python3 venv
# Para iniciar el entorno virtual
$ . venv/bin/activate
# Instalar las dependencias dentro del entorno virtual
$ pip3 install -r requirements.txt
# En el directorio raiz
$ FLASK_ENV=dev python run.py
```

Para salir del entorno virtual, ejecutar:

```bash
$ deactivate
```


### Ejecución (sobre Windows)

```bash
# Para crear el entorno virtual
$ python3 -m venv venv
# Para iniciar el entorno virtual
$ venv\\Scripts\\activate.bat
# Instalar las dependencias dentro del entorno virtual
$ pip3 install -r requirements.txt
# En el directorio raiz
$ set FLASK_ENV=development
# Correr Flask
$ flask run
```

Para salir del entorno virtual, ejecutar:

```bash
$ deactivate
```


