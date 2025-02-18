from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Importamos la Base desde models.py para que Alembic reconozca los modelos
from models import Base  

# Este es el objeto de configuración de Alembic, que proporciona acceso
# a los valores dentro del archivo .ini en uso.
config = context.config

# Interpreta el archivo de configuración para Python logging.
# Esta línea configura los registradores básicamente.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Se asigna target_metadata para el soporte de 'autogenerate'
# Antes estaba en None, ahora lo vinculamos a los modelos de SQLAlchemy
target_metadata = Base.metadata  

# Otras configuraciones de valores definidas por las necesidades de env.py
# pueden ser adquiridas:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'.

    Configura el contexto solo con una URL sin un Engine.
    Llamadas a context.execute() aquí emiten la consulta SQL.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'.

    En este caso, creamos un Engine y lo asociamos con el contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
