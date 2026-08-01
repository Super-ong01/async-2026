# Objective: Group multiple operations to run concurrently and return an ordered list of outputs.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ time, ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import time, ctime

# อธิบาย: ประกาศ Coroutine สำหรับจำลองการอ่านข้อมูลจากฐานข้อมูล โดยรับพารามิเตอร์ table_name, latency
async def fetch_db_record(table_name, latency):
    # อธิบาย: พัก Coroutine เป็นเวลา latency วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(latency)
    # อธิบาย: คืนค่าข้อความผลลัพธ์จาก Coroutine ให้กับ Task หรือผู้ที่ await
    return f"RowData_{table_name}"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: บันทึกเวลาเริ่มต้น เพื่อใช้คำนวณเวลารวมของการทำงาน
    start = time()

    # 
    # อธิบาย: ใช้ asyncio.gather() รัน Coroutine หลายตัวแบบ Concurrent และรอจนทั้งหมดเสร็จ โดยเก็บผลลัพธ์ตามลำดับที่ส่งเข้าไป
    results = await asyncio.gather(
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
        fetch_db_record("Users", 1.0),
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
        fetch_db_record("Products", 0.5),
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        fetch_db_record("Invoices", 1.0)
    # อธิบาย: ปิดโครงสร้างคำสั่งที่เริ่มไว้ในบรรทัดก่อนหน้า
    )

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Aggregated Output Results List: {results}")
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Execution Completed in: {time() - start:.2f} seconds") #

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
