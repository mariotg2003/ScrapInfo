import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Path, status
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

#  Funcion para obtener variables de entorno requeridas
def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value.strip()

#  Funcion para parsear los allowed origins desde la variable de entorno
def parse_allowed_origins() -> list[str]:
    raw_origins = os.getenv("ALLOWED_ORIGINS", "")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


#  Inicializar Supabase client
supabase_url = get_required_env("SUPABASE_URL")
supabase_key = get_required_env("SUPABASE_KEY")
allowed_origins = parse_allowed_origins()

supabase: Client = create_client(supabase_url, supabase_key)

#  Funcion para los selects de la base de datos
def fetch_objects(product_type: str | None = None) -> list[dict]:
    try:
        query = supabase.table("Object").select("*")
        if product_type is not None:
            query = query.eq("product_type", product_type)
        response = query.execute()
        return response.data
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Database query failed",
        ) from exc

#  Inicializar FastAPI app
app = FastAPI()

# Agregar middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)

#  Ruta principal
@app.get("/")
async def root():
    return {"message": "Welcome to ScrapInfo API"}

# Ruta para obtener todos los objetos
@app.get("/select")
async def select_all():
    return {"data": fetch_objects()}

#  Ruta para obtener objetos filtrados por tipo
@app.get("/select/{type}")
async def select_type(
    type: Annotated[str, Path(min_length=1, max_length=100)],):
    return {"data": fetch_objects(type)}