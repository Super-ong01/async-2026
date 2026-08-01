# foodcourt_02_gather.py
# foodcourt_02_gather.py
# อธิบาย: นำเข้าโมดูล asyncio สำหรับ Coroutine, Task, Event Loop และการทำงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import time, ctime
# อธิบาย: นำเข้าฟังก์ชัน send_order_to_kitchen จาก food_utils เพื่อส่งออเดอร์ไปยัง Food Court API
from food_utils import send_order_to_kitchen

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: กำหนดรหัสนักศึกษาที่จะใช้ส่งไปพร้อมคำสั่งในตัวอย่างนี้
    MY_STUDENT_ID = "6710301004"

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณเวลารวม
    start_time = time()

    # 1. Spawn 3 concurrent tasks to order food from different shops.
    # อธิบาย: สร้าง asyncio Task แล้วเก็บไว้ในตัวแปร t1 เพื่อให้ Coroutine เริ่มทำงานแบบ Concurrent
    t1 = asyncio.create_task(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        send_order_to_kitchen(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )
    # อธิบาย: สร้าง asyncio Task แล้วเก็บไว้ในตัวแปร t2 เพื่อให้ Coroutine เริ่มทำงานแบบ Concurrent
    t2 = asyncio.create_task(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        send_order_to_kitchen(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            MY_STUDENT_ID, "noodle", "Wonton Noodles"
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )
    # อธิบาย: สร้าง asyncio Task แล้วเก็บไว้ในตัวแปร t3 เพื่อให้ Coroutine เริ่มทำงานแบบ Concurrent
    t3 = asyncio.create_task(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        send_order_to_kitchen(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            MY_STUDENT_ID, "steak", "Sizzling Steak"
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )

    # 2. Use asyncio.gather to wait for all dishes to be prepared concurrently.
    # อธิบาย: รอ Task ทุกตัวให้เสร็จด้วย gather() และเก็บผลลัพธ์เรียงตามลำดับที่ส่งเข้าไป
    results = await asyncio.gather(t1, t2, t3)

    # อธิบาย: วนลูปผ่านผลลัพธ์ของอาหารแต่ละจานที่ gather() คืนมา
    for dish in results:
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
        print(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"{ctime()} | [Pickup] Shop: {dish['shop']} | "
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"Menu: {dish['menu']} is ready!"
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        f"{ctime()} | Total time: {time() - start_time:.2f} "
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "seconds (Equals to the slowest dish)."
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )


# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ ก่อนเรียกฟังก์ชันหลัก
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
