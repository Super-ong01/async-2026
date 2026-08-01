# Program 7: Concurrent Tasks (Dual Tasks)
# Concept: Scheduling multiple concurrent tasks and awaiting them.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ time, ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import time, ctime

# อธิบาย: ประกาศ Coroutine Function สำหรับจำลองการทำสปาเกตตี โดยรับพารามิเตอร์ customer
async def cook_spaghetti(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Starting cooking for Customer {customer}...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} -> Finished cooking for Customer {customer}!")

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start_time เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start_time = time()
    # อธิบาย: สร้าง asyncio Task ชื่อ task_a จาก cook_spaghetti("A") และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_a = asyncio.create_task(cook_spaghetti("A"))
    # อธิบาย: สร้าง asyncio Task ชื่อ task_b จาก cook_spaghetti("B") และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_b = asyncio.create_task(cook_spaghetti("B"))

    # อธิบาย: รอให้ task_a ทำงานเสร็จ; ระหว่างรอ Event Loop ยังสามารถสลับไปทำ Task อื่นได้
    await task_a
    # อธิบาย: รอให้ task_b ทำงานเสร็จ; ถ้า Task ทำเสร็จแล้วจะผ่านบรรทัดนี้ได้ทันที
    await task_b
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"Total Operation Time: {time() - start_time:.2f} seconds")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
