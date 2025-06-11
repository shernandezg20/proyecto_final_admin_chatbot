from fastapi import FastAPI
from core.database import Base, engine
from routers import productos, predicciones, precios

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir routers
app.include_router(productos.router)
app.include_router(predicciones.router)
app.include_router(precios.router)

# Opcional: ruta raíz
@app.get("/")
def root():
    return {"mensaje": "API Backend de Ecommerce Bot"}
