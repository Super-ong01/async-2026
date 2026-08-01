# Program 10: Retreiving Task Return Value
# Concept: Accessing the return value of completed tasks.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task และ Event Loop สำหรับงานแบบ Asynchronous
import asyncio

# อธิบาย: ประกาศ Coroutine Function สำหรับคำนวณยอดบิลของลูกค้า โดยรับพารามิเตอร์ customer, base_price
async def calculate_bill(customer, base_price):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"Calculating receipt for Customer {customer}...")
    # อธิบาย: พัก Coroutine ประมาณ 1 วินาทีแบบไม่บล็อก Event Loop และเปิดโอกาสให้ Task อื่นทำงานระหว่างรอ
    await asyncio.sleep(1)
    # อธิบาย: คำนวณราคาสุทธิ โดยเพิ่ม 7% จากราคาพื้นฐาน แล้วเก็บไว้ใน final_price
    final_price = base_price * 1.07
    # อธิบาย: คืนค่าราคาสุทธิจาก Coroutine ให้ Task หรือผู้ที่ await รับค่าไปใช้ต่อ
    return final_price

# อธิบาย: ประกาศ Coroutine Function หลักของโปรแกรม ซึ่งจะถูกขับเคลื่อนด้วย Event Loop
async def main():
    # อธิบาย: สร้าง asyncio Task ชื่อ task_a จาก calculate_bill("A", 100) และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_a = asyncio.create_task(calculate_bill("A", 100))
    # อธิบาย: สร้าง asyncio Task ชื่อ task_b จาก calculate_bill("B", 200) และลงทะเบียนกับ Event Loop เพื่อให้เริ่มทำงานแบบ Concurrent
    task_b = asyncio.create_task(calculate_bill("B", 200))

    # อธิบาย: รอ task_a ให้เสร็จและรับค่าที่ Coroutine return กลับมาเก็บใน result_a
    result_a = await task_a
    # อธิบาย: รอ task_b ให้เสร็จและรับค่าที่ Coroutine return กลับมาเก็บใน result_b
    result_b = await task_b

    # result_b = task_b.result()

    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"\nFinal Bill A: {result_a:.2f}")
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"Final Bill B: {result_b:.2f}")
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"Combined Total Revenue: {result_a + result_b:.2f}")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้าง Event Loop ชั่วคราว รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
    asyncio.run(main())
