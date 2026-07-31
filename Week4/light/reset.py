# reset_all_students_lights.py

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, ctime

BASE_URL = "http://172.16.2.117:8088"

STUDENT_IDS = [
    "6710301001",
    "6710301003",
    "6710301004",
    "6710301005",
    "6710301006",
    "6710301007",
    "6710301008",

    "6710301009",
    "6710301010",
    "6710301011",
    "6710301012",
    "6710301017",
    "6710301018",
    "6710301019",

    "6710301020",
    "6710301021",
    "6710301022",
    "6710301023",
    "6710301024",
    "6710301025",
    "6710301027",

    "6710301030",
    "6710301031",
    "6710301032",
    "6710301033",
    "6710301034",
    "6710301036",
    "6710301037",

    "6710301041",
    "6710301042",
    "6710301043",
    "6710301045",
    "6710301047",
    "6710301048",
    "6710301049",

    "6710301051",
    "6710301054",

    "6720301001",
    "6720301002",
    "6720301003",
    "6720301004",
]


def reset_student_lights(student_id: str) -> dict:
    """รีเซ็ตไฟทั้ง 4 ดวงของนักศึกษาหนึ่งคนเป็น OFF"""

    url = f"{BASE_URL}/api/{student_id}/lights/reset"

    try:
        response = requests.delete(url, timeout=10.0)

        if response.status_code == 200:
            return {
                "student_id": student_id,
                "success": True,
                "result": response.json(),
            }

        return {
            "student_id": student_id,
            "success": False,
            "result": f"HTTP {response.status_code}: {response.text}",
        }

    except requests.exceptions.RequestException as error:
        return {
            "student_id": student_id,
            "success": False,
            "result": f"Connection failed: {error}",
        }


def main():
    print(f"{ctime()} | Resetting every student's lights...")
    print(f"Total students: {len(STUDENT_IDS)}")

    start_time = time()
    success_count = 0
    error_count = 0

    # ส่งพร้อมกันสูงสุด 10 requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(reset_student_lights, student_id): student_id
            for student_id in STUDENT_IDS
        }

        for future in as_completed(futures):
            result = future.result()
            student_id = result["student_id"]

            if result["success"]:
                success_count += 1
                print(f"{ctime()} | {student_id} -> OFF ✅")
            else:
                error_count += 1
                print(
                    f"{ctime()} | {student_id} -> ERROR ❌ "
                    f"{result['result']}"
                )

    total_time = time() - start_time

    print("\n" + "=" * 50)
    print(f"Success : {success_count}")
    print(f"Errors  : {error_count}")
    print(f"Total   : {len(STUDENT_IDS)}")
    print(f"Time    : {total_time:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()