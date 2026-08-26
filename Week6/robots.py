import asyncio
import time
import httpx

# ==========================================
# 1. Configuration & Constants
# ==========================================
<<<<<<< HEAD
STUDENT_ID = "6710301004"
BASE_URL = "http://172.16.2.117:8088"

# กำหนดลำดับชิ้นส่วนและหุ่นยนต์
PARTS = ["A", "B", "C"]
ROBOTS = ["robot_1", "robot_2", "robot_3", "robot_4"]


async def reset_factory(client: httpx.AsyncClient):
    """ส่ง Request เพื่อทำการ Reset สถานะของหุ่นยนต์ทั้งหมด"""
    response = await client.post(f"/student/{STUDENT_ID}/reset")
    return response.json()

async def grab_part(client: httpx.AsyncClient, robot_id: str, part: str):
    """สั่งให้หุ่นยนต์หยิบชิ้นส่วน 1 ชิ้น"""
    response = await client.post(
        f"/student/{STUDENT_ID}/robot/{robot_id}/grab",
        json={"part": part}
    )
    return response.json()

async def run_robot_task(client: httpx.AsyncClient, robot_id: str):
    """สั่งให้หุ่นยนต์ 1 ตัว ทำการหยิบชิ้นส่วน A, B, และ C ตามลำดับ"""
    results = []
    for part in PARTS:
        print(f"[{robot_id}] Grabbing part '{part}'...")
        res = await grab_part(client, robot_id, part)
        results.append(res)
        print(f"[{robot_id}] Finished part '{part}': {res}")
    return results
=======
STUDENT_ID = "" 
BASE_URL = ""

# กำหนดลำดับชิ้นส่วนและหุ่นยนต์
PARTS = ["A", "B", "C"]
ROBOTS = ["robot_1", "robot_2", "robot_3"]

# ==========================================
# 2. Async Functions Development
# ==========================================

async def reset_factory(client: httpx.AsyncClient):
    """ส่ง Request เพื่อทำการ Reset สถานะของหุ่นยนต์ทั้งหมดของรหัสนักเรียนนี้"""
    # TODO: เติมโค้ดการส่ง POST request ไปยัง /student/{STUDENT_ID}/reset
    pass

async def grab_part(client: httpx.AsyncClient, robot_id: str, part: str):
    """สั่งให้หุ่นยนต์หยิบชิ้นส่วน 1 ชิ้น"""
    # TODO: เติมโค้ดส่ง POST request ไปยัง /student/{STUDENT_ID}/robot/{robot_id}/grab
    # พร้อมแนบ JSON Payload {"part": part}
    pass

async def run_robot_task(client: httpx.AsyncClient, robot_id: str):
    """สั่งให้หุ่นยนต์ 1 ตัว ทำการหยิบชิ้นส่วน A, B, และ C ตามลำดับ"""
    # TODO: วนลูปหยิบชิ้นส่วนใน PARTS ตามลำดับเรียงกัน (Sequential inside single robot)
    pass
>>>>>>> 95a8a921d2ec4c879de9b0ef9ae2cab345058cd6

async def main():
    """ฟังก์ชันหลักสำหรับเริ่มการทำงานของหุ่นยนต์ทั้ง 4 ตัวแบบ Async"""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
<<<<<<< HEAD
        print(f"Resetting Factory for Student {STUDENT_ID}...")
        try:
            reset_res = await reset_factory(client)
            print(f"Factory Reset Result: {reset_res}")
        except Exception as err:
            print(f"Notice: Factory Reset ({err})")

        start_time = time.time()
        print("Starting Async Robot Operation...")

        # สั่งรัน run_robot_task ของหุ่นยนต์ทั้ง 4 ตัวพร้อมกันโดยใช้ asyncio.gather
        tasks = [run_robot_task(client, robot_id) for robot_id in ROBOTS]
        await asyncio.gather(*tasks)

=======
        print("Resetting Factory...")
        await reset_factory(client)
        
        start_time = time.time()
        print("Starting Async Robot Operation...")
        
        # TODO: สั่งรัน run_robot_task ของหุ่นยนต์ทั้ง 4 ตัวพร้อมกันโดยใช้ asyncio.gather
        
>>>>>>> 95a8a921d2ec4c879de9b0ef9ae2cab345058cd6
        elapsed_time = time.time() - start_time
        print(f"Finished all tasks in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())