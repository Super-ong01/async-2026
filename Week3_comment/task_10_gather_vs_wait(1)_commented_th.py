# Objective: Compare the structural and mechanical differences of both strategies in a racing scenario.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine สำหรับจำลองผู้เข้าแข่งขันแต่ละคน โดยรับพารามิเตอร์ name, speed
async def runner(name, speed):
    # อธิบาย: พัก Coroutine เป็นเวลา speed วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(speed)
    # อธิบาย: คืนค่าข้อความผลลัพธ์จาก Coroutine ให้กับ Task หรือผู้ที่ await
    return f"{name} crossed line!"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # 
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} --- Starting gather() approach (Unified Aggregation) ---")
    # อธิบาย: ใช้ gather() รอผู้แข่งขันทุกคนให้เสร็จ แล้วคืนผลลัพธ์เป็นลิสต์ตามลำดับอาร์กิวเมนต์
    all_finishes = await asyncio.gather(runner("A", 0.5), runner("B", 2.0))
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Gather output: {all_finishes}\n")

    # 
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} --- Starting wait() approach (State control / Racing) ---")
    # อธิบาย: สร้าง Set ของ Task ผู้เข้าแข่งขัน เพื่อใช้กับ asyncio.wait()
    active_tasks = {asyncio.create_task(runner("A", 0.5)), asyncio.create_task(runner("B", 2.0))}

    # อธิบาย: ใช้ asyncio.wait() รอ Task ตามเงื่อนไขที่กำหนด และแยกผลเป็น Set: done กับ pending
    done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)
    # อธิบาย: อ่านค่าที่ Task ผู้ชนะ return กลับมาแล้วแสดงผล
    print(f"{ctime()} Wait output: The winner of the race is -> {list(done)[0].result()}")

    # 
    # อธิบาย: วนลูปผ่าน Task ที่ยัง Pending เพื่อยกเลิกผู้ที่ไม่ชนะ/ไม่ต้องรอแล้ว
    for t in pending:
        # อธิบาย: ส่งคำขอยกเลิก Task ที่ยังทำงานค้างอยู่
        t.cancel()

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
