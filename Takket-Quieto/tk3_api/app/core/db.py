from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion a base de datos (MariaDB)
# TODO: Mover a variables de entorno
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user2dam03:bG1cS6tW@82.223.102.153:3306/2DAM_alumno03"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
