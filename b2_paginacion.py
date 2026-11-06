
import requests

# Servicio de veredas de Boyaca
url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

# Parametros de consulta del ejercicio B2
base = {
    "where": "COD_DPTO='15'",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson",
    "orderByFields": "OBJECTID ASC"
}
prueba = requests.get(
    url,
    params={**base, "f": "json", "returnCountOnly": "true"},
    timeout=60
)

print("CONTEO DIRECTO DEL SERVICIO:", prueba.json())

# Paginacion
features = []
offset = 0
bloque = 500

while True:
    parametros = {
        **base,
        "resultOffset": offset,
        "resultRecordCount": bloque
    }

    respuesta = requests.get(url, params=parametros, timeout=60)

    if respuesta.status_code != 200:
        print("Error:", respuesta.status_code)
        print(respuesta.text)
        break

    datos = respuesta.json()

    if "error" in datos:
        print("Error de ArcGIS:", datos["error"])
        break

    nuevos = datos.get("features", [])
    features.extend(nuevos)

    print(f"Offset {offset}: {len(nuevos)} registros")

    if len(nuevos) < bloque:
        break

    offset += bloque

# Total recuperado
print("\nTOTAL DE VEREDAS RECUPERADAS:", len(features))

# Municipios distintos
municipios = {
    f["properties"]["NOMB_MPIO"]
    for f in features
    if f.get("properties", {}).get("NOMB_MPIO")
}

print("TOTAL DE MUNICIPIOS DISTINTOS:", len(municipios))
print("MUNICIPIOS:", sorted(municipios))
