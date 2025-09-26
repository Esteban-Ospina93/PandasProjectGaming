# Generador de dataset sintético (100,000 registros)
# Creará: ventas_sinteticas_100k.csv, ventas_sinteticas_100k.xlsx
import os, random, math, datetime
import pandas as pd
import numpy as np
from pathlib import Path

random.seed(42)
np.random.seed(42)

N = 100_000

# Crear carpeta output en el directorio del proyecto
out_dir = Path(__file__).resolve().parent / "output"
out_dir.mkdir(parents=True, exist_ok=True)

# Listas base (nombres, apellidos, vendedores, ciudades)
first_names = ["Juan","Carlos","Andrés","Luis","Mateo","Sofía","María","Valentina","Camila","Isabella",
               "Daniel","Sebastián","Alejandro","Laura","Mónica","Diego","Andrés","Miguel","Fernando","Natalia"]
last_names = ["García","Martínez","Rodríguez","González","Pérez","López","Ramírez","Sánchez","Torres","Rivera",
              "Castillo","Vega","Ríos","Cruz","Ortiz","Ruiz","Díaz","Suárez","Molina","Romero"]
sellers = ["Andrés Morales","Camila Rojas","Diego Castro","Laura Fernández","Miguel Herrera",
           "Sergio Valdez","Paula Gómez","Natalia Suárez","Felipe Díaz","Julia Cárdenas"]
cities = ["Bogotá","Medellín","Cali","Barranquilla","Bucaramanga","Pereira","Manizales","Ibagué","Cartagena","Santa Marta"]

# Productos para armar PC gamer (variedad) y categorías
products = [
    ("Procesador Intel i5 12400F","CPU"),
    ("Procesador AMD Ryzen 5 5600X","CPU"),
    ("Placa Madre B660","Motherboard"),
    ("Placa Madre B550","Motherboard"),
    ("Memoria RAM 16GB DDR4","RAM"),
    ("Memoria RAM 32GB DDR4","RAM"),
    ("Tarjeta Gráfica GTX 1660","GPU"),
    ("Tarjeta Gráfica RTX 3060","GPU"),
    ("Tarjeta Gráfica RTX 4070","GPU"),
    ("SSD NVMe 500GB","Storage"),
    ("SSD NVMe 1TB","Storage"),
    ("Disco HDD 2TB","Storage"),
    ("Fuente 650W 80+ Bronze","PSU"),
    ("Fuente 750W 80+ Gold","PSU"),
    ("Gabinete Mid Tower","Case"),
    ("Cooler por aire CPU","Cooling"),
    ("Disipador líquido 240mm","Cooling"),
    ("Monitor 24 pulgadas 144Hz","Monitor"),
    ("Monitor 27 pulgadas 165Hz","Monitor"),
    ("Teclado mecánico RGB","Peripherals"),
    ("Mouse gaming 16000 DPI","Peripherals"),
    ("Auriculares gaming con micrófono","Peripherals"),
    ("Placa de video usada GTX 1070 (refurb)","GPU"),
    ("Caja para SSD/HDD","Accessories")
]

# Asignar precios aproximados (COP)
base_price_map = {
    "Procesador Intel i5 12400F": 700000,
    "Procesador AMD Ryzen 5 5600X": 850000,
    "Placa Madre B660": 450000,
    "Placa Madre B550": 520000,
    "Memoria RAM 16GB DDR4": 250000,
    "Memoria RAM 32GB DDR4": 420000,
    "Tarjeta Gráfica GTX 1660": 1200000,
    "Tarjeta Gráfica RTX 3060": 2200000,
    "Tarjeta Gráfica RTX 4070": 4200000,
    "SSD NVMe 500GB": 280000,
    "SSD NVMe 1TB": 480000,
    "Disco HDD 2TB": 220000,
    "Fuente 650W 80+ Bronze": 320000,
    "Fuente 750W 80+ Gold": 480000,
    "Gabinete Mid Tower": 180000,
    "Cooler por aire CPU": 90000,
    "Disipador líquido 240mm": 360000,
    "Monitor 24 pulgadas 144Hz": 900000,
    "Monitor 27 pulgadas 165Hz": 1400000,
    "Teclado mecánico RGB": 220000,
    "Mouse gaming 16000 DPI": 120000,
    "Auriculares gaming con micrófono": 180000,
    "Placa de video usada GTX 1070 (refurb)": 700000,
    "Caja para SSD/HDD": 60000
}

# Función para generar nombre completo aleatorio
def gen_name():
    return f"{random.choice(first_names)} {random.choice(last_names)} {random.choice(last_names)}"

# Generar arrays
clientes = [gen_name() for _ in range(N)]
prod_choices = [p[0] for p in products]
producto = np.random.choice(prod_choices, size=N, replace=True)
categoria = [next(cat for (name,cat) in products if name==p) for p in producto]

# Precios desde map
precio = []
for p in producto:
    base = base_price_map[p]
    factor = random.uniform(0.9,1.2)
    val = int(round((base * factor) / 1000.0) * 1000)
    precio.append(val)

cantidad = np.random.randint(1,9,size=N)
ciudad = np.random.choice(cities, size=N)
vendedor = np.random.choice(sellers, size=N)

today = datetime.date.today()
start_date = today - datetime.timedelta(days=365)
fecha = [start_date + datetime.timedelta(days=int(x)) for x in np.random.randint(0,366,size=N)]
estados = np.random.choice(["Cerrado","Pendiente","Cancelado"], size=N, p=[0.75,0.18,0.07])

valor_venta = [int(p*q) for p,q in zip(precio,cantidad)]
comision = [round(v*0.05,2) for v in valor_venta]

# Introducir algunos valores nulos
for col, arr in [("CLIENTE", clientes), ("PRODUCTO", producto), ("VALOR_VENTA", valor_venta)]:
    idxs = np.random.choice(N, size=20, replace=False)
    for i in idxs:
        if col=="CLIENTE":
            clientes[i] = None
        elif col=="PRODUCTO":
            producto[i] = None
        elif col=="VALOR_VENTA":
            valor_venta[i] = 0

# Crear DataFrame
df = pd.DataFrame({
    "CLIENTE": clientes,
    "PRODUCTO": producto,
    "PRECIO": precio,
    "CANTIDAD": cantidad,
    "CIUDAD": ciudad,
    "VENDEDOR": vendedor,
    "FECHA": pd.to_datetime(fecha),
    "ESTADO": estados,
    "VALOR_VENTA": valor_venta,
    "COMISION": comision,
    "CATEGORIA": categoria
})

# Guardar en CSV y Excel
csv_path = out_dir / "ventas_sinteticas_100k.csv"
xlsx_path = out_dir / "ventas_sinteticas_100k.xlsx"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
df.to_excel(xlsx_path, index=False, engine="openpyxl")

# Guardar informe como DOC
doc_path = out_dir / "informe_administrativo.doc"
with open(doc_path, "w", encoding="utf-8") as f:
    f.write("Informe administrativo de ventas - generado correctamente.\n")

print(f"✅ Archivos exportados en: {out_dir}")
print(f"- CSV: {csv_path}")
print(f"- XLSX: {xlsx_path}")
print(f"- DOC: {doc_path}")
