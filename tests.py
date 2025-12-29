import os
import re
import time
import random
import requests


BASE_URL = os.getenv("BASE_URL", "https://qa-internship.avito.com").rstrip("/")
TIMEOUT_S = 15

SELLER_ID = int(os.getenv("SELLER_ID", "123654"))

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)


def build_payload_ok() -> dict:
    return {
        "sellerID": SELLER_ID,
        "name": f"Egor-{int(time.time() * 1000)}",
        "price": random.randint(1, 10_000),
        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(0, 10_000),
            "contacts": random.randint(0, 500),
        }
    }


def extract_item_id_from_status(resp_json: dict) -> str:
    status_text = resp_json.get("status", "")
    m = UUID_RE.search(status_text)
    if not m:
        return ""
    return m.group(0)


# 1) Создать объявление
def test_1_create_item():
    url = f"{BASE_URL}/api/1/item"
    payload = build_payload_ok()

    resp = requests.post(url, json=payload, timeout=TIMEOUT_S)
    assert resp.status_code == 200

    data = resp.json()
    assert "status" in data

    item_id = extract_item_id_from_status(data)
    assert item_id != ""


# 2) Получить объявление по id
def test_2_get_item_by_id():
    create_url = f"{BASE_URL}/api/1/item"
    payload = build_payload_ok()
    create_resp = requests.post(create_url, json=payload, timeout=TIMEOUT_S)
    assert create_resp.status_code == 200

    item_id = extract_item_id_from_status(create_resp.json())
    assert item_id != ""

    # потом получаем по id
    get_url = f"{BASE_URL}/api/1/item/{item_id}"
    get_resp = requests.get(get_url, timeout=TIMEOUT_S)
    assert get_resp.status_code == 200

    data = get_resp.json()
    assert isinstance(data, dict)
    assert data != {}


# 3) Получить все объявления по sellerID
def test_3_get_all_items_by_seller():
    # создаём одно объявление, чтобы список точно был не пуст
    create_url = f"{BASE_URL}/api/1/item"
    payload = build_payload_ok()
    create_resp = requests.post(create_url, json=payload, timeout=TIMEOUT_S)
    assert create_resp.status_code == 200

    # получаем список
    list_url = f"{BASE_URL}/api/1/{SELLER_ID}/item"
    list_resp = requests.get(list_url, timeout=TIMEOUT_S)
    assert list_resp.status_code == 200

    data = list_resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


# 4) Получить статистику по item_id
def test_4_get_statistics_by_item_id():
    # создаём объявление
    create_url = f"{BASE_URL}/api/1/item"
    payload = build_payload_ok()
    create_resp = requests.post(create_url, json=payload, timeout=TIMEOUT_S)
    assert create_resp.status_code == 200

    item_id = extract_item_id_from_status(create_resp.json())
    assert item_id != ""

    # получаем статистику
    stat_url = f"{BASE_URL}/api/1/statistic/{item_id}"
    stat_resp = requests.get(stat_url, timeout=TIMEOUT_S)
    assert stat_resp.status_code == 200

    data = stat_resp.json()
    assert isinstance(data, dict)
    assert data != {}


# 6) Негативный тест: неверные типы -> 400
def test_6_create_item_invalid_types():
    url = f"{BASE_URL}/api/1/item"
    payload = build_payload_ok()

    payload["price"] = "1"
    payload["statistics"]["likes"] = "10"
    payload["statistics"]["viewCount"] = "100"
    payload["statistics"]["contacts"] = "5"

    resp = requests.post(url, json=payload, timeout=TIMEOUT_S)
    assert resp.status_code == 400
