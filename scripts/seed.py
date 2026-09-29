"""Datos de prueba de TaskFlow.

Uso, desde la raíz del proyecto:

    python -m scripts.seed

Crea los usuarios de prueba, o les restablece la contraseña si ya existen.
Se puede correr las veces que haga falta: el resultado siempre es el mismo.

OJO: estas credenciales son solo para desarrollo. Este script nunca se
ejecuta contra una base de datos de producción.

El dominio es example.com porque está reservado para documentación y pruebas.
Dominios como .test o .local los rechaza el validador de correos de Pydantic.
"""

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import Rol, User

USUARIOS = [
    {
        "name": "Admin",
        "last_name": "TaskFlow",
        "email": "admin@example.com",
        "password": "Admin12345",
        "rol": Rol.ADMIN,
    },
    {
        "name": "Manager",
        "last_name": "Uno",
        "email": "manager1@example.com",
        "password": "Manager12345",
        "rol": Rol.MANAGER,
    },
    {
        "name": "Manager",
        "last_name": "Dos",
        "email": "manager2@example.com",
        "password": "Manager12345",
        "rol": Rol.MANAGER,
    },
    {
        "name": "Dev",
        "last_name": "Uno",
        "email": "dev@example.com",
        "password": "Dev12345",
        "rol": Rol.DEVELOPER,
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        for datos in USUARIOS:
            usuario = db.query(User).filter(User.email == datos["email"]).first()

            if usuario is None:
                usuario = User(
                    name=datos["name"],
                    last_name=datos["last_name"],
                    email=datos["email"],
                    password=hash_password(datos["password"]),
                    rol=datos["rol"],
                )
                db.add(usuario)
                accion = "creado"
            else:
                usuario.password = hash_password(datos["password"])
                usuario.is_active = True
                accion = "actualizado"

            print(f"{accion:12} {datos['email']:24} {datos['password']}")

        db.commit()
        print("\nListo.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
