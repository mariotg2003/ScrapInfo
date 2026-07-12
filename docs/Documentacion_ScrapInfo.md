# Documentacion del Proyecto ScrapInfo

## 1. Resumen
ScrapInfo es un proyecto de scraping y exposicion de datos compuesto por dos partes:

- Un proceso batch que extrae productos desde PCComponentes, limpia la tabla destino e inserta los resultados en la base de datos.
- Una API construida con FastAPI para consultar los productos almacenados (todos o filtrados por tipo).

El flujo principal permite automatizar una ejecucion diaria y notificar por correo el resultado de la ejecucion.

## 2. Objetivo
Centralizar ofertas de distintas categorias de hardware/perifericos en una sola fuente de datos para:

- Persistir informacion historica en base de datos.
- Exponer datos mediante endpoints simples.
- Integrar el resultado en otros sistemas (dashboards, bots, alertas, etc.).

## 3. Arquitectura General

### 3.1 Componentes
- `main.py`: orquestador principal del scraping e insercion.
- `functions/`: modulo de funciones auxiliares para acceso a BD, parseo, lectura de parametros y envio de correo.
- `data/pcComponentesData.json`: configuracion de URLs y selectores CSS usados por el parser.
- `data/month.json`: mapeo de numero de mes a nombre en espanol para correos.
- `api/main.py`: API REST con FastAPI y cliente Supabase.
- `execution_local/main.ipynb`: notebook de ejecucion y pruebas locales.

### 3.2 Flujo de datos
1. Se crea el engine SQLAlchemy y se define la tabla `Object`.
2. Se elimina la data previa de la tabla.
3. Se leen parametros de scraping desde `data/pcComponentesData.json`.
4. Por cada categoria se descarga HTML usando Scrape.do (`SCRAPE_TOKEN`).
5. Se parsean productos (nombre, enlace, precio, imagen, precio anterior).
6. Se insertan registros en la base de datos.
7. Se envia correo indicando ejecucion Exitosa o Fallida.
8. La API consulta la tabla `Object` y devuelve resultados JSON.

## 4. Estructura del Proyecto

```text
ScrapInfo/
|-- main.py
|-- requirements.txt
|-- api/
|   `-- main.py
|-- data/
|   |-- month.json
|   `-- pcComponentesData.json
|-- execution_local/
|   `-- main.ipynb
`-- functions/
    |-- create_engine.py
    |-- create_json.py
    |-- delete_data.py
    |-- format_data.py
    |-- get_url.py
    |-- insert_data.py
    |-- read_params.py
    `-- send_email.py
```

## 5. Requisitos

### 5.1 Tecnologias principales
- Python 3.11+ recomendado.
- FastAPI + Uvicorn.
- SQLAlchemy.
- BeautifulSoup4.
- requests.
- yagmail.
- python-dotenv.
- supabase.

### 5.2 Dependencias
Instalar desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 6. Variables de Entorno
Crear un archivo `.env` en la raiz del proyecto con las variables necesarias.

### 6.1 Para scraping y carga a BD
- `DATABASE_URL`: cadena de conexion a la base de datos.
- `SCRAPE_TOKEN`: token de acceso a la API de Scrape.do.
- `GMAIL`: correo emisor para notificaciones.
- `PASSWORD`: password o app password del correo emisor.

### 6.2 Para API
- `SUPABASE_URL`: URL del proyecto Supabase.
- `SUPABASE_KEY`: clave de acceso para consultas.
- `ALLOWED_ORIGINS`: lista separada por comas (actualmente no aplicada en tiempo de ejecucion, ver notas).

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
SCRAPE_TOKEN=tu_token_scrape_do
GMAIL=tu_correo@gmail.com
PASSWORD=tu_app_password
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJ...
ALLOWED_ORIGINS=http://localhost:3000,https://tu-frontend.com
```

## 7. Configuracion y Ejecucion

### 7.1 Ejecutar scraping batch
Desde la raiz del proyecto:

```bash
python main.py
```

