# Program 8: Interleaving Tasks (Context Switching)
# Concept: Demonstrating how single-threaded event loop switches execution context between tasks.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine Function สำหรับงานของฝ่ายครัว
async def kitchen_crew():
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> [Chef] puts noodle in boiling water...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> [Chef] strains the noodle!")

# อธิบาย: ประกาศ Coroutine Function สำหรับงานของฝ่ายเครื่องดื่ม
async def bar_crew():
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> [Bar] starts grinding coffee bean...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> [Bar] pours espresso shot!")

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: สร้าง asyncio Task ชื่อ task_kitchen จาก kitchen_crew() และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_kitchen = asyncio.create_task(kitchen_crew())
    # อธิบาย: สร้าง asyncio Task ชื่อ task_bar จาก bar_crew() และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_bar = asyncio.create_task(bar_crew())

    # อธิบาย: รอ Task ของฝ่ายครัวให้เสร็จ โดยไม่บล็อก Event Loop
    await task_kitchen
    # อธิบาย: รอ Task ของฝ่ายเครื่องดื่มให้เสร็จ โดยไม่บล็อก Event Loop
    await task_bar

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
