import argparse
from pathlib import Path

from alembic import command
from alembic.config import Config


def _get_alembic_config() -> Config:
    project_root = Path(__file__).resolve().parents[1]
    return Config(str(project_root / "alembic.ini"))


def db_upgrade() -> None:
    command.upgrade(_get_alembic_config(), "head")


def db_downgrade() -> None:
    parser = argparse.ArgumentParser(
        prog="db-downgrade",
        description="Ejecuta un downgrade de Alembic usando la configuracion raiz del proyecto.",
    )
    parser.add_argument(
        "revision",
        nargs="?",
        default="-1",
        help="Revision destino. Por defecto hace downgrade de un paso (-1).",
    )
    args = parser.parse_args()
    command.downgrade(_get_alembic_config(), args.revision)


def db_revision() -> None:
    parser = argparse.ArgumentParser(
        prog="db-revision",
        description="Crea una revision de Alembic usando la configuracion raiz del proyecto.",
    )
    parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Mensaje descriptivo de la migracion.",
    )
    parser.add_argument(
        "--autogenerate",
        action="store_true",
        help="Genera la revision comparando modelos y base de datos.",
    )
    parser.add_argument(
        "--rev-id",
        dest="rev_id",
        help="Id manual para la revision.",
    )
    parser.add_argument(
        "--head",
        default="head",
        help="Revision head sobre la que se crea la nueva migracion.",
    )
    parser.add_argument(
        "--splice",
        action="store_true",
        help="Permite crear la revision fuera de la rama head actual.",
    )
    parser.add_argument(
        "--branch-label",
        dest="branch_label",
        help="Etiqueta de rama para la revision.",
    )
    args = parser.parse_args()
    command.revision(
        _get_alembic_config(),
        message=args.message,
        autogenerate=args.autogenerate,
        rev_id=args.rev_id,
        head=args.head,
        splice=args.splice,
        branch_label=args.branch_label,
    )


def db_current() -> None:
    parser = argparse.ArgumentParser(
        prog="db-current",
        description="Muestra la revision actual de Alembic usando la configuracion raiz del proyecto.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Muestra informacion detallada de la revision actual.",
    )
    args = parser.parse_args()
    command.current(_get_alembic_config(), verbose=args.verbose)


def db_history() -> None:
    parser = argparse.ArgumentParser(
        prog="db-history",
        description="Muestra el historial de revisiones de Alembic usando la configuracion raiz del proyecto.",
    )
    parser.add_argument(
        "range",
        nargs="?",
        help="Rango opcional de revisiones, por ejemplo base:head o -3:current.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Muestra informacion detallada de cada revision.",
    )
    args = parser.parse_args()
    command.history(_get_alembic_config(), rev_range=args.range, verbose=args.verbose)


def db_stamp() -> None:
    parser = argparse.ArgumentParser(
        prog="db-stamp",
        description="Marca la base de datos en una revision sin ejecutar migraciones.",
    )
    parser.add_argument(
        "revision",
        help="Revision que se quiere marcar, por ejemplo head o base.",
    )
    parser.add_argument(
        "--purge",
        action="store_true",
        help="Limpia la tabla de version antes de marcar la revision.",
    )
    args = parser.parse_args()
    command.stamp(_get_alembic_config(), args.revision, purge=args.purge)
