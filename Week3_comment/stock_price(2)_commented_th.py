# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime


# อธิบาย: ประกาศ Coroutine สำหรับดึงราคาหุ้น โดยรับพารามิเตอร์ server_name, delay
async def fetch_stock_price(server_name, delay):
    # อธิบาย: พัก Coroutine เป็นเวลา delay วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(delay)
    # อธิบาย: คืนค่าข้อความผลลัพธ์จาก Coroutine ให้กับ Task หรือผู้ที่ await
    return f"[{server_name}] Price: 150 USD"


# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: สร้าง Set สำหรับเก็บ Task หลายตัวที่ต้องการให้ทำงานพร้อมกัน
    tasks = {
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Alpha", 3.0)),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Beta", 0.8)),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(fetch_stock_price("Gamma", 1.5)),
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
