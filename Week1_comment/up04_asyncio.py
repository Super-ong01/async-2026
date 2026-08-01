# อธิบาย: นำเข้าฟังก์ชันเกี่ยวกับเวลาจากโมดูล time ได้แก่ ctime, time เพื่อใช้หน่วงเวลา แสดงเวลา หรือวัดเวลา
from time import ctime, time
# อธิบาย: นำเข้าโมดูล asyncio สำหรับเขียนโปรแกรมแบบ Asynchronous ด้วย Event Loop และ Task
import asyncio

# อธิบาย: ประกาศฟังก์ชันแบบ async ชื่อ update_cup_number รับพารามิเตอร์ customer_name และสามารถใช้ await ภายในฟังก์ชันได้
async def update_cup_number(customer_name):
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    # อธิบาย: พัก Task นี้เป็นเวลา 1 วินาทีแบบไม่บล็อก Thread ทำให้ Event Loop สามารถไปทำ Task อื่นระหว่างรอได้
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

# อธิบาย: ประกาศฟังก์ชันแบบ async ชื่อ make_coffee รับพารามิเตอร์ customer_name และสามารถใช้ await ภายในฟังก์ชันได้
async def make_coffee(customer_name):
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | Making coffee for {customer_name}...")
    # อธิบาย: พัก Task นี้เป็นเวลา 1 วินาทีแบบไม่บล็อก Thread ทำให้ Event Loop สามารถไปทำ Task อื่นระหว่างรอได้
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | Coffee ready for {customer_name}!")

    # อธิบาย: รอ coroutine อัปเดต LCD ของลูกค้าคนนี้ให้เสร็จ โดยยังเปิดโอกาสให้ Event Loop สลับไปทำ Task อื่นได้
    await update_cup_number(customer_name)

# อธิบาย: ประกาศฟังก์ชันแบบ async ชื่อ main รับพารามิเตอร์ ไม่มี และสามารถใช้ await ภายในฟังก์ชันได้
async def main():
    # อธิบาย: สร้างรายการคิวลูกค้า A, B, C เพื่อใช้วนทำงานกับลูกค้าแต่ละคน
    queue = ['A', 'B', 'C']

    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | === Asyncio Coffee Machine ===")
    # อธิบาย: บันทึกเวลาปัจจุบันก่อนเริ่มงาน เพื่อใช้คำนวณระยะเวลาทำงานทั้งหมดภายหลัง
    start_time = time()

    # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บ asyncio Task ที่สร้างขึ้น
    tasks = []

    # อธิบาย: วนลูปนำสมาชิกแต่ละตัวจาก queue มาเก็บในตัวแปร customer แล้วทำคำสั่งภายในบล็อกทีละรอบ
    for customer in queue:
        # อธิบาย: สร้าง asyncio Task จาก coroutine เพื่อให้ Event Loop สามารถจัดตารางให้รันแบบ concurrent ได้
        task = asyncio.create_task(make_coffee(customer))
        # อธิบาย: เพิ่ม Task ที่สร้างแล้วเข้าไปในลิสต์ tasks เพื่อรอทุก Task พร้อมกันภายหลัง
        tasks.append(task)

    # อธิบาย: รอให้ Task ทุกตัวในลิสต์ tasks ทำงานเสร็จ โดย Task เหล่านั้นสามารถสลับกันทำงานระหว่างจุด await ได้
    await asyncio.gather(*tasks)

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมด โดยนำเวลาปัจจุบันลบด้วยเวลาเริ่มต้น
    duration = time() - start_time
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | Total time: {duration:0.2f} seconds")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกเรียกใช้งานโดยตรงหรือไม่ เพื่อให้โค้ดด้านล่างรันเฉพาะตอนเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    # อธิบาย: สร้างและเปิด Event Loop แล้วรัน coroutine main() จนทำงานเสร็จ จากนั้นปิด Event Loop
    asyncio.run(main())
