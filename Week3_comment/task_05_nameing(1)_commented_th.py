# Objective: Label task objects explicitly to simplify logging and production tracking.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine งานเบื้องหลังสำหรับสาธิตการตั้งชื่อ Task
async def background_worker():
    # อธิบาย: พัก Coroutine เป็นเวลา 0.1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(0.1)

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มสร้าง asyncio Task เพื่อให้ Coroutine ทำงานแบบ Concurrent ภายใต้ Event Loop
    task = asyncio.create_task(background_worker())

    # 
    # อธิบาย: อ่านชื่อ Task ปัจจุบันด้วย get_name() แล้วแสดงออกทางหน้าจอ
    print(f"{ctime()} Initial Name: {task.get_name()}") # 

    # 
    # อธิบาย: เปลี่ยนชื่อ Task เป็น Payment-Gateway-Validator เพื่อให้ติดตาม Task ใน Log ได้ง่าย
    task.set_name("Payment-Gateway-Validator")
    # อธิบาย: อ่านชื่อ Task ปัจจุบันด้วย get_name() แล้วแสดงออกทางหน้าจอ
    print(f"{ctime()} Updated Name: {task.get_name()}") # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
