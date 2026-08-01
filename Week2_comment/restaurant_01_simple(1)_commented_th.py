# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ sleep, ctime, time สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import sleep, ctime, time

# Greeting synchronous
# อธิบาย: ประกาศฟังก์ชันปกติสำหรับต้อนรับลูกค้า โดยรับพารามิเตอร์ customer
def greet_diners(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# Take Order
# อธิบาย: ประกาศฟังก์ชันปกติสำหรับรับออเดอร์จากลูกค้า โดยรับพารามิเตอร์ customer
def take_orders(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Taking Order for Customer-{customer} ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Taking Order for Customer-{customer} ...Done!")

# Do Cooking
# อธิบาย: ประกาศฟังก์ชันปกติสำหรับจำลองขั้นตอนทำอาหาร โดยรับพารามิเตอร์ customer
def do_cooking(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Cooking for Customer-{customer} ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Cooking for Customer-{customer} ...Done!")

# Do Cooking
# อธิบาย: ประกาศฟังก์ชันปกติสำหรับจำลองงานเครื่องดื่มหรือ Mini Bar โดยรับพารามิเตอร์ customer
def mini_bar(customer):
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Mini Bar for Customer-{customer} ...")
    # อธิบาย: หยุดการทำงานของ Thread/Process ปัจจุบันประมาณ 1 วินาทีแบบ Blocking เพื่อจำลองเวลาที่ใช้ทำงาน
    sleep(1)
    # อธิบาย: แสดงข้อความสถานะการทำงานและข้อมูลที่เกี่ยวข้องออกทางหน้าจอ
    print(f"{ctime()} Mini Bar for Customer-{customer} ...Done!")

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # Begin of main thread
    # อธิบาย: สร้างลิสต์รายชื่อลูกค้าที่โปรแกรมจะนำมาจำลองการให้บริการ
    customers = ['A', 'B', 'C']

    # อธิบาย: บันทึกเวลาเริ่มต้นไว้ในตัวแปร start_time เพื่อนำไปคำนวณเวลาที่ใช้ทั้งหมด
    start_time = time()
    # Cooking for each customer
    # อธิบาย: วนลูปทีละคนตามรายชื่อลูกค้า เพื่อสร้างหรือเรียกขั้นตอนการทำงานสำหรับลูกค้าแต่ละคน
    for customer in customers:
        # อธิบาย: เรียกฟังก์ชันต้อนรับลูกค้าคนปัจจุบันและรอจนฟังก์ชันทำเสร็จ
        greet_diners(customer)
        # อธิบาย: เรียกฟังก์ชันรับออเดอร์ของลูกค้าคนปัจจุบัน
        take_orders(customer)
        # อธิบาย: เรียกฟังก์ชันทำอาหารของลูกค้าคนปัจจุบัน
        do_cooking(customer)
        # อธิบาย: เรียกฟังก์ชันจัดเตรียมเครื่องดื่มของลูกค้าคนปัจจุบัน
        mini_bar(customer)

    # อธิบาย: คำนวณระยะเวลารวม โดยนำเวลาปัจจุบันลบด้วยเวลาเริ่มต้น
    duration = time() - start_time
    # อธิบาย: แสดงผลเวลารวม/สถานะสิ้นสุดของโปรแกรมออกทางหน้าจอ
    print(f"{ctime()} Finished Cooking in {duration:0.2f} seconds.")
