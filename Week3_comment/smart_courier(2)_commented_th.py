# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime


# อธิบาย: ประกาศ Coroutine สำหรับจำลองงานจัดส่งพัสดุ โดยรับพารามิเตอร์ package_id, duration
async def delivery_task(package_id, duration):
    # อธิบาย: เริ่มบล็อก try เพื่อทดลองรันโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Courier started delivering {package_id}...")
        # อธิบาย: พัก Coroutine เป็นเวลา duration วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
        await asyncio.sleep(duration)
        # อธิบาย: คืนค่าข้อความผลลัพธ์จาก Coroutine ให้กับ Task หรือผู้ที่ await
        return f"Package {package_id} Delivered!"
    # อธิบาย: ดักจับ asyncio.CancelledError ซึ่งเกิดเมื่อ Task ถูกสั่ง cancel()
    except asyncio.CancelledError:
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        # อธิบาย: โยน Exception เดิมต่อขึ้นไป หลังจากทำ Clean-up/แสดงข้อความแล้ว
        raise


# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มสร้าง asyncio Task เพื่อให้ Coroutine ทำงานแบบ Concurrent ภายใต้ Event Loop
    task = asyncio.create_task(
        # อธิบาย: ส่ง Coroutine delivery_task พร้อม package_id และเวลาจัดส่งให้ create_task()
        delivery_task("P001", 5.0),
        # อธิบาย: ตั้งชื่อ Task เป็น Express-Courier เพื่อให้อ่าน Log และตรวจสอบสถานะได้ง่าย
        name="Express-Courier"
    # อธิบาย: ปิดโครงสร้างคำสั่งที่เริ่มไว้ในบรรทัดก่อนหน้า
    )

    # อธิบาย: พัก Coroutine เป็นเวลา 2 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(2)

    # อธิบาย: ตรวจว่า Task ทำงานเสร็จแล้วหรือยังด้วย done() และแสดงผล True/False
    print(f"{ctime()} Checking task '{task.get_name()}'. Is it done? {task.done()}")

    # อธิบาย: ตรวจว่า Task ทำงานเสร็จแล้วหรือยังด้วย done() และแสดงผล True/False
    if not task.done():
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Taking too long! Canceling the task...")
        # อธิบาย: ส่งคำขอยกเลิก Task; asyncio จะฉีด CancelledError เข้าไปใน Coroutine ณ จุด await ถัดไป
        task.cancel()

    # อธิบาย: เริ่มบล็อก try เพื่อทดลองรันโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: รอ Task นี้จนเสร็จ; ถ้า Task ถูกยกเลิกอาจได้รับ CancelledError
        await task
    # อธิบาย: ดักจับ asyncio.CancelledError ซึ่งเกิดเมื่อ Task ถูกสั่ง cancel()
    except asyncio.CancelledError:
        # อธิบาย: ไม่ทำอะไรในบล็อกนี้ ใช้เพื่อให้โครงสร้างไวยากรณ์สมบูรณ์
        pass

    # อธิบาย: ตรวจว่า Task ถูกยกเลิกอย่างเป็นทางการแล้วหรือยังด้วย cancelled()
    print(f"{ctime()} Final verify: Is task officially canceled? {task.cancelled()}")


# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
