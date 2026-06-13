import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db.deps import get_db
from app.core.config import settings
from main import app

# URL de la DB de prueba, remplazamos el nombre de la DB por la de prueba
TEST_DATABASE_URL = settings.database_url.replace("taskflow", "taskflow_test")

# aqui creamos el motor para la conexion, no usamos pool_recicly porque los test son segundo no es necesario y sin debug porque queremos ver los ouputs limpios 
test_engine = create_engine(TEST_DATABASE_URL)

# Fabrica de sessiones de prueba
TestingSessionLocal = sessionmaker(autoflush= False, autocommit= False, bind=test_engine)

# lo que hace este fixture explicitamente es crear las tablas en la base de datos de test las mantiene y despues las elimina completando el proceso
@pytest.fixture(scope="session", autouse=True) 
def setup_database():
    Base.metadata.create_all(bind=test_engine) #aqui creamos todas las tablas
    yield # aqui hay una espera a que corran todos los test
    Base.metadata.drop_all(bind=test_engine) # aqui se eliminan todas las tablas 

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    
@pytest.fixture
def test_user(db):
    from app.models.user import User, Rol
    from app.core.security import hash_password
    
    
    user = User(
        name = "Test",
        last_name = "User",
        email = "test@gmail.com",
        password = hash_password("123456789"),
        rol = Rol.ADMIN
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user