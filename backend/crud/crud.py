from sqlalchemy.orm import Session
from models.models import Producto, Prediccion
import pandas as pd

def guardar_productos_desde_csv(db: Session, file):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        prod = Producto(
            nombre=row["nombre"],
            descripcion=row["descripcion"],
            imagen_url=row.get("imagen_url", ""),
            precio_real=row.get("precio_real")
        )
        db.add(prod)
    db.commit()

def obtener_predicciones(db: Session):
    subq = db.query(
        Prediccion.id_prediccion,
        Producto.nombre,
        Producto.precio_real,
        Prediccion.precio_predicho,
        Prediccion.estado
    ).join(Producto).filter(Prediccion.estado == "pendiente")
    return subq.all()

def actualizar_estado_prediccion(db: Session, id: int, estado: str):
    pred = db.query(Prediccion).filter(Prediccion.id_prediccion == id).first()
    if pred:
        pred.estado = estado
        if estado == "aceptado":
            producto = pred.producto
            producto.precio_real = pred.precio_predicho
        db.commit()
        return True
    return False