Resultado esperado:
- Limpieza de tabla `Object`.
- Insercion de productos de todas las categorias definidas.
- Envio de correo de estado.

### 7.2 Levantar API local
Desde la raiz del proyecto:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## 8. API REST

Base URL local: `http://localhost:8000`

### 8.1 Health / bienvenida
- Metodo: `GET`
- Ruta: `/`
- Respuesta:

```json
{
  "message": "Welcome to ScrapInfo API"
}
```

### 8.2 Obtener todos los objetos
- Metodo: `GET`
- Ruta: `/select`
- Respuesta:

```json
{
  "data": [
    {
      "id": 1,
      "product_name": "...",
      "product_link": "...",
      "product_price": "...",
      "product_type": "ram",
      "product_img": "...",
      "product_old_price": "..."
    }
  ]
}
```

### 8.3 Obtener objetos por tipo
- Metodo: `GET`
- Ruta: `/select/{type}`
- Ejemplo: `/select/monitores`

## 9. Detalle de Modulos

### 9.1 `functions/create_engine.py`
- Crea el engine SQLAlchemy con `DATABASE_URL`.
- Define la tabla `Object` (id, timestamps y campos de producto).

### 9.2 `functions/get_url.py`
- Llama a Scrape.do para obtener HTML renderizado.
- Devuelve `BeautifulSoup` o `None` si falla.

### 9.3 `functions/format_data.py`
- Aplica selectores CSS configurables.
- Extrae campos clave del producto y arma lista de diccionarios.

### 9.4 `functions/insert_data.py`
- Limpia encoding de campos de texto.
- Inserta registros en la tabla.

### 9.5 `functions/delete_data.py`
- Elimina todos los registros de la tabla antes de una nueva carga.

### 9.6 `functions/send_email.py`
- Envia notificacion por Gmail con estado de ejecucion.

### 9.7 `functions/read_params.py`
- Carga archivos JSON de configuracion (`data/`).

## 10. Parametrizacion de Categorias y Selectores
El archivo `data/pcComponentesData.json` controla:

- Categorias a scrapear (`paginas`) y sus URLs.
- Selectores CSS (`clases_objetos`) del layout objetivo.

Si PCComponentes cambia su HTML/CSS, normalmente solo necesitas actualizar este archivo.

## 11. Manejo de Errores y Riesgos
- Si `SCRAPE_TOKEN` no existe, la descarga retorna `None`.
- Si cambian clases CSS del sitio objetivo, el parser puede dejar de extraer datos.
- El proceso actual borra toda la tabla antes de recargar.
- El flag `execution` refleja estado de insercion, pero no discrimina exitos parciales.

## 12. Mejoras Recomendadas
- Aplicar validacion de `None` en todas las cadenas `.find()` del parser.
- Registrar logs estructurados por categoria y cantidad de inserciones.
- Cambiar borrado total por estrategia incremental (upsert/delta).
- Aplicar `allowed_origins` en el middleware CORS en lugar de `"*"`.
- Añadir autenticacion por API key para endpoints publicos.
- Agregar pruebas unitarias del parser y pruebas de integracion de API.

## 13. Troubleshooting Rapido

### 13.1 Error de conexion a BD
- Revisar `DATABASE_URL`.
- Verificar conectividad/red hacia el host de base de datos.

### 13.2 API Scrape.do devuelve error
- Confirmar `SCRAPE_TOKEN`.
- Revisar limites/cuota del proveedor.

### 13.3 No llega correo
- Verificar `GMAIL` y `PASSWORD`.
- Usar app password si tu cuenta lo requiere.

### 13.4 API no responde
- Validar variables `SUPABASE_URL` y `SUPABASE_KEY`.
- Confirmar que la tabla `Object` existe en el proyecto de Supabase.

## 14. Comandos Utiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar scraping
python main.py

# Levantar API
uvicorn api.main:app --reload
```

## 15. Licencia y Uso
Uso interno/educativo (ajustar segun tus necesidades de distribucion). Se recomienda definir una licencia explicita si se publicara el repositorio.
