from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert
from core.database import engine
from apichatbot.main import registrar_auditoria

router = APIRouter(prefix="/precios", tags=["Precios"])

class PrecioFinalRequest(BaseModel):
    id_producto: int
    id_prediccion: int
    id_usuario: int
    precio_final: float

@router.post("/guardar")
def guardar_precio_final(data: PrecioFinalRequest):
    try:
        with engine.connect() as conn:
            stmt = insert("precios_definidos").values(
                id_producto=data.id_producto,
                id_prediccion=data.id_prediccion,
                id_usuario=data.id_usuario,
                precio_final=data.precio_final
            )
            conn.execute(stmt)
            conn.commit()

        registrar_auditoria(
            id_usuario=data.id_usuario,
            tabla="precios_definidos",
            operacion="INSERT",
            descripcion=f"Definió precio final {data.precio_final} para producto {data.id_producto}"
        )
        return {"mensaje": "Precio final guardado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
