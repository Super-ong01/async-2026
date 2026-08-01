# foodcourt_04_wait_for.py

# อธิบาย: นำเข้าโมดูล asyncio สำหรับ Coroutine, Task, Event Loop และการทำงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import ctime
# อธิบาย: นำเข้าฟังก์ชัน send_order_to_kitchen จาก food_utils เพื่อส่งออเดอร์ไปยัง Food Court API
from food_utils import send_order_to_kitchen


# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # อธิบาย: กำหนดรหัสนักศึกษาที่จะใช้ส่งไปพร้อมคำสั่งในตัวอย่างนี้
    MY_STUDENT_ID = "6710301004"

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        f"{ctime()} | --- [Task 4] Practice using wait_for to handle timeouts ---"
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )

    # อธิบาย: เริ่มบล็อก try สำหรับคำสั่งที่อาจเกิด Exception
    try:
        # 1. Order a steak (takes 4s) but enforce a strict timeout of 2.0 seconds.
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
        print(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"{ctime()} | [System] Order sent. "
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"Monitoring 2.0s timeout limit..."
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

        # อธิบาย: ใช้ wait_for() ครอบ Coroutine เพื่อบังคับ Timeout ตามเวลาที่กำหนด
        result = await asyncio.wait_for(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            send_order_to_kitchen(
                # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
                MY_STUDENT_ID,
                # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
                "steak",
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                "T-Bone Steak"
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการภายในคำสั่งหลายบรรทัด
            ),
            # อธิบาย: กำหนดจำนวนวินาทีสูงสุดก่อนเกิด TimeoutError
            timeout=2.0
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
        print(f"{ctime()} | Success: {result}")

    # อธิบาย: ดักจับ TimeoutError เมื่อคำสั่งใช้เวลานานเกินเวลาที่กำหนด
    except asyncio.TimeoutError:
        # 2. Catch the TimeoutError exception when the execution exceeds the limit.
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
        print(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"{ctime()} | Timeout occurred: "
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"Steak took too long! Leaving the food court now."
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )


# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ ก่อนเรียกฟังก์ชันหลัก
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
