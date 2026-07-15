# lab_lighting_async.py

import asyncio
from time import time, ctime

import httpx


BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301012"

LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


async def get_all_lights_status(
    client: httpx.AsyncClient,
    student_id: str
) -> dict:
    """GET สถานะไฟทั้งหมดของนักเรียน"""

    url = f"{BASE_URL}/api/{student_id}/lights"

    response = await client.get(url)
    response.raise_for_status()

    return response.json()


async def set_light_status(
    client: httpx.AsyncClient,
    student_id: str,
    light_id: str,
    status: str
) -> dict:
    """POST สั่งเปิดหรือปิดไฟหนึ่งดวงแบบ asynchronous"""

    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    payload = {"status": status}

    light_start = time()

    try:
        response = await client.post(
            url,
            json=payload,
            timeout=10.0
        )

        elapsed = time() - light_start

        if response.status_code == 200:
            result = response.json()
        else:
            result = {
                "status": "ERROR",
                "detail": f"HTTP Error {response.status_code}"
            }

        return {
            "light_id": light_id,
            "result": result,
            "elapsed": elapsed
        }

    except httpx.RequestError as error:
        elapsed = time() - light_start

        return {
            "light_id": light_id,
            "result": {
                "status": "ERROR",
                "detail": f"Connection failed: {error}"
            },
            "elapsed": elapsed
        }


async def reset_all_lights(
    client: httpx.AsyncClient,
    student_id: str
) -> dict:
    """DELETE รีเซ็ตไฟทั้งหมดเป็น OFF"""

    url = f"{BASE_URL}/api/{student_id}/lights/reset"

    response = await client.delete(url)
    response.raise_for_status()

    return response.json()


async def main():
    print(f"{ctime()} | --- Async Version: Turning ON all 4 lights ---")

    start_time = time()

    async with httpx.AsyncClient() as client:

        # สร้าง Task สำหรับเปิดไฟทั้ง 4 ดวงพร้อมกัน
        tasks = []

        for light_id in LIGHTS:
            task = asyncio.create_task(
                set_light_status(
                    client,
                    STUDENT_ID,
                    light_id,
                    "ON"
                )
            )

            tasks.append(task)

        # รอผลลัพธ์ของไฟทุกดวง
        results = await asyncio.gather(*tasks)

        # แสดงผลของแต่ละดวง
        for item in results:
            light_id = item["light_id"]
            result = item["result"]
            elapsed = item["elapsed"]

            print(
                f"{ctime()} | {light_id} -> "
                f"{result.get('current_status', result)} "
                f"(took {elapsed:.2f}s)"
            )

    total_time = time() - start_time

    print(
        f"{ctime()} | Total execution time: "
        f"{total_time:.2f} seconds."
    )


if __name__ == "__main__":
    asyncio.run(main())