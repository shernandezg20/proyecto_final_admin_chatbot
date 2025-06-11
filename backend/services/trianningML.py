import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
import os
from datetime import datetime
# from backecore.database import engine


# load_dotenv(".env")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:S%40nt0%24kr0n0%24@localhost:5432/ecommerce_bot")
# os.getenv("DATABASE_URL", "postgresql://postgres:S%40nt0%24kr0n0%24@localhost:5432/ecommerce_bot")
engine = create_engine(DATABASE_URL)

def cargar_datos():
    query = text("""
        SELECT id_producto, nombre, descripcion, categoria, precio_real
        FROM productos
        WHERE precio_real IS NOT NULL
    """)
    
    with engine.connect() as conn:
        print("Conectando a la base de datos...")
        df = pd.read_sql(query, conn)
        print(f"Datos cargados: {len(df)} registros")
    return df

def preprocesar(df):
    df = df.copy()

    df["texto"] = df["nombre"].fillna('') + ' ' + df["descripcion"].fillna('')

    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=200)
    X_text = vectorizer.fit_transform(df["texto"])

    encoder = LabelEncoder()
    df["categoria_encoded"] = encoder.fit_transform(df["categoria"].fillna("SinCategoria"))

    from scipy.sparse import hstack
    X = hstack([X_text, df[["categoria_encoded"]]])

    y = df["precio_real"]

    return X, y, df["id_producto"]

def entrenar_y_predecir(X, y):
    model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X, y)
    predicciones = model.predict(X)
    return predicciones, model

def guardar_predicciones(id_productos, precios):
    now = datetime.now()
    with  engine.connect() as conn:
        for id_prod, precio in zip(id_productos, precios):
            query = text("""
                INSERT INTO predicciones (id_producto, precio_predicho, fecha_prediccion)
                VALUES (:id_producto, :precio_predicho, :fecha_prediccion)
            """)
            conn.execute(query, {
                "id_producto": int(id_prod),
                "precio_predicho": round(float(precio),2),
                "fecha_prediccion": now
            })

def ejecutar_entrenamiento():
    print("Cargando datos...")
    df = cargar_datos()

    print("Preprocesando datos...")
    X, y, ids = preprocesar(df)

    print("Entrenando modelo...")
    precios_predichos, model = entrenar_y_predecir(X, y)

    print("Guardando en base de datos...")
    guardar_predicciones(ids, precios_predichos)

    print("Proceso completado")

if __name__ == "__main__":
    ejecutar_entrenamiento()