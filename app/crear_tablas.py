from app.database import Base, engine
import app.models  # importa los modelos para que SQLAlchemy los registre


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Tablas creadas correctamente")

