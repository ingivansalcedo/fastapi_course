from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy import inspect, text
from app.database import Base, engine
import app.models  # importa los modelos para que SQLAlchemy registre los modelos


def _get_existing_columns(table_name: str) -> set[str]:
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        return set()
    return {column["name"] for column in inspector.get_columns(table_name)}


def _compile_column_type(column) -> str:
    return column.type.compile(dialect=engine.dialect)


def _add_missing_columns(table_name: str, columns) -> None:
    existing_columns = _get_existing_columns(table_name)
    missing_columns = [col for col in columns if col.name not in existing_columns]
    if not missing_columns:
        return

    preparer = engine.dialect.identifier_preparer
    quoted_table = preparer.quote(table_name)

    with engine.begin() as conn:
        for column in missing_columns:
            column_type = _compile_column_type(column)
            quoted_column = preparer.quote(column.name)
            ddl = f"ALTER TABLE {quoted_table} ADD COLUMN {quoted_column} {column_type}"
            conn.execute(text(ddl))
            print(f"Columna agregada: {table_name}.{column.name}")


def create_or_update_tables() -> None:
    """Crea tablas nuevas y agrega columnas nuevas a tablas existentes."""
    Base.metadata.create_all(bind=engine)

    for table_name, table in Base.metadata.tables.items():
        if inspect(engine).has_table(table_name):
            _add_missing_columns(table_name, table.columns)


if __name__ == "__main__":
    create_or_update_tables()
    print("Tablas creadas/actualizadas correctamente")

