# Objective: Introspect runtime contexts and monitor open workload queues on the active loop.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine งานตัวอย่างสำหรับตรวจสอบ Task ทั้งหมดใน Event Loop โดยรับพารามิเตอร์ number
async def dynamic_job(number):
    # อธิบาย: พัก Coroutine เป็นเวลา 1.0 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(1.0)

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # 
    # อธิบาย: ดึง Task ที่กำลังรัน Coroutine main() อยู่ในขณะนี้
    me = asyncio.current_task()
    # อธิบาย: ตั้งชื่อ Task ปัจจุบันของ main() เป็น Main-Coordinator
    me.set_name("Main-Coordinator")
    # อธิบาย: อ่านชื่อ Task ปัจจุบันแล้วแสดงผล
    print(f"{ctime()} Active Execution Context Name: {me.get_name()}")

    # 
    # อธิบาย: สร้าง Task หลายตัวด้วย List Comprehension พร้อมตั้งชื่อ Job-0, Job-1, Job-2
    tasks = [asyncio.create_task(dynamic_job(i), name=f"Job-{i}") for i in range(3)]

    # 
    # อธิบาย: ดึง Set ของ Task ทุกตัวที่ยังไม่เสร็จใน Event Loop ปัจจุบัน
    all_active = asyncio.all_tasks()
    # อธิบาย: นับจำนวน Task ที่กำลัง Active อยู่ใน Event Loop แล้วแสดงผล
    print(f"{ctime()} Total Active Tasks inside Loop: {len(all_active)}")
    # อธิบาย: วนลูปผ่าน Task ที่ยัง Active ทุกตัว
    for t in all_active:
        # อธิบาย: แสดงชื่อของ Task แต่ละตัวที่กำลังอยู่ใน Event Loop
        print(f"{ctime()}  -> Active Queue Item: {t.get_name()}")

    # อธิบาย: พัก Coroutine เป็นเวลา 1.1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(1.1) # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
