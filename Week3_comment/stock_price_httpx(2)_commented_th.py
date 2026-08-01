# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าไลบรารี httpx สำหรับส่ง HTTP Request; ในไฟล์นี้ใช้ AsyncClient เพื่อไม่ให้บล็อก Event Loop
import httpx
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime


# อธิบาย: ประกาศ Coroutine สำหรับดึงราคาหุ้น โดยรับพารามิเตอร์ server_name: str
async def fetch_stock_price(server_name: str):
# อธิบาย: พบ Git merge conflict marker ฝั่ง HEAD: บรรทัดนี้ไม่ใช่ Python ที่ถูกต้องและต้องแก้ conflict ก่อนรันไฟล์
<<<<<<< HEAD
    # อธิบาย: สร้าง URL ของ Mock Stock API โดยนำชื่อเซิร์ฟเวอร์มาต่อท้าย Endpoint
    url = f"http://127.0.0.1:8088/price/{server_name}"

# อธิบาย: Git merge conflict marker ใช้คั่นโค้ดสองเวอร์ชัน: บรรทัดนี้ทำให้ไฟล์รันไม่ได้จนกว่าจะแก้ conflict
=======
    # อธิบาย: ข้อความ Docstring ใช้อธิบายวัตถุประสงค์และเงื่อนไขของฟังก์ชัน
    """
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    TODO: Assignment 3 - เขียนฟังก์ชันเชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    1. กำหนดเป้าหมายไปที่พอร์ต 8088 ตามสเปกเซิร์ฟเวอร์ของอาจารย์
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    2. ใช้ httpx.AsyncClient() ดึงข้อมูลเพื่อไม่ให้เกิดการ Block สัญญาณ Event Loop
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    3. นำข้อมูล JSON (server และ price_usd) มาจัดฟอร์แมตแสดงผล
    # อธิบาย: ข้อความ Docstring ใช้อธิบายวัตถุประสงค์และเงื่อนไขของฟังก์ชัน
    """
    # อธิบาย: สร้าง URL ของ Mock Stock API โดยนำชื่อเซิร์ฟเวอร์มาต่อท้าย Endpoint
    url = f"http://127.0.0.1:8088/price/{server_name}"

# อธิบาย: Git merge conflict marker ฝั่งอีก branch: ต้องเลือก/รวมโค้ดแล้วลบ marker ก่อนจึงจะรันได้
>>>>>>> upstream/main
    # อธิบาย: เปิด Async HTTP Client ภายใน Context Manager เพื่อปิด Connection/Resource ให้อัตโนมัติเมื่อใช้งานเสร็จ
    async with httpx.AsyncClient() as client:
        # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous ไปยัง URL และรอ Response โดยไม่บล็อก Event Loop
        response = await client.get(url)
        # อธิบาย: แปลงข้อมูล JSON จาก Response ให้เป็น Python Dictionary
        data = response.json()
        # อธิบาย: จัดรูปแบบชื่อเซิร์ฟเวอร์และราคาหุ้นจาก JSON แล้วคืนค่าเป็นข้อความ
        return f"[{data['server']}] Price: {data['price_usd']} USD"


# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: สร้าง Set สำหรับเก็บ Task หลายตัวที่ต้องการให้ทำงานพร้อมกัน
    tasks = {
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Alpha")),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Beta")),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Gamma")),
    # อธิบาย: ปิด Dictionary ที่ใช้เป็นข้อมูลตอบกลับ
    }

    # อธิบาย: ใช้ asyncio.wait() รอ Task ตามเงื่อนไขที่กำหนด และแยกผลเป็น Set: done กับ pending
    done, pending = await asyncio.wait(
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
        tasks,
        # อธิบาย: กำหนดให้ wait() คืนค่าทันทีเมื่อมี Task อย่างน้อยหนึ่งตัวทำงานเสร็จก่อน
        return_when=asyncio.FIRST_COMPLETED
    # อธิบาย: ปิดโครงสร้างคำสั่งที่เริ่มไว้ในบรรทัดก่อนหน้า
    )

    # อธิบาย: วนลูป Task ที่ชนะหรือเสร็จก่อน เพื่ออ่านผลลัพธ์
    for winner in done:
        # อธิบาย: อ่านค่าที่ Task ผู้ชนะ return กลับมาแล้วแสดงผล
        print(f"{ctime()} Winner Result: {winner.result()}")

    # อธิบาย: นับจำนวน Task ที่ยังไม่เสร็จและอยู่ในสถานะ Pending
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")

    # อธิบาย: วนลูปผ่าน Task ที่ยังไม่เสร็จเพื่อทำความสะอาดหรือยกเลิก
    for task in pending:
        # อธิบาย: ส่งคำขอยกเลิก Task; asyncio จะฉีด CancelledError เข้าไปใน Coroutine ณ จุด await ถัดไป
        task.cancel()


# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
