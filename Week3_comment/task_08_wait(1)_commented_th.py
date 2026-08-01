# Objective: Implement complex processing workflows based on task fulfillment conditions.
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime เพื่อใช้แสดงเวลาปัจจุบันหรือวัดเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศ Coroutine สำหรับจำลองการตรวจสอบการตอบสนองของเซิร์ฟเวอร์ โดยรับพารามิเตอร์ server_name, delay
async def network_probe(server_name, delay):
    # อธิบาย: พัก Coroutine เป็นเวลา delay วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
    await asyncio.sleep(delay)
    # อธิบาย: คืนค่าข้อความผลลัพธ์จาก Coroutine ให้กับ Task หรือผู้ที่ await
    return f"Ping successful: {server_name}"

# อธิบาย: ประกาศ Coroutine หลักของโปรแกรม
async def main():
    # 
    # อธิบาย: สร้าง Set สำหรับเก็บ Task หลายตัวที่ต้องการให้ทำงานพร้อมกัน
    tasks = {
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(network_probe("Primary-Server", 2.0)),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(network_probe("Backup-Server-1", 0.5)),
        # อธิบาย: สร้าง Task จาก Coroutine เพื่อให้ Event Loop นำไปจัดตารางการทำงาน
        asyncio.create_task(network_probe("Backup-Server-2", 1.0))
    # อธิบาย: ปิด Dictionary ที่ใช้เป็นข้อมูลตอบกลับ
    }

    # 
    # อธิบาย: ใช้ asyncio.wait() รอ Task ตามเงื่อนไขที่กำหนด และแยกผลเป็น Set: done กับ pending
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # อธิบาย: นับจำนวน Task ที่เสร็จแล้วจากผลของ asyncio.wait()
    print(f"{ctime()} Count of Tasks Done: {len(done)}")       # 
    # อธิบาย: นับจำนวน Task ที่ยังไม่เสร็จและอยู่ในสถานะ Pending
    print(f"{ctime()} Count of Tasks Pending: {len(pending)}") # 

    # อธิบาย: วนลูป Task ที่เสร็จแล้วเพื่ออ่านผลลัพธ์
    for finished_task in done:
        # อธิบาย: อ่านค่าผลลัพธ์จาก Task ที่เสร็จแล้วภายใน Callback และแสดงผล
        print(f"{ctime()} Fastest Task Result: {finished_task.result()}")

    # 
    # อธิบาย: วนลูปผ่าน Task ที่ยัง Pending เพื่อยกเลิกงานที่ไม่จำเป็นแล้ว
    for ongoing_task in pending:
        # อธิบาย: ส่งคำขอยกเลิก Task ที่ยังทำงานค้างอยู่
        ongoing_task.cancel()

# อธิบาย: สร้าง Event Loop รัน main() จนเสร็จ แล้วปิด Event Loop ให้อัตโนมัติ
asyncio.run(main())
