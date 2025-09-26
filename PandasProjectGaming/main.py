import pandas as pd
import os


# ==============================
# Cargar datos
# ==============================
base_dir = os.path.dirname(__file__)   # carpeta donde está main.py
file_path = os.path.join(base_dir, "output", "ventas_sinteticas_100k.xlsx")

df = pd.read_excel(file_path)

# Convertir fechas
df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

print("========== INFORME ADMINISTRATIVO ==========\n")

# 1. Total de registros
print("1. Total de registros (ventas):", len(df))

# 2. Ventas por estado
print("\n2. Ventas por estado:")
print(df["ESTADO"].value_counts())

# 3. Valor total de ventas
print("\n3. Valor total de ventas realizadas:", df["VALOR_VENTA"].sum())

# 4. Promedio de comisión en ventas cerradas
df["ESTADO"] = df["ESTADO"].str.strip().str.capitalize()
cerradas = df[df["ESTADO"] == "Cerrado"]
print("\n4. Promedio comisión ventas cerradas:", cerradas["COMISION"].mean())

# 5. Ciudad con mayor número de ventas cerradas
print("\n5. Ciudad con más ventas cerradas:")
print(cerradas["CIUDAD"].value_counts().head(1))

# 6. Valor total de ventas por ciudad
print("\n6. Valor total de ventas por ciudad:")
print(df.groupby("CIUDAD")["VALOR_VENTA"].sum().sort_values(ascending=False))

# 7. Top 5 productos más vendidos
print("\n7. Top 5 productos más vendidos:")
print(df["PRODUCTO"].value_counts().head(5))

# 8. Productos únicos
print("\n8. Productos únicos vendidos:", df["PRODUCTO"].nunique())

# 9. Vendedor con más ventas cerradas
print("\n9. Vendedor con más ventas cerradas:")
print(cerradas["VENDEDOR"].value_counts().head(1))

# 10. Venta con mayor valor
max_venta = df.loc[df["VALOR_VENTA"].idxmax()]
print("\n10. Venta de mayor valor:")
print(max_venta[["CLIENTE", "PRODUCTO", "VALOR_VENTA", "CIUDAD", "VENDEDOR"]])

# 11. Ventas con valor o comisión nula/negativa
invalidas = df[(df["VALOR_VENTA"] <= 0) | (df["COMISION"] <= 0)]
print("\n11. Ventas con valor/comisión nula o negativa:", len(invalidas))

# 12. Media de ventas por mes
print("\n12. Media de ventas por mes:")
print(df.groupby(df["FECHA"].dt.month)["VALOR_VENTA"].mean())

# 13. Mes con más ventas cerradas
print("\n13. Mes con más ventas cerradas:")
print(cerradas.groupby(cerradas["FECHA"].dt.month).size().idxmax())

# 14. Ventas por trimestre
print("\n14. Ventas por trimestre:")
print(df.groupby(df["FECHA"].dt.to_period("Q")).size())

# 15. Productos vendidos en más de 3 ciudades
prod_ciudades = df.groupby("PRODUCTO")["CIUDAD"].nunique()
print("\n15. Productos vendidos en más de 3 ciudades:")
print(prod_ciudades[prod_ciudades > 3])

# 16. Duplicados
print("\n16. Existen duplicados:", df.duplicated().sum())

# 17. Eliminar nulos en columnas clave
df_clean = df.dropna(subset=["CLIENTE", "PRODUCTO", "VALOR_VENTA"]).copy()
print("\n17. Registros después de limpiar nulos:", len(df_clean))

# 18. Nueva columna UTILIDAD y producto más rentable
df_clean.loc[:, "UTILIDAD"] = df_clean["VALOR_VENTA"] * 0.95
utilidad = df_clean.groupby("PRODUCTO")["UTILIDAD"].sum().sort_values(ascending=False)
print("\n18. Producto con mayor utilidad total:")
print(utilidad.head(1))

# ==============================
# Preguntas específicas con groupby
# ==============================

# Valor total de ventas por ciudad
print("\n[GroupBy] Valor total de ventas por ciudad:")
print(df.groupby("CIUDAD")["VALOR_VENTA"].sum().head())

# Promedio comisión por vendedor
print("\n[GroupBy] Promedio comisión por vendedor:")
print(df.groupby("VENDEDOR")["COMISION"].mean().head())

# Número de ventas por estado y ciudad
print("\n[GroupBy] Número de ventas por estado y ciudad:")
print(df.groupby(["ESTADO", "CIUDAD"]).size().head(10))

# Categoría de producto con mayor valor de ventas
print("\n[GroupBy] Categoría con mayor valor de ventas:")
print(df.groupby("CATEGORIA")["VALOR_VENTA"].sum().sort_values(ascending=False).head(1))

# Total de ventas mensuales por ciudad
print("\n[GroupBy] Total de ventas mensuales por ciudad:")
print(df.groupby([df["FECHA"].dt.to_period("M"), "CIUDAD"])["VALOR_VENTA"].sum().head(10))

# Ventas cerradas por vendedor y ciudad
print("\n[GroupBy] Ventas cerradas por vendedor y ciudad:")
print(cerradas.groupby(["VENDEDOR", "CIUDAD"]).size())

print("\n✅ Análisis completado.")
