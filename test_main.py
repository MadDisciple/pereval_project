from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import PerevalAdded

test_data = {
    "beauty_title": "пер. Тестовый",
    "title": "Тест",
    "other_titles": "Test",
    "connect": "соединяет А и Б",
    "add_time": "2025-11-06T10:00:00",
    "user": {
        "email": "test.user@mail.ru",
        "fam": "Тестов",
        "name": "Тест",
        "otc": "Тестович",
        "phone": "+7 123 456 78 90"
    },
    "coords": {
        "latitude": 50.0,
        "longitude": 50.0,
        "height": 1000
    },
    "level": {
        "winter": "1A",
        "summer": "1A",
        "autumn": "1A",
        "spring": "1A"
    },
    "images": [
        {
            "data": "base64_string_1",
            "title": "Фото 1"
        }
    ]
}


def test_submit_data_success(client: TestClient):
    response_post = client.post("/submitData", json=test_data)

    assert response_post.status_code == 200
    data_post = response_post.json()
    assert data_post["status"] == 200
    assert data_post["message"] == "Отправлено успешно"
    assert data_post["id"] is not None

    new_id = data_post["id"]

    response_get = client.get(f"/submitData/{new_id}")

    assert response_get.status_code == 200
    data_get = response_get.json()

    assert data_get["id"] == new_id
    assert data_get["title"] == test_data["title"]
    assert data_get["status"] == "new"  # 🎯 Проверяем статус
    assert data_get["user"]["email"] == test_data["user"]["email"]
    assert data_get["coords"]["height"] == test_data["coords"]["height"]
    assert len(data_get["images"]) == 1
    assert data_get["images"][0]["title"] == "Фото 1"


def test_get_by_email(client: TestClient):
    response = client.get(f"/submitData/?user__email={test_data['user']['email']}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["user"]["email"] == test_data["user"]["email"]


def test_patch_data_success(client: TestClient, db_session: Session):
    pereval = db_session.query(PerevalAdded).filter(PerevalAdded.user.has(email=test_data['user']['email'])).first()
    assert pereval is not None
    pass_id = pereval.id

    patch_json = {
        "title": "НОВОЕ НАЗВАНИЕ",
        "level": {"summer": "2B"}
    }

    response_patch = client.patch(f"/submitData/{pass_id}", json=patch_json)

    assert response_patch.status_code == 200
    data_patch = response_patch.json()
    assert data_patch["state"] == 1

    response_get = client.get(f"/submitData/{pass_id}")
    data_get = response_get.json()

    assert data_get["title"] == "НОВОЕ НАЗВАНИЕ"
    assert data_get["level_summer"] == "2B"


def test_patch_data_fail_not_new(client: TestClient, db_session: Session):
    pereval = db_session.query(PerevalAdded).filter(PerevalAdded.user.has(email=test_data['user']['email'])).first()
    assert pereval is not None
    pass_id = pereval.id

    pereval.status = "pending"
    db_session.commit()

    patch_json = {"title": "ПОПЫТКА 2"}

    response_patch = client.patch(f"/submitData/{pass_id}", json=patch_json)

    assert response_patch.status_code == 403
    data_patch = response_patch.json()
    assert data_patch["state"] == 0
    assert "Нельзя редактировать" in data_patch["message"]