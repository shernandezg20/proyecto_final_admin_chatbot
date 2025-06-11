from fastapi import FastAPI, APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crud import crud
from core.database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/predicciones", tags=["Predicciones"])

class EstadoInput(BaseModel):
    id: int

@router.get("/", summary="Obtener predicciones pendientes")
def get_predicciones(db: Session = Depends(get_db)):
    preds = crud.obtener_predicciones(db)
    return [{
        "id_prediccion": p.id_prediccion,
        "nombre": p.nombre,
        "precio_predicho": p.precio_predicho,
        "precio_real": p.precio_real,
        "estado": p.estado
    } for p in preds]

@router.post("/aceptar")
def aceptar_prediccion(data: EstadoInput, db: Session = Depends(get_db)):
    success = crud.actualizar_estado_prediccion(db, data.id, "aceptado")
    return {"success": success}

@router.post("/rechazar")
def rechazar_prediccion(data: EstadoInput, db: Session = Depends(get_db)):
    success = crud.actualizar_estado_prediccion(db, data.id, "rechazado")
    return {"success": success}

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    crud.guardar_productos_desde_csv(db, file)
    return {"message": "Productos guardados"}
