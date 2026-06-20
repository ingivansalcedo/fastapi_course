# Ecommerce FastAPI

Proyecto API con FastAPI, SQLAlchemy y Alembic, gestionado con `uv`.

## Requisitos

- Python 3.13+
- PostgreSQL en ejecucion
- Archivo `.env` en la raiz del proyecto

## Configuracion inicial

Desde la raiz del proyecto (`C:\Cursos\ecommerce_fastapi`):

```powershell
.venv\Scripts\Activate.ps1
uv sync
```

Clonacion en otro equipo:

```powershell
git clone <URL_DEL_REPOSITORIO>
cd ecommerce_fastapi
uv sync
```

Configuracion de variables de entorno:

```powershell
Copy-Item .env.example .env
```

Luego edita `.env` con tus valores locales (no se versiona en Git).

## Ejecutar API

```powershell
.venv\Scripts\Activate.ps1
uv run uvicorn app.main:app --reload
```

## Flujo de migraciones Alembic

Importante:

- Ejecutar comandos desde la raiz del proyecto.
- Usar el archivo `alembic.ini` de la raiz.
- Evitar ejecutar migraciones con `app/alembic.ini`.

### Subir migraciones

```powershell
uv run db-upgrade
```

### Crear una nueva migracion

```powershell
uv run db-revision -m "descripcion_cambio" --autogenerate
```

### Cuando agregues un modelo nuevo

Para que Alembic lo detecte con `--autogenerate`, sigue este orden:

1. Crear la clase del modelo en `app/models/` usando `Base` de `app.db.database`.
2. Importar ese modelo en `app/models/__init__.py`.
3. Generar la migracion:

```powershell
uv run db-revision -m "crear nueva tabla" --autogenerate
```

4. Revisar el archivo generado en `app/alembic/versions/`.
5. Aplicar la migracion:

```powershell
uv run db-upgrade
```

Si el modelo no se importa en `app/models/__init__.py`, Alembic no lo incluira en `Base.metadata` y no aparecera en la migracion autogenerada.

### Bajar una migracion

```powershell
uv run db-downgrade
```

Opciones comunes:

```powershell
uv run db-downgrade -1
uv run db-downgrade base
```

### Ver estado actual de migracion

```powershell
uv run db-current
uv run db-current --verbose
```

### Ver historial de migraciones

```powershell
uv run db-history
uv run db-history base:head --verbose
```

### Marcar revision sin ejecutar migraciones

```powershell
uv run db-stamp head
uv run db-stamp base --purge
```

## Comandos adicionales recomendados

Estos comandos no son obligatorios para correr la API, pero conviene documentarlos porque forman parte del flujo real del proyecto:

### Calidad de codigo (Ruff / pre-commit)

```powershell
uv run ruff check .
uv run ruff check . --fix
uv run pre-commit run --all-files
```

### Utilidad de inicializacion manual de tablas

Existe una utilidad en `app/db/init_db.py`:

```powershell
uv run python -m app.db.init_db
```

Recomendacion:

- En entornos reales, preferir Alembic para cambios de esquema.
- Dejar `init_db` para escenarios de bootstrap local o mantenimiento puntual.

## Politica de archivos para GitHub

Este repositorio ya esta preparado para evitar subir archivos sensibles o locales:

- Se ignoran credenciales y archivos de entorno (`.env`, `.env.*`).
- Se versiona `.env.example` para facilitar la configuracion en otros equipos.
- Se ignoran carpetas de entorno virtual, caches y artefactos de build.

Antes de hacer push, valida:

```powershell
git status
```

Si ves un archivo sensible en staged o modified, quitalo antes del commit.

## Checklist pre-push (seguridad y calidad)

Usa este checklist antes de ejecutar `git push`:

1. Verificar estado general.

```powershell
git status
```

2. Confirmar que no hay secretos en archivos versionados (`.env`, tokens, passwords).

```powershell
git grep -nE "(SECRET_KEY|DB_PASSWORD|API_KEY|TOKEN|postgresql\+psycopg2://)"
```

3. Confirmar reglas de `.gitignore` para archivos sensibles/locales.

```powershell
git check-ignore -v .env .env.example .venv\Scripts\python.exe
```

4. Ejecutar validaciones rapidas de calidad.

```powershell
uv run ruff check .
uv run pre-commit run --all-files
```

5. Validar migraciones segun el cambio realizado.

```powershell
uv run db-current
uv run db-history
```

6. Revisar lo que realmente se va a commitear.

```powershell
git diff --staged
```

7. Commit con mensaje claro y push.

```powershell
git add .
git commit -m "mensaje claro del cambio"
git push
```

Atajo automatizado (ejecuta este mismo checklist):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\prepush-check.ps1
```

Opciones utiles:

```powershell
# Omite validaciones de calidad
powershell -ExecutionPolicy Bypass -File .\scripts\prepush-check.ps1 -SkipQuality

# Omite validaciones de migraciones
powershell -ExecutionPolicy Bypass -File .\scripts\prepush-check.ps1 -SkipMigrations
```

Si detectas un secreto en archivos ya commiteados:

1. Rota la credencial inmediatamente.
2. Elimina o reemplaza el secreto en el codigo.
3. Si ya se publico en remoto, limpia historial con `git filter-repo` o BFG.

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'app'`

Causa frecuente:

- Ejecutar Alembic desde una carpeta distinta o con configuracion no alineada al proyecto.

Solucion:

```powershell
Set-Location C:\Cursos\ecommerce_fastapi
uv run db-upgrade
```

### Error: Alembic no detecta `.env` o toma valores incorrectos

Causa frecuente:

- `.env` ausente en la raiz.
- Variables con nombres distintos a los esperados en `Settings`.

Solucion:

- Verifica que exista `C:\Cursos\ecommerce_fastapi\.env`.
- Revisa claves usadas por la app: `db_user`, `db_password`, `db_host`, `db_port`, `db_name`.

### Error: comando `alembic` no reconocido en PowerShell

Causa frecuente:

- El ejecutable no esta en `PATH` para esa sesion.

Solucion recomendada:

- Usa siempre wrappers con `uv run`:

```powershell
uv run db-upgrade
uv run db-history
uv run db-current
```

### Error: Uvicorn levanta, pero Alembic falla

Causa frecuente:

- Uvicorn y Alembic se ejecutan con distintos contextos de directorio/configuracion.

Solucion:

- Ejecuta ambos comandos desde la raiz.
- Para API usa: `uv run uvicorn app.main:app --reload`.
- Para migraciones usa los comandos `db-*` documentados en este README.
