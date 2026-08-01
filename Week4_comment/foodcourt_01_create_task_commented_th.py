# foodcourt_01_create_task.py
# อธิบาย: นำเข้าโมดูล asyncio สำหรับ Coroutine, Task, Event Loop และการทำงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import ctime
# อธิบาย: นำเข้าฟังก์ชัน send_order_to_kitchen จาก food_utils เพื่อส่งออเดอร์ไปยัง Food Court API
from food_utils import send_order_to_kitchen

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: กำหนดรหัสนักศึกษาที่จะใช้ส่งไปพร้อมคำสั่งในตัวอย่างนี้
    MY_STUDENT_ID = "6710301004"
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | --- [Task 1] Practice using create_task to queue an order ---")

    # 1. Create a task for ordering chicken rice without awaiting it immediately.
    # Store the task object in 'food_task'.
    # อธิบาย: สร้าง asyncio Task แล้วเก็บไว้ในตัวแปร food_task เพื่อให้ Coroutine เริ่มทำงานแบบ Concurrent
    food_task = asyncio.create_task(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Mixed")
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )

    # 2. Check the task status immediately using .done() to see if it is finished.
    # อธิบาย: ตรวจสถานะ Task ด้วย done() ว่าเสร็จแล้วหรือยัง
    print(f"{ctime()} | Checking task status immediately: Is it done? = {food_task.done()}")

    # 3. Use await to fetch the result once the task is fully completed.
    # อธิบาย: รอ food_task จนเสร็จ แล้วรับผลลัพธ์ที่ Coroutine คืนกลับมา
    result = await food_task
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | System Response: {result}")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ ก่อนเรียกฟังก์ชันหลัก
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
