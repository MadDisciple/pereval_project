import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from main import app
from database import get_db, Base
import os

postgres_container = PostgresContainer("postgres:15-alpine")

postgres_container.get_container_host_ip = lambda: "localhost"


@pytest.fixture(scope="session", autouse=True)
def start_db_container():
    with postgres_container as postgres:


        host = postgres.get_container_host_ip()
        port = postgres.get_exposed_port("5432")
        login = postgres.POSTGRES_USER
        password = postgres.POSTGRES_PASSWORD
        dbname = postgres.POSTGRES_DB

        os.environ["FSTR_DB_HOST"] = host
        os.environ["FSTR_DB_PORT"] = str(port)
        os.environ["FSTR_DB_LOGIN"] = login
        os.environ["FSTR_DB_PASS"] = password
        os.environ["FSTR_DB_NAME"] = dbname
        db_url = f"postgresql+psycopg2://{login}:{password}@{host}:{port}/{dbname}"

        yield db_url


@pytest.fixture(scope="session")
def TestSessionLocal(start_db_container):
    engine = create_engine(start_db_container)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session(TestSessionLocal):
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()