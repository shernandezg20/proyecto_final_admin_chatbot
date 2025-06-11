import pandas as pd
from sqlalchemy import text
from backend.core.database import engine
from matplotlib import pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime

def guardar_productos_csv(csv_file):
    df = pd.read_csv(csv_file)
    df.fillna('', inplace=True)
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO productos (nombre, descripcion, categoria, precio_oficial, imagen_url)
                VALUES (:nombre, :descripcion, :categoria, :precio, :imagen_url)
            """), {
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "categoria": row["categoria"],
                "precio": row.get("precio_oficial", None),
                "imagen_url": row.get("imagen_url", None),
            })

def generar_pdf():
    df = pd.read_sql("""
        SELECT p.nombre, p.precio_oficial, pr.precio_predicho
        FROM productos p
        LEFT JOIN (
            SELECT DISTINCT ON (id_producto) * 
            FROM predicciones
            ORDER BY id_producto, fecha_prediccion DESC
        ) pr ON p.id_producto = pr.id_producto
        WHERE p.precio_oficial IS NOT NULL AND pr.precio_predicho IS NOT NULL
    """, engine)

    plt.figure(figsize=(8, 5))
    plt.scatter(df["precio_oficial"], df["precio_predicho"], c="blue")
    plt.xlabel("Precio oficial")
    plt.ylabel("Precio predicho")
    plt.title("Predicción vs Precio Oficial")
    plt.grid(True)
    plt.savefig("grafico.png")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Predicciones", ln=True, align='C')
    pdf.image("grafico.png", x=10, y=30, w=180)
    output_path = f"reporte_predicciones_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(output_path)
    os.remove("grafico.png")
    return output_path
