from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:S%40nt0%24kr0n0%24@localhost:5432/ecommerce_bot")
