import requests, json

def tipos_documento():
    # Armo la lista de opciones del select de tipo de documento
    tipos = []
    res = requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento")
    for r in json.loads(res.text) :
        tipos.append( (r['id'], r['nombre']) )
    return tipos

def localidades():
    localidades = []
    res = requests.get("https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad")
    for l in json.loads(res.text) :
        localidades.append( (l['id'], l['nombre']) )
    return localidades