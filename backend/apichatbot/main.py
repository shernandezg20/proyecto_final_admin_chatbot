from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
import crud.crud as crud
import models.models as models
from models.models import precios_definidos, auditoria
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import insert, create_engine, text
from dotenv import load_dotenv
from typing import List
import os

load_dotenv(dotenv_path=".env")

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS para que Angular pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cambia por seguridad si usas un dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EstadoInput(BaseModel):
    id: int

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    crud.guardar_productos_desde_csv(db, file)
    return {"message": "Productos guardados"}

@app.get("/predicciones")
def get_predicciones(db: Session = Depends(get_db)):
    predicciones = crud.obtener_predicciones(db)
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio_predicho": p.precio_predicho,
            "precio_real": p.precio_real,
            "estado": p.estado
        } for p in predicciones
    ]

@app.post("/aceptar-prediccion")
def aceptar_prediccion(data: EstadoInput, db: Session = Depends(get_db)):
    success = crud.actualizar_estado_prediccion(db, data.id, "aceptado")
    return {"success": success}

@app.post("/rechazar-prediccion")
def rechazar_prediccion(data: EstadoInput, db: Session = Depends(get_db)):
    success = crud.actualizar_estado_prediccion(db, data.id, "rechazado")
    return {"success": success}

# Guardar decisiones de precios
class PrecioFinalRequest(BaseModel):
    id_producto: int
    id_prediccion: int
    id_usuario: int
    precio_final: float

@app.post("/guardar-precio-final")
def guardar_precio_final(data: PrecioFinalRequest):
    try:
        with engine.connect() as conn:
            stmt = insert(precios_definidos).values(
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
        print("Error al guardar el precio final:", e)
        raise HTTPException(status_code=500, detail="Error al guardar el precio final")

def registrar_auditoria(id_usuario: int, tabla: str, operacion: str, descripcion: str):
    try:
        with engine.connect() as conn:
            stmt = insert(auditoria).values(
                id_usuario=id_usuario,
                tabla_afectada=tabla,
                operacion=operacion,
                descripcion=descripcion
            )
            conn.execute(stmt)
            conn.commit()
    except Exception as e:
        print("Error registrando auditoría:", e)

# CONFIGURACION DE LA BASE DE DATOS 
# DATABASE_URL = os.getenv("DATABASE_URL")
# print(f"Conectando a la base de datos en:*********************************** {DATABASE_URL}")
# engine = create_engine(DATABASE_URL)

# CONFIGURACION DE LA BASE DE DATOS 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:S%40nt0%24kr0n0%24@localhost:5432/ecommerce_bot")
engine = create_engine(DATABASE_URL)

# Modelo de respuesta para nuestro chatbot
class ProductoRespuesta(BaseModel):
    nombre: str
    descripcion: str
    imagen_url: str
    precio_predicho: float
    precio_real: float

@app.get("/busqueda-producto", response_model=List[ProductoRespuesta])
def buscar_producto(q: str = Query(..., description="Texto enviado por el usuario")):
    query = text("""
        SELECT p.nombre, p.descripcion, p.imagen_url, pr.precio_predicho, p.precio_real
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
        with engine.connect() as conn:
            result = conn.execute(query, {"query": f"%{q}%"}).fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron productos relacionados a la búsqueda")
            productos = [
                ProductoRespuesta(
                    nombre=row[0],
                    descripcion=row[1],
                    imagen_url=row[2],
                    precio_predicho=row[3] if row[3] else 0.0,
                    precio_real=row[4] if row[4] else 0.0
                ) for row in result
            ]
            return productos
    except Exception as e:
        print(f"Error al ejecutar la consulta:", e)
        return []
