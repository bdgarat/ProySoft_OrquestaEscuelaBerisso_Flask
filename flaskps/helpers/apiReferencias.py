import requests, json

def tipos_documento():
    # Armo la lista de opciones del select de tipo de documento
    tipos = []
    res = requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento")
    if res.status_code == 200:
        for r in json.loads(res.text) :
            tipos.append( (r['id'], r['nombre']) )    
    return tipos

def localidades():
    localidades = []
    res = requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad")
    if res.status_code == 200:
        for r in json.loads(res.text) :
            localidades.append( (r['id'], r['nombre']) )    
    return localidades