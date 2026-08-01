# Program 2: Coroutine Object
# Concept: Calling an async def function returns a coroutine object, it doesn't run the function yet.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าโมดูล inspect เพื่อใช้ตรวจสอบชนิดและคุณสมบัติของฟังก์ชันหรือ Coroutine
import inspect
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine Function สำหรับจำลองการให้บริการลูกค้า โดยรับพารามิเตอร์ name
async def serve_customer(name):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Cooking for {name}...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} -> Served {name}!")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: แสดงข้อความก่อนเรียก async function เพื่อสังเกตลำดับการทำงาน
    print(f"{ctime()} -> Calling serve_customer('A')...")
    # อธิบาย: เรียก async function เพื่อสร้าง Coroutine Object ของลูกค้า A แต่ยังไม่ได้เริ่มรัน Coroutine
    coro = serve_customer("A")
    # อธิบาย: แสดง Coroutine Object ที่ถูกสร้างขึ้น เพื่อให้เห็นว่ายังเป็นออบเจ็กต์ที่รอการรัน
    print(f"{ctime()} -> Coroutine object created: {coro}")
    # อธิบาย: แสดงข้อความอธิบายว่าการสร้าง Coroutine Object อย่างเดียวยังไม่ได้รันโค้ดภายใน
    print(f"{ctime()} -> Note that 'Cooking for A...' was not printed yet because it has not run.")

    # อธิบาย: แสดงชนิดของตัวแปร coro เพื่อยืนยันว่าเมื่อเรียก async function แล้วจะได้ Coroutine Object
    print(f"{ctime()} -> type(coro): {type(coro)}")
    # อธิบาย: ตรวจว่าออบเจ็กต์ในตัวแปร coro เป็น Coroutine Object หรือไม่ แล้วแสดงผล
    print(f"{ctime()} -> inspect.iscoroutine(coro): {inspect.iscoroutine(coro)}")
