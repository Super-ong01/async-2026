# Program 5: Sequential Execution (The Wrong Way)
# Concept: Awaiting coroutines sequentially is still synchronous.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ time, ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import time, ctime

# อธิบาย: ประกาศ Coroutine Function สำหรับจำลองการให้บริการลูกค้า โดยรับพารามิเตอร์ name
async def serve_customer(name):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Cooking for {name}...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Served {name}!")

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start = time()
    # อธิบาย: เรียกและรอ Coroutine ของลูกค้า A ให้เสร็จก่อน จึงไปทำบรรทัดถัดไป ทำให้ส่วนนี้ทำงานแบบเรียงลำดับ
    await serve_customer("A")
    # อธิบาย: เรียกและรอ Coroutine ของลูกค้า B ให้เสร็จก่อน จึงไปทำบรรทัดถัดไป ทำให้ส่วนนี้ทำงานแบบเรียงลำดับ
    await serve_customer("B")

    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"Total Time: {time() - start:.2f} seconds")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
