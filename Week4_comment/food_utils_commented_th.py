# food_utils.py
# อธิบาย: นำเข้า httpx เพื่อส่ง HTTP Request แบบ Asynchronous โดยไม่บล็อก Event Loop
import httpx

# อธิบาย: ประกาศ Coroutine สำหรับส่งออเดอร์ไปยัง Kitchen API ผ่าน HTTP
async def send_order_to_kitchen(student_id: str, shop_name: str, menu_name: str) -> dict:
    # อธิบาย: ประกอบ URL ของ Endpoint โดยแทรกค่าตัวแปรที่เกี่ยวข้องลงใน path
    url = f"http://172.16.2.117:8088/order/{shop_name}"
    # อธิบาย: สร้าง Dictionary สำหรับใช้เป็น JSON Request Body ที่จะส่งไปยัง API
    payload = {"student_id": student_id, "menu_name": menu_name}
    # อธิบาย: เริ่มบล็อก try สำหรับคำสั่งที่อาจเกิด Exception
    try:
        # อธิบาย: สร้าง Async HTTP Client ภายใน Context Manager เพื่อเปิด/ปิดทรัพยากรให้อัตโนมัติ
        async with httpx.AsyncClient() as client:
            # อธิบาย: ส่ง HTTP POST Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            response = await client.post(url, json=payload, timeout=10.0)
            # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจว่าจะทำคำสั่งในบล็อกนี้หรือไม่
            if response.status_code == 200:
                # อธิบาย: แปลง JSON Response เป็น Python Dictionary แล้วคืนค่าให้ผู้เรียก
                return response.json()
            # อธิบาย: ถ้าเงื่อนไขก่อนหน้าไม่เป็นจริง ให้ทำงานในส่วน else
            else:
                # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
                return {"status": "ERROR", "detail": f"HTTP Error {response.status_code}"}
    # อธิบาย: ดักจับ Exception ทั่วไปและเก็บรายละเอียดข้อผิดพลาดไว้ในตัวแปร
    except Exception as e:
        # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
        return {"status": "ERROR", "detail": f"Connection failed: {e}"}
