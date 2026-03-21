import requests

BASE_URL = "http://127.0.0.1:8000"


def api_get_records():
    resp = requests.get(f"{BASE_URL}/records")
    resp.raise_for_status()
    return resp.json()


def api_post_record(payload: dict):
    resp = requests.post(f"{BASE_URL}/records", json=payload)
    resp.raise_for_status()
    return resp.json()


def api_delete_record(record_id: int):
    resp = requests.delete(f"{BASE_URL}/records/{record_id}")
    if resp.status_code == 404:
        # вернём специальный маркер, чтобы UI показал ошибку
        return {"status": "not_found"}
    resp.raise_for_status()
    return resp.json()

