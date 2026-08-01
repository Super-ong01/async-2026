# Objective: Enforce strict deadlines on operations and raise errors if exceeded.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine สำหรับจำลอง Query ที่ใช้เวลานาน
async def long_query_simulation():
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Database: Fetching data...")
    # อธิบาย: พัก Coroutine เป็นเวลา 5.0 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(5.0) # 
    # อธิบาย: คืนข้อมูลรายงานจำลอง หาก Query ทำงานเสร็จก่อน Timeout
    return "Heavy_Report_Data"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มบล็อก try เพื่อทดลองรันโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Main: Enforcing a strict 2-second timeout deadline...")
        # 
        # อธิบาย: ใช้ wait_for() ครอบ Coroutine และกำหนด Timeout 2 วินาที; ถ้าเกินเวลาจะยกเลิกงานและเกิด TimeoutError
        result = await asyncio.wait_for(long_query_simulation(), timeout=2.0)
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Result acquired: {result}")
    # อธิบาย: ดักจับ TimeoutError เมื่อ wait_for() รอเกินเวลาที่กำหนด
    except asyncio.TimeoutError:
        # 
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Main Error Alert: Operation timed out! Task terminated.")

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
