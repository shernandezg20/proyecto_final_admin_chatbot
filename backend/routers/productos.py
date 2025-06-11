from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db

router = APIRouter(prefix="/productos", tags=["Productos"])

class ProductoRespuesta(BaseModel):
    nombre: str
    descripcion: str
    imagen_url: str
    # precio_predicho: float
    precio_real: float

@router.get("/buscar", response_model=List[ProductoRespuesta])
def buscar_producto(q: str = Query(..., description="Texto enviado por el usuario"), db: Session = Depends(get_db)):
    query = text("""
        SELECT p.nombre, p.descripcion, p.imagen_url, p.precio_real
        FROM productos p
        LEFT JOIN (
            SELECT DISTINCT ON (id_producto) id_producto, precio_predicho
            FROM predicciones
            ORDER BY id_producto, fecha_prediccion DESC
        ) pr ON p.id_producto = pr.id_producto
        WHERE LOWER(p.nombre) LIKE LOWER(:query) OR LOWER(p.descripcion) LIKE LOWER(:query)
        LIMIT 5
    """)
    try:
        result = db.execute(query, {"query": f"%{q}%"}).fetchall()
        if not result:
            # raise HTTPException(status_code=404, detail="No se encontraron productos relacionados")
            return []
        
        productos = [
            ProductoRespuesta(
                nombre=row[0],
                descripcion=row[1],
                imagen_url=row[2],
                # precio_predicho=row[3] if row[3] else 0.0,
                precio_real=row[3] if row[3] else 0.0
            ) for row in result
        ]
        return productos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
