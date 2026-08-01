# Objective: Learn how to query the lifecycle status of a task object.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine งานสั้น ๆ เพื่อใช้ตรวจสอบสถานะของ Task
async def short_job():
    # อธิบาย: พัก Coroutine เป็นเวลา 1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: คืนค่าข้อความ Success เมื่อ Coroutine ทำงานเสร็จ
    return "Success"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มสร้าง asyncio Task เพื่อให้ Coroutine ทำงานแบบ Concurrent ภายใต้ Event Loop
    task = asyncio.create_task(short_job())

    # 
    # อธิบาย: ตรวจว่า Task ทำงานเสร็จแล้วหรือยังด้วย done() และแสดงผล True/False
    print(f"{ctime()} Is task done? {task.done()}")          # 
    # อธิบาย: ตรวจว่า Task ถูกยกเลิกอย่างเป็นทางการแล้วหรือยังด้วย cancelled()
    print(f"{ctime()} Is task canceled? {task.cancelled()}")  # 

    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    await task # 

    # Inspect status again after it finishes
    # อธิบาย: ตรวจว่า Task ทำงานเสร็จแล้วหรือยังด้วย done() และแสดงผล True/False
    print(f"{ctime()} Is task done now? {task.done()}")      # 
    # อธิบาย: ตรวจว่า Task ถูกยกเลิกอย่างเป็นทางการแล้วหรือยังด้วย cancelled()
    print(f"{ctime()} Is task canceled now? {task.cancelled()}") # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
