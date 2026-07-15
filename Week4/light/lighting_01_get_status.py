# lab_lighting_sync.py

import requests
from time import time, ctime

BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301004"

LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


def get_all_lights_status(student_id: str) -> dict:
    """GET สถานะไฟทั้งหมดของนักเรียน"""
    url = f"{BASE_URL}/api/{student_id}/lights"
    response = requests.get(url)
    return response.json()


def set_light_status(student_id: str, light_id: str, status: str) -> dict:
    """POST สั่งเปิด/ปิดไฟดวงเดียว (จะบล็อครอจน hardware delay เสร็จ)"""
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    payload = {"status": status}
    try:
        response = requests.post(url, json=payload, timeout=10.0)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "ERROR", "detail": f"HTTP Error {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}


def reset_all_lights(student_id: str) -> dict:
    """DELETE รีเซ็ตไฟทั้งหมดเป็น OFF"""
    url = f"{BASE_URL}/api/{student_id}/lights/reset"
    response = requests.delete(url)
    return response.json()


def main():
    print(f"{ctime()} | --- Sync Version: Turning ON all 4 lights ---")

    start_time = time()

    # ทำงานทีละดวง เรียงตามลำดับ (sequential/blocking)
    for light_id in LIGHTS:
        light_start = time()
        result = set_light_status(STUDENT_ID, light_id, "ON")
        elapsed = time() - light_start
        print(
            f"{ctime()} | {light_id} -> {result.get('current_status', result)} "
            f"(took {elapsed:.2f}s)"
        )

    total_time = time() - start_time
    print(f"{ctime()} | Total execution time: {total_time:.2f} seconds.")


if __name__ == "__main__":
    main()