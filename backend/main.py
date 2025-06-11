from fastapi import FastAPI
from core.database import Base, engine
from routers import productos, predicciones, precios
from fastapi.middleware.cors import CORSMiddleware

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(productos.router)
app.include_router(predicciones.router)
app.include_router(precios.router)

# Opcional: ruta raíz
@app.get("/")
def root():
    return {"mensaje": "API Backend de Ecommerce Bot"}
