# อธิบาย: นำเข้าโมดูล multiprocessing เพื่อสร้างหลาย Process ที่สามารถทำงานแยกกันได้
import multiprocessing
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ sleep, ctime, time สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import sleep, ctime, time

# 1. ขั้นตอนต้อนรับหน้าร้าน ทำแบบ Synchronous เรียงทีละคน
# อธิบาย: ประกาศฟังก์ชันปกติสำหรับต้อนรับลูกค้า โดยรับพารามิเตอร์ customer
def greet_diners(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# 2. กระบวนการย่อยของลูกค้าแต่ละคน ที่รอบนี้จะถูกนำไปรันแยกในโปรเซสของตัวเอง
# อธิบาย: ประกาศฟังก์ชันสำหรับรวมขั้นตอนบริการของลูกค้าแต่ละคน โดยรับพารามิเตอร์ customer
def customer_private_workflow(customer):
    # ในแต่ละ Process จะทำงาน 3 Tasks นี้
    # อธิบาย: อ่าน Process ID (PID) ของ Process ที่กำลังทำงานอยู่ เพื่อใช้แสดงว่าแต่ละลูกค้ารันอยู่คนละ Process
    pid = multiprocessing.current_process().pid
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Taking Order ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Taking Order ...Done!")

    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Cooking Spaghetti ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Cooking Spaghetti ...Done!")

    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Manage Bar for Drink ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] Manage Bar for Drink ...Done!")
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()}  [Process-{customer} (PID: {pid})] All served!\n")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: สร้างลิสต์รายชื่อลูกค้าที่โปรแกรมจะนำมาจำลองการให้บริการ
    customers = ['A', 'B', 'C']
    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start_time เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start_time = time()

    # ----------------------------------------------------
    # PHASE 1: Greet ลูกค้าทีละคนแบบ Synchronous ใน Main Process
    # ----------------------------------------------------
    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for customer in customers:
        # อธิบาย: เรียกฟังก์ชันต้อนรับลูกค้าคนปัจจุบันและรอจนฟังก์ชันทำเสร็จ
        greet_diners(customer)

    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"\n{ctime()} --- All customers greeted. FORKING into independent Processes (Branch)! ---\n")

    # ----------------------------------------------------
    # PHASE 2: แตกโปรเซส (เปิดสาขาใหม่แยกขาดจากกันตามคอร์ซีพียู)
    # ----------------------------------------------------
    # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บ Process ของลูกค้าแต่ละคน
    processes = []
    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for customer in customers:
        # เปลี่ยนจาก threading.Thread เป็น multiprocessing.Process
        # อธิบาย: สร้าง Process ใหม่ โดยกำหนดฟังก์ชันที่จะให้ Process นั้นทำงานและส่ง customer เป็นอาร์กิวเมนต์
        p = multiprocessing.Process(target=customer_private_workflow, args=(customer,))
        # อธิบาย: เก็บออบเจ็กต์ Process ที่สร้างไว้ในลิสต์ เพื่อใช้ start หรือ join ภายหลัง
        processes.append(p)
        # อธิบาย: สั่งให้ Process นี้เริ่มทำงานจริง โดยระบบปฏิบัติการจะสร้าง Process แยกจาก Main Process
        p.start() # OS จะทำการโคลนทุกอย่างแล้วเตะไปรันบน CPU คอร์อื่น ๆ ขนานกันทันที

    # รอให้ทุกโปรเซส (ทุกสาขา) ทำงานของตัวเองเสร็จสิ้นทั้งหมด
    # อธิบาย: วนลูปผ่าน Process ทุกตัวที่เก็บไว้ในลิสต์ processes
    for p in processes:
        # อธิบาย: ให้ Main Process รอจนกว่า Process นี้จะทำงานเสร็จ ก่อนดำเนินขั้นตอนถัดไป
        p.join()

    # อธิบาย: คำนวณระยะเวลารวม โดยนำเวลาปัจจุบันลบด้วยเวลาเริ่มต้น
    duration = time() - start_time
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:0.2f} seconds.")
