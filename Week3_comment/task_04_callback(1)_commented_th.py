# Objective: Attach a plain synchronous function that automatically triggers the moment a task finishes.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Callback Function แบบปกติ ซึ่งจะถูกเรียกอัตโนมัติเมื่อ Task ที่ผูกไว้ทำงานเสร็จ
def alert_manager(finished_task):
    # 
    # อธิบาย: อ่านค่าผลลัพธ์จาก Task ที่เสร็จแล้วภายใน Callback และแสดงผล
    print(f"{ctime()} Callback Triggered! Task output fetched: {finished_task.result()}")

# อธิบาย: ประกาศ Coroutine สำหรับจำลองการดาวน์โหลดไฟล์
async def download_file():
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Downloading packet...")
    # อธิบาย: พัก Coroutine เป็นเวลา 1.0 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(1.0)
    # อธิบาย: คืนชื่อไฟล์จำลองหลังดาวน์โหลดเสร็จ
    return "Data_Payload.zip"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: เริ่มสร้าง asyncio Task เพื่อให้ Coroutine ทำงานแบบ Concurrent ภายใต้ Event Loop
    task = asyncio.create_task(download_file())
    # 
    # อธิบาย: ผูก Callback alert_manager เข้ากับ Task เพื่อให้ถูกเรียกอัตโนมัติทันทีที่ Task เสร็จ
    task.add_done_callback(alert_manager)

    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    await task # 

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
