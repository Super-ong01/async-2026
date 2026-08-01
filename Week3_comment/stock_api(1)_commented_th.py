# mock_stock_api.py
# อธิบาย: นำเข้า FastAPI เพื่อสร้าง Web API จำลองสำหรับให้โปรแกรมอื่นเรียกดูราคาหุ้น
from fastapi import FastAPI
# อธิบาย: นำเข้าโมดูล asyncio เพื่อใช้ Coroutine, Task, Event Loop, wait(), gather(), wait_for() และการยกเลิก Task
import asyncio

# อธิบาย: สร้างออบเจ็กต์แอป FastAPI และกำหนดชื่อของ Mock Stock API
app = FastAPI(title="Asyncio Week 3 Mock Stock API")

# อธิบาย: กำหนด Route แบบ GET ที่รับค่า server_name จาก URL เช่น /price/alpha
@app.get("/price/{server_name}")
# อธิบาย: ประกาศ Coroutine สำหรับตอบ API ราคาหุ้น โดยรับชื่อเซิร์ฟเวอร์จาก URL
async def get_stock_price(server_name: str):
    # อธิบาย: ข้อความ Docstring ใช้อธิบายวัตถุประสงค์และเงื่อนไขของฟังก์ชัน
    """ API จำลองราคาหุ้น โดยแต่ละสาขาจะมีความหน่วง (Latency) ไม่เท่ากัน """
    # อธิบาย: แปลงชื่อเซิร์ฟเวอร์เป็นตัวพิมพ์เล็ก เพื่อให้เปรียบเทียบชื่อได้โดยไม่สนตัวพิมพ์ใหญ่/เล็ก
    name_lower = server_name.lower()

    # อธิบาย: ตรวจว่าผู้ใช้เรียกเซิร์ฟเวอร์ Alpha หรือไม่
    if name_lower == "alpha":
        # อธิบาย: พัก Coroutine เป็นเวลา 3.0 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
        await asyncio.sleep(3.0)  # ช้าที่สุด
        # อธิบาย: กำหนดราคาหุ้นจำลองของเซิร์ฟเวอร์นี้
        price = 152.50
    # อธิบาย: ถ้าไม่ใช่ Alpha ให้ตรวจต่อว่าเป็นเซิร์ฟเวอร์ Beta หรือไม่
    elif name_lower == "beta":
        # อธิบาย: พัก Coroutine เป็นเวลา 0.8 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
        await asyncio.sleep(0.8)  # เร็วที่สุด!
        # อธิบาย: กำหนดราคาหุ้นจำลองของเซิร์ฟเวอร์นี้
        price = 149.80
    # อธิบาย: ถ้าไม่ใช่ Alpha/Beta ให้ตรวจต่อว่าเป็นเซิร์ฟเวอร์ Gamma หรือไม่
    elif name_lower == "gamma":
        # อธิบาย: พัก Coroutine เป็นเวลา 1.5 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
        await asyncio.sleep(1.5)  # ปานกลาง
        # อธิบาย: กำหนดราคาหุ้นจำลองของเซิร์ฟเวอร์นี้
        price = 150.20
    # อธิบาย: กรณีที่ไม่ตรงกับเงื่อนไขก่อนหน้า ให้ทำงานในทางเลือกเริ่มต้น
    else:
        # อธิบาย: พัก Coroutine เป็นเวลา 0.1 วินาทีแบบไม่บล็อก Event Loop ทำให้ Task อื่นมีโอกาสทำงานระหว่างรอ
        await asyncio.sleep(0.1)
        # อธิบาย: กำหนดราคาหุ้นจำลองของเซิร์ฟเวอร์นี้
        price = 100.00

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response ของ API
    return {
        # อธิบาย: กำหนดฟิลด์ server ใน JSON ให้เป็นชื่อเซิร์ฟเวอร์ที่ผู้ใช้ร้องขอ
        "server": server_name,
        # อธิบาย: กำหนดฟิลด์ price_usd ใน JSON ให้เป็นราคาหุ้นที่จำลองไว้
        "price_usd": price,
        # อธิบาย: กำหนดฟิลด์ status ใน JSON เพื่อบอกว่างานสำเร็จ
        "status": "success"
    # อธิบาย: ปิด Dictionary ที่ใช้เป็นข้อมูลตอบกลับ
    }
# pip install fastapi uvicorn httpx
# วิธีรันเซิร์ฟเวอร์: uvicorn stock_api:app --reload --port 8088
