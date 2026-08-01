# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ time, ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import time, ctime

# 1. ขั้นตอนต้อนรับหน้าร้าน ทำแบบ Synchronous เรียงทีละคน
# อธิบาย: ประกาศ Coroutine Function สำหรับต้อนรับลูกค้า โดยรับพารามิเตอร์ customer
async def greet_diners(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# 2. กระบวนการส่วนตัวของลูกค้าแต่ละคน ที่จะถูกนำไปรันแยกใน Task ของตัวเอง
# อธิบาย: ประกาศ Coroutine Function สำหรับขั้นตอนบริการส่วนตัวของลูกค้าแต่ละคน โดยรับพารามิเตอร์ customer
async def customer_private_workflow(customer):
    # Take Order
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Taking Order ...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Taking Order ...Done!")

    # Do Cooking
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Cooking Spaghetti ...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Cooking Spaghetti ...Done!")

    # Manage Bar
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Manage Bar for Drink ...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] Manage Bar for Drink ...Done!")
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Task-{customer}] All served!\n")

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start_time เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start_time = time()
    # อธิบาย: สร้างลิสต์รายชื่อลูกค้าที่โปรแกรมจะนำมาจำลองการให้บริการ
    customers = ['A', 'B', 'C']

    # ----------------------------------------------------
    # PHASE 1: Greet diners sequentially
    # ----------------------------------------------------
    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for customer in customers:
        # อธิบาย: รอการต้อนรับลูกค้าคนปัจจุบันให้เสร็จก่อน จึงเริ่มต้อนรับลูกค้าคนถัดไป จึงยังเป็น Sequential
        await greet_diners(customer)

    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"\n{ctime()} --- All customers greeted. Scheduling independent Async Tasks! ---\n")

    # ----------------------------------------------------
    # PHASE 2: Spawn tasks for concurrent phases
    # ----------------------------------------------------
    # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บออบเจ็กต์ asyncio Task ที่สร้างขึ้น
    tasks = []
    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for customer in customers:
        # อธิบาย: สร้าง asyncio Task ชื่อ task จาก customer_private_workflow(customer) และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
        task = asyncio.create_task(customer_private_workflow(customer))
        # อธิบาย: เพิ่ม Task ของลูกค้าคนนี้เข้าไปในลิสต์ tasks
        tasks.append(task)

    # อธิบาย: รอ Task ทุกตัวในลิสต์ tasks ให้เสร็จทั้งหมดพร้อมกัน โดย * ใช้กระจายสมาชิกในลิสต์เป็นอาร์กิวเมนต์
    await asyncio.gather(*tasks)

    # อธิบาย: คำนวณระยะเวลารวม โดยนำเวลาปัจจุบันลบด้วยเวลาเริ่มต้น
    duration = time() - start_time
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Finished Cooking in {duration:0.2f} seconds.")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
