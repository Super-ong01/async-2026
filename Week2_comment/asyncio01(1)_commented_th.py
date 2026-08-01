# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.
# อธิบาย: นำเข้าโมดูล inspect เพื่อใช้ตรวจสอบชนิดและคุณสมบัติของฟังก์ชันหรือ Coroutine
import inspect
# อธิบาย: นำเข้าฟังก์ชันจากโมดูล time ได้แก่ ctime สำหรับหน่วงเวลา ดูเวลา และวัดระยะเวลาการทำงาน
from time import ctime

# อธิบาย: ประกาศฟังก์ชันปกติสำหรับจำลองการทำสปาเกตตี โดยรับพารามิเตอร์ customer
def cook_spaghetti(customer):
    # อธิบาย: คืนค่าข้อความผลลัพธ์การทำสปาเกตตีให้กับผู้เรียกฟังก์ชัน
    return f"Spaghetti for {customer}"

# อธิบาย: ประกาศ Coroutine Function สำหรับจำลองการให้บริการลูกค้า โดยรับพารามิเตอร์ customer
async def serve_customer(customer):
    # อธิบาย: คืนค่าข้อความว่าบริการลูกค้าเสร็จแล้วจาก Coroutine นี้
    return f"Served customer {customer}"

# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ เพื่อให้โค้ดด้านในทำงานเฉพาะตอนรันไฟล์นี้
if __name__ == "__main__":
    # อธิบาย: แสดงชนิดของ cook_spaghetti เพื่อดูว่าฟังก์ชันปกติมีชนิดเป็น function
    print(f"{ctime()} -> type(cook_spaghetti): {type(cook_spaghetti)}")
    # อธิบาย: แสดงชนิดของ serve_customer; แม้ประกาศด้วย async def ตัวฟังก์ชันเองยังมีชนิดเป็น function
    print(f"{ctime()} -> type(serve_customer): {type(serve_customer)}")

    # อธิบาย: ตรวจว่า cook_spaghetti เป็น Coroutine Function หรือไม่ แล้วแสดงผล True/False
    print(f"{ctime()} -> inspect.iscoroutinefunction(cook_spaghetti): {inspect.iscoroutinefunction(cook_spaghetti)}")
    # อธิบาย: ตรวจว่า serve_customer เป็น Coroutine Function หรือไม่ แล้วแสดงผล True/False
    print(f"{ctime()} -> inspect.iscoroutinefunction(serve_customer): {inspect.iscoroutinefunction(serve_customer)}")
