from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table, MetaData, func, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

metadata = MetaData()

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    imagen_url = Column(String)
    precio_real = Column(Float, nullable=True)

    predicciones = relationship("Prediccion", back_populates="producto")

class Prediccion(Base):
    __tablename__ = "predicciones"
    id_prediccion = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"))
    precio_predicho = Column(Float)
    fecha_prediccion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")  # pendiente, aceptado, rechazado

    producto = relationship("Producto", back_populates="predicciones")

precios_definidos = Table(
    "precios_definidos",
    metadata,
    Column("id_precio", Integer, primary_key=True),
    Column("id_producto", Integer, nullable=False),
    Column("id_prediccion", Integer, nullable=False),
    Column("id_usuario", Integer, nullable=False),
    Column("precio_final", Float, nullable=False),
    Column("fecha_establecido", DateTime, server_default=func.now()),
)

auditoria = Table(
    "auditoria",
    metadata,
    Column("id_auditoria", Integer, primary_key=True),
    Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario")),
    Column("tabla_afectada", String(100)),
    Column("operacion", String(10)),
    Column("fecha", DateTime, server_default=func.now()),
    Column("descripcion", Text)
)
