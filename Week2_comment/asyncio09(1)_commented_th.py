# Program 9: Dynamic Task List
# Concept: Managing multiple tasks in a list and awaiting them.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ time, ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import time, ctime

# อธิบาย: ประกาศ Coroutine Function สำหรับจำลองการให้บริการลูกค้า โดยรับพารามิเตอร์ name
async def serve_customer(name):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Handling customer {name}")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Done customer {name}")

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start_time เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start_time = time()
    # อธิบาย: สร้างลิสต์รายชื่อลูกค้าที่โปรแกรมจะนำมาจำลองการให้บริการ
    customers = ["A", "B", "C", "D"]
    # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บออบเจ็กต์ asyncio Task ที่สร้างขึ้น
    task_list = []

    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for name in customers:
        # อธิบาย: สร้าง asyncio Task ชื่อ t จาก serve_customer(name) และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
        t = asyncio.create_task(serve_customer(name))
        # อธิบาย: เพิ่ม Task ที่เพิ่งสร้างเข้าไปใน task_list เพื่อเก็บไว้รอผลภายหลัง
        task_list.append(t)

    # อธิบาย: วนลูปผ่าน Task ทุกตัวที่เก็บไว้ใน task_list
    for t in task_list:
        # อธิบาย: รอ Task ปัจจุบันให้ทำงานเสร็จ ก่อนวนไป Task ถัดไป
        await t

    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"Served all {len(customers)} customers in {time() - start_time:.2f} seconds.")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
