# lab_lighting_async.py

# อธิบาย: นำเข้าโมดูล asyncio สำหรับ Coroutine, Task, Event Loop และการทำงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import time, ctime

# อธิบาย: นำเข้า httpx เพื่อส่ง HTTP Request แบบ Asynchronous โดยไม่บล็อก Event Loop
import httpx


# อธิบาย: กำหนด Base URL ของ API Server ที่โปรแกรมจะเชื่อมต่อ
BASE_URL = "http://172.16.2.117:8088"
# อธิบาย: กำหนดรหัสนักศึกษาที่ใช้ระบุชุดข้อมูล/อุปกรณ์ของผู้ใช้ใน API
STUDENT_ID = "6710301004"

# อธิบาย: สร้างลิสต์รหัสหลอดไฟทั้ง 4 ดวงที่โปรแกรมจะควบคุม
LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
async def get_all_lights_status(
    # อธิบาย: กำหนดพารามิเตอร์ client ให้เป็น Async HTTP Client ของ httpx
    client: httpx.AsyncClient,
    # อธิบาย: กำหนดฟิลด์ student_id ให้ต้องเป็นข้อความ
    student_id: str
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
) -> dict:
    """GET สถานะไฟทั้งหมดของนักเรียน"""

    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights"

    # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
    response = await client.get(url)
    # อธิบาย: ตรวจ HTTP Status Code และยก Exception หาก Response เป็นข้อผิดพลาด
    response.raise_for_status()

    # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
    return response.json()


# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
async def set_light_status(
    # อธิบาย: กำหนดพารามิเตอร์ client ให้เป็น Async HTTP Client ของ httpx
    client: httpx.AsyncClient,
    # อธิบาย: กำหนดฟิลด์ student_id ให้ต้องเป็นข้อความ
    student_id: str,
    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
    light_id: str,
    # อธิบาย: กำหนดพารามิเตอร์ status ให้เป็นชนิดข้อความ
    status: str
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
) -> dict:
    """POST สั่งเปิดหรือปิดไฟหนึ่งดวงแบบ asynchronous"""

    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    # อธิบาย: สร้าง Dictionary สำหรับใช้เป็น JSON Request Body ที่จะส่งไปยัง API
    payload = {"status": status}

    # อธิบาย: บันทึกเวลาเริ่มทำงานของไฟดวงนี้ เพื่อคำนวณเวลาที่ใช้รายดวง
    light_start = time()

    # อธิบาย: เริ่มบล็อก try สำหรับคำสั่งที่อาจเกิด Exception
    try:
        # อธิบาย: ส่ง HTTP POST Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
        response = await client.post(
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
            url,
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
            json=payload,
            # อธิบาย: กำหนดจำนวนวินาทีสูงสุดก่อนเกิด TimeoutError
            timeout=10.0
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

        # อธิบาย: คำนวณเวลาที่ใช้กับไฟดวงนี้
        elapsed = time() - light_start

        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจว่าจะทำคำสั่งในบล็อกนี้หรือไม่
        if response.status_code == 200:
            # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วเก็บไว้ใน result
            result = response.json()
        # อธิบาย: ถ้าเงื่อนไขก่อนหน้าไม่เป็นจริง ให้ทำงานในส่วน else
        else:
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            result = {
                # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
                "status": "ERROR",
                # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
                "detail": f"HTTP Error {response.status_code}"
            # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
            }

        # อธิบาย: เริ่มสร้าง Dictionary เพื่อใช้เป็นข้อมูลผลลัพธ์/JSON Response
        return {
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "light_id": light_id,
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "result": result,
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "elapsed": elapsed
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        }

    # อธิบาย: ดักจับข้อผิดพลาดด้านการเชื่อมต่อ HTTP ของ httpx
    except httpx.RequestError as error:
        # อธิบาย: คำนวณเวลาที่ใช้กับไฟดวงนี้
        elapsed = time() - light_start

        # อธิบาย: เริ่มสร้าง Dictionary เพื่อใช้เป็นข้อมูลผลลัพธ์/JSON Response
        return {
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "light_id": light_id,
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "result": {
                # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
                "status": "ERROR",
                # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
                "detail": f"Connection failed: {error}"
            # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
            },
            # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
            "elapsed": elapsed
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        }


# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
async def reset_all_lights(
    # อธิบาย: กำหนดพารามิเตอร์ client ให้เป็น Async HTTP Client ของ httpx
    client: httpx.AsyncClient,
    # อธิบาย: กำหนดฟิลด์ student_id ให้ต้องเป็นข้อความ
    student_id: str
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
) -> dict:
    """DELETE รีเซ็ตไฟทั้งหมดเป็น OFF"""

    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights/reset"

    # อธิบาย: ส่ง HTTP DELETE Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
    response = await client.delete(url)
    # อธิบาย: ตรวจ HTTP Status Code และยก Exception หาก Response เป็นข้อผิดพลาด
    response.raise_for_status()

    # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
    return response.json()


# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | --- Async Version: Turning ON all 4 lights ---")

    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณเวลารวม
    start_time = time()

    # อธิบาย: สร้าง Async HTTP Client ภายใน Context Manager เพื่อเปิด/ปิดทรัพยากรให้อัตโนมัติ
    async with httpx.AsyncClient() as client:

        # สร้าง Task สำหรับเปิดไฟทั้ง 4 ดวงพร้อมกัน
        # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บ Task หลายตัว
        tasks = []

        # อธิบาย: วนลูปทีละรหัสไฟจากลิสต์ LIGHTS
        for light_id in LIGHTS:
            # อธิบาย: สร้าง asyncio Task แล้วเก็บไว้ในตัวแปร task เพื่อให้ Coroutine เริ่มทำงานแบบ Concurrent
            task = asyncio.create_task(
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                set_light_status(
                    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
                    client,
                    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
                    STUDENT_ID,
                    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
                    light_id,
                    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                    "ON"
                # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
                )
            # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
            )

            # อธิบาย: เพิ่ม Task ที่สร้างแล้วลงในลิสต์ tasks
            tasks.append(task)

        # รอผลลัพธ์ของไฟทุกดวง
        # อธิบาย: รอ Task ทุกตัวให้เสร็จด้วย gather() และเก็บผลลัพธ์เรียงตามลำดับที่ส่งเข้าไป
        results = await asyncio.gather(*tasks)

        # แสดงผลของแต่ละดวง
        # อธิบาย: วนลูปผ่านผลลัพธ์ของไฟแต่ละดวง
        for item in results:
            # อธิบาย: ดึงรหัสไฟจากผลลัพธ์ของไฟดวงปัจจุบัน
            light_id = item["light_id"]
            # อธิบาย: ดึงผลลัพธ์ API ของไฟดวงปัจจุบัน
            result = item["result"]
            # อธิบาย: ดึงเวลาที่ใช้ของไฟดวงปัจจุบัน
            elapsed = item["elapsed"]

            # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
            print(
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                f"{ctime()} | {light_id} -> "
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                f"{result.get('current_status', result)} "
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                f"(took {elapsed:.2f}s)"
            # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
            )

    # อธิบาย: คำนวณเวลารวมทั้งหมดตั้งแต่เริ่มโปรแกรม
    total_time = time() - start_time

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        f"{ctime()} | Total execution time: "
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        f"{total_time:.2f} seconds."
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )


# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ ก่อนเรียกฟังก์ชันหลัก
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
