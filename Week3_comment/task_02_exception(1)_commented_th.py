# Objective: Extract returned data safely and inspect crashed tasks without breaking the main loop.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine สำหรับทดลองหารตัวเลขและทดสอบ Exception โดยรับพารามิเตอร์ a, b
async def division_worker(a, b):
    # อธิบาย: พัก Coroutine เป็นเวลา 0.5 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(0.5)
    # อธิบาย: คืนค่าผลหาร a / b; ถ้า b เป็น 0 จะเกิด ZeroDivisionError
    return a / b # 

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: สร้าง Task ที่คาดว่าจะทำงานสำเร็จจากการหาร 10 ด้วย 2
    task_success = asyncio.create_task(division_worker(10, 2))
    # อธิบาย: สร้าง Task ที่จะเกิดข้อผิดพลาดจากการหารด้วยศูนย์ เพื่อใช้ทดลองตรวจ Exception
    task_fail = asyncio.create_task(division_worker(10, 0))

    # 
    # อธิบาย: พัก Coroutine เป็นเวลา 1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(1)

    # 
    # อธิบาย: ตรวจว่า Task สำเร็จแล้วและไม่มี Exception ก่อนเรียก result() เพื่ออ่านค่าผลลัพธ์อย่างปลอดภัย
    if task_success.done() and not task_success.exception():
        # อธิบาย: อ่านค่าที่ Task สำเร็จ return กลับมา แล้วแสดงผล
        print(f"{ctime()} Task Success Result: {task_success.result()}") # 

    # 
    # อธิบาย: ตรวจว่า Task ที่ตั้งใจให้ล้มเหลวทำงานจบแล้วหรือยัง
    if task_fail.done():
        # อธิบาย: อ่าน Exception ที่เกิดใน Task และแสดงชื่อชนิดของ Exception โดยไม่ทำให้ main ล้มตาม
        print(f"{ctime()} Task Fail Exception: {type(task_fail.exception()).__name__}") # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
