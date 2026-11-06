
import requests
import json
from pathlib import Path

# Servicio ArcGIS REST del IDE Boyacá
url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

# Parámetros de consulta
params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

# Consultar el servicio
respuesta = requests.get(url, params=params, timeout=30)
respuesta.raise_for_status()

# Obtener GeoJSON
datos = respuesta.json()

# Guardar resultado
ruta_salida = Path("nivelacion/datos/veredas_tunja.geojson")
ruta_salida.parent.mkdir(parents=True, exist_ok=True)

with open(ruta_salida, "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, ensure_ascii=False, indent=2)

# Mostrar resultado
print("PUNTO 1 - DESCARGA DE VEREDAS DE TUNJA")
print("Total de veredas descargadas:", len(datos["features"]))
print("Archivo guardado en:", ruta_salida)
# PUNTO 2 - VEREDAS POR MUNICIPIO

import geopandas as gpd

gdf = gpd.read_file("nivelacion/datos/veredas_boyaca.geojson")

print("\nPUNTO 2 - VEREDAS POR MUNICIPIO")
print("Total de registros:", len(gdf))

por_municipio = (
    gdf.groupby("NOMB_MPIO")
    .size()
    .sort_values(ascending=False)
)

print("\nTOP 10 MUNICIPIOS CON MAS VEREDAS:")
print(por_municipio.head(10))
print(por_municipio.head(10))

# ==========================================
# PUNTO 3 - AREA DE VEREDAS EN HECTAREAS
# ==========================================

# Reproyectar a MAGNA-SIRGAS / Origen-Nacional
gdf_metros = gdf.to_crs(epsg=9377)

# Calcular el area en hectareas
gdf_metros["area_ha"] = gdf_metros.geometry.area / 10000

# Ordenar de mayor a menor y mostrar las 5 mas grandes
top_5 = gdf_metros.sort_values(
    by="area_ha",
    ascending=False
).head(5)

print("\nPUNTO 3 - LAS 5 VEREDAS MAS GRANDES")
print(top_5[["NOMBRE_VER", "NOMB_MPIO", "area_ha"]])