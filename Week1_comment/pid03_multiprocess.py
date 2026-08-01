# อธิบาย: นำเข้าฟังก์ชันเกี่ยวกับเวลาจากโมดูล time ได้แก่ sleep, ctime, time เพื่อใช้หน่วงเวลา แสดงเวลา หรือวัดเวลา
from time import sleep, ctime, time
# อธิบาย: นำเข้าโมดูล multiprocessing เพื่อสร้างหลาย Process ให้ทำงานแยกจากกัน
import multiprocessing
# อธิบาย: นำเข้าโมดูล os เพื่อเรียกข้อมูลของระบบปฏิบัติการ เช่น Process ID (PID)
import os
# อธิบาย: นำเข้าโมดูล threading เพื่อสร้างและจัดการ Thread ภายใน Process เดียว
import threading

# อธิบาย: หมายเหตุเดิมของโค้ด: ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คนแบบซิงโครนัส
# ฟังก์ชันจำลองการทำกาแฟให้ลูกค้า 1 คนแบบซิงโครนัส
# อธิบาย: ประกาศฟังก์ชันชื่อ make_coffee รับพารามิเตอร์ customer_name สำหรับรวมขั้นตอนการทำงานไว้เป็นชุดเดียว
def make_coffee(customer_name):
    # อธิบาย: อ่าน Process ID (PID) ของ Process ที่กำลังรันโค้ดบรรทัดนี้
    pid = os.getpid()
    # อธิบาย: อ่าน Native Thread ID ของ Thread ปัจจุบันจากระบบปฏิบัติการ
    thread_id = threading.current_thread().native_id
    # อธิบาย: อ่านชื่อของ Thread ปัจจุบัน เพื่อใช้แสดงว่าโค้ดกำลังทำงานอยู่บน Thread ใด
    thread_name = threading.current_thread().name

    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] กำลังชงกาแฟให้ลูกค้า {customer_name}...")
    # อธิบาย: หยุดการทำงานของ Thread ปัจจุบันเป็นเวลา 5 วินาที เพื่อจำลองช่วงเวลาที่ต้องรอ
    sleep(5)
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | [PID: {pid}] [TID: {thread_id}] [Thread Name: {thread_name}] ลูกค้า {customer_name}: ได้รับกาแฟแล้ว!")

# อธิบาย: ประกาศฟังก์ชันชื่อ main รับพารามิเตอร์ ไม่มี สำหรับรวมขั้นตอนการทำงานไว้เป็นชุดเดียว
def main():
    # อธิบาย: สร้างรายการคิวลูกค้า A, B, C เพื่อใช้วนทำงานกับลูกค้าแต่ละคน
    queue = ['A', 'B', 'C']
    # อธิบาย: เก็บ Process ID ของ Process หลักไว้ในตัวแปร main_pid
    main_pid = os.getpid()
    # อธิบาย: อ่าน Native Thread ID ของ Main Thread แล้วเก็บไว้ในตัวแปร main_tid
    main_tid = threading.current_thread().native_id

    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] เริ่มต้นการทำงานของร้านกาแฟ...")
    # อธิบาย: บันทึกเวลาปัจจุบันก่อนเริ่มงาน เพื่อใช้คำนวณระยะเวลาทำงานทั้งหมดภายหลัง
    start_time = time()

    # อธิบาย: สร้างลิสต์ว่างสำหรับเก็บออบเจ็กต์ Process ที่สร้างขึ้น
    processes = []
    # อธิบาย: วนลูปนำสมาชิกแต่ละตัวจาก queue มาเก็บในตัวแปร customer แล้วทำคำสั่งภายในบล็อกทีละรอบ
    for customer in queue:
        # อธิบาย: สร้าง Process ใหม่เพื่อรันงานแยกจาก Process หลัก โดยแต่ละ Process มีหน่วยความจำและ Python interpreter ของตนเอง
        p = multiprocessing.Process(target=make_coffee, args=(customer,))
        # อธิบาย: เพิ่ม Process ที่สร้างแล้วเข้าไปในลิสต์ processes เพื่อจัดการรวมกันภายหลัง
        processes.append(p)
        # อธิบาย: สั่งให้ Process นี้เริ่มทำงานจริง โดยระบบปฏิบัติการสร้าง Process ลูกขึ้นมา
        p.start()

    # อธิบาย: หมายเหตุเดิมของโค้ด: Wait for all processes to complete
    # Wait for all processes to complete
    # อธิบาย: วนลูปนำสมาชิกแต่ละตัวจาก processes มาเก็บในตัวแปร p แล้วทำคำสั่งภายในบล็อกทีละรอบ
    for p in processes:
        # อธิบาย: ให้ Process หลักรอจนกว่า Process ลูกตัวนี้จะทำงานเสร็จ
        p.join()

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมด โดยนำเวลาปัจจุบันลบด้วยเวลาเริ่มต้น
    duration = time() - start_time
    # อธิบาย: แสดงข้อความสถานะและเวลาปัจจุบันทางหน้าจอ เพื่อให้เห็นลำดับและช่วงเวลาการทำงาน
    print(f"{ctime()} | [Main PID: {main_pid}] [Main TID: {main_tid}] ร้านกาแฟปิดทำการแล้ว! ใช้เวลาในการทำงานทั้งหมด: {duration:.2f} วินาที") 

# อธิบาย: ตรวจว่าไฟล์นี้ถูกเรียกใช้งานโดยตรงหรือไม่ เพื่อให้โค้ดด้านล่างรันเฉพาะตอนเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    # อธิบาย: บันทึกเวลาปัจจุบันก่อนเริ่มงาน เพื่อใช้คำนวณระยะเวลาทำงานทั้งหมดภายหลัง
    start_time = time()
    # อธิบาย: เรียกฟังก์ชัน main() เพื่อเริ่มลำดับการทำงานหลักของโปรแกรม
    main()
