from app.db.session import SessionLocal

def get_db():
    db = SessionLocal() # abre la session
    try:
        # entrega la session al endpoint
        # PAUSA — el endpoint hace su trabajo
        yield db
        
    finally:
        db.close() # cuando el endpoint termina, cierra la session