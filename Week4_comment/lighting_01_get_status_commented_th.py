# lab_lighting_sync.py

# อธิบาย: นำเข้า requests สำหรับส่ง HTTP Request แบบ Synchronous/Blocking
import requests
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import time, ctime

# อธิบาย: กำหนด Base URL ของ API Server ที่โปรแกรมจะเชื่อมต่อ
BASE_URL = "http://172.16.2.117:8088"
# อธิบาย: กำหนดรหัสนักศึกษาที่ใช้ระบุชุดข้อมูล/อุปกรณ์ของผู้ใช้ใน API
STUDENT_ID = "6710301004"

# อธิบาย: สร้างลิสต์รหัสหลอดไฟทั้ง 4 ดวงที่โปรแกรมจะควบคุม
LIGHTS = ["light_1", "light_2", "light_3", "light_4"]


# อธิบาย: ประกาศฟังก์ชัน Synchronous สำหรับอ่านสถานะไฟทั้งหมด
def get_all_lights_status(student_id: str) -> dict:
    """GET สถานะไฟทั้งหมดของนักเรียน"""
    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights"
    # อธิบาย: ส่ง HTTP GET แบบ Synchronous ซึ่งจะบล็อกรอจน Server ตอบกลับ
    response = requests.get(url)
    # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
    return response.json()


# อธิบาย: ประกาศฟังก์ชัน Synchronous สำหรับสั่งเปิดหรือปิดไฟหนึ่งดวง
def set_light_status(student_id: str, light_id: str, status: str) -> dict:
    """POST สั่งเปิด/ปิดไฟดวงเดียว (จะบล็อครอจน hardware delay เสร็จ)"""
    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights/{light_id}"
    # อธิบาย: สร้าง Dictionary สำหรับใช้เป็น JSON Request Body ที่จะส่งไปยัง API
    payload = {"status": status}
    # อธิบาย: เริ่มบล็อก try สำหรับคำสั่งที่อาจเกิด Exception
    try:
        # อธิบาย: ส่ง HTTP POST แบบ Synchronous พร้อม JSON และรอ Response
        response = requests.post(url, json=payload, timeout=10.0)
        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจว่าจะทำคำสั่งในบล็อกนี้หรือไม่
        if response.status_code == 200:
            # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
            return response.json()
        # อธิบาย: ถ้าเงื่อนไขก่อนหน้าไม่เป็นจริง ให้ทำงานในส่วน else
        else:
            # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
            return {"status": "ERROR", "detail": f"HTTP Error {response.status_code}"}
    # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจากการเชื่อมต่อ HTTP ด้วย requests
    except requests.exceptions.RequestException as e:
        # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}


# อธิบาย: ประกาศฟังก์ชัน Synchronous สำหรับรีเซ็ตไฟทุกดวง
def reset_all_lights(student_id: str) -> dict:
    """DELETE รีเซ็ตไฟทั้งหมดเป็น OFF"""
    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"{BASE_URL}/api/{student_id}/lights/reset"
    # อธิบาย: ส่ง HTTP DELETE แบบ Synchronous เพื่อรีเซ็ตข้อมูล และรอ Response
    response = requests.delete(url)
    # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
    return response.json()


# อธิบาย: ประกาศฟังก์ชันหลักของโปรแกรม
def main():
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | --- Sync Version: Turning ON all 4 lights ---")

    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณเวลารวม
    start_time = time()

    # ทำงานทีละดวง เรียงตามลำดับ (sequential/blocking)
    # อธิบาย: วนลูปทีละรหัสไฟจากลิสต์ LIGHTS
    for light_id in LIGHTS:
        # อธิบาย: บันทึกเวลาเริ่มทำงานของไฟดวงนี้ เพื่อคำนวณเวลาที่ใช้รายดวง
        light_start = time()
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        result = set_light_status(STUDENT_ID, light_id, "ON")
        # อธิบาย: คำนวณเวลาที่ใช้กับไฟดวงนี้
        elapsed = time() - light_start
        # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
        print(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"{ctime()} | {light_id} -> {result.get('current_status', result)} "
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            f"(took {elapsed:.2f}s)"
        # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

    # อธิบาย: คำนวณเวลารวมทั้งหมดตั้งแต่เริ่มโปรแกรม
    total_time = time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | Total execution time: {total_time:.2f} seconds.")


# อธิบาย: ตรวจว่าไฟล์นี้ถูกสั่งรันโดยตรงหรือไม่ ก่อนเรียกฟังก์ชันหลัก
if __name__ == "__main__":
    # อธิบาย: เรียกฟังก์ชัน main() เพื่อเริ่มการทำงานของโปรแกรม
    main()
