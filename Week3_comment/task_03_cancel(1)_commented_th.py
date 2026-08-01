# Objective: Stop an ongoing execution prematurely by triggering a cancellation exception.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine งานเบื้องหลังที่ทำงานวนซ้ำจนถูกยกเลิก
async def background_loop():
    # อธิบาย: เริ่มบล็อก try เพื่อทดลองรันโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Worker: Starting long infinite process...")
        # อธิบาย: เริ่มลูปไม่สิ้นสุด เพื่อให้ Worker ทำงานต่อเนื่องจนกว่าจะถูกยกเลิก
        while True:
            # อธิบาย: พัก Coroutine เป็นเวลา 1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
            await asyncio.sleep(1)
            # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
            print(f"{ctime()} Worker: Still ticking...")
    # อธิบาย: ดักจับ asyncio.CancelledError ซึ่งเกิดเมื่อ Task ถูกสั่ง cancel()
    except asyncio.CancelledError:
        # 
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
        print(f"{ctime()} Worker: Interrupted! Executing clean-up logic before exit...")

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มสร้าง asyncio Task เพื่อให้ Coroutine ทำงานแบบ Concurrent ภายใต้ Event Loop
    task = asyncio.create_task(background_loop())
    # อธิบาย: พัก Coroutine เป็นเวลา 2.5 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(2.5) # 

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Main: Changing plans, canceling the worker task now!")
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    task.cancel() # 
    # อธิบาย: พัก Coroutine เป็นเวลา 0.1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(0.1) # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
