# foodcourt_api.py
# อธิบาย: นำเข้า FastAPI สำหรับสร้าง Web API และ HTTPException สำหรับส่งข้อผิดพลาด HTTP
from fastapi import FastAPI, HTTPException
# อธิบาย: นำเข้าโมดูล asyncio สำหรับ Coroutine, Task, Event Loop และการทำงานแบบ Asynchronous
import asyncio
# อธิบาย: นำเข้า BaseModel จาก Pydantic เพื่อกำหนดโครงสร้างข้อมูล Request Body และตรวจสอบชนิดข้อมูล
from pydantic import BaseModel
# อธิบาย: นำเข้าฟังก์ชัน time/ctime เพื่อวัดเวลาการทำงานและแสดงเวลาปัจจุบัน
from time import ctime

# อธิบาย: สร้างแอปพลิเคชัน FastAPI และตั้งชื่อ API
app = FastAPI(title="🍳 Smart Food Court API")

# อธิบาย: ประกาศ Data Model สำหรับข้อมูลออเดอร์ที่รับจาก Request Body
class OrderModel(BaseModel):
    # อธิบาย: กำหนดฟิลด์ student_id ให้ต้องเป็นข้อความ
    student_id: str
    # อธิบาย: กำหนดฟิลด์ menu_name ให้ต้องเป็นข้อความ
    menu_name: str

# Mock cooking times for each shop (in seconds)
# อธิบาย: สร้าง Dictionary เก็บเวลาจำลองในการทำอาหารของแต่ละร้าน
KITCHEN_LATENCY = {
    # อธิบาย: กำหนดเวลาจำลองของร้านข้าวมันไก่ ซึ่งเป็นร้านที่เร็วที่สุด
    "hainanese_chicken": 0.8,  # Fast: chopped and served quickly
    # อธิบาย: กำหนดเวลาจำลองของร้านก๋วยเตี๋ยว
    "noodle": 1.5,             # Medium: boiling noodles and soup
    # อธิบาย: กำหนดเวลาจำลองของร้านสเต็ก ซึ่งใช้เวลานานที่สุด
    "steak": 4.0               # Slowest: grilling thick meat
# อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
}

# อธิบาย: กำหนด Endpoint แบบ POST สำหรับรับออเดอร์ โดย shop_name มาจาก URL
@app.post("/order/{shop_name}")
# อธิบาย: ประกาศ Coroutine สำหรับรับออเดอร์ ตรวจร้าน จำลองเวลาทำอาหาร และส่งผลลัพธ์กลับ
async def cook_food(shop_name: str, order: OrderModel):
    # อธิบาย: ตรวจว่าชื่อร้านมีอยู่ในรายการร้านที่รองรับหรือไม่
    if shop_name not in KITCHEN_LATENCY:
        # อธิบาย: ถ้าร้านไม่มีอยู่ ให้ส่ง HTTP 404 กลับไปยังผู้เรียก API
        raise HTTPException(status_code=404, detail="Shop not found")

    # อธิบาย: อ่านเวลาทำอาหารของร้านที่เลือกจาก Dictionary
    cooking_time = KITCHEN_LATENCY[shop_name]

    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | [📥 INBOUND ORDER from Student: {order.student_id}] Shop '{shop_name}' started cooking '{order.menu_name}'...")
    # อธิบาย: จำลองเวลาทำอาหารแบบ Asynchronous โดยไม่บล็อก Event Loop
    await asyncio.sleep(cooking_time)
    # อธิบาย: แสดงข้อความสถานะหรือผลลัพธ์ออกทางหน้าจอ
    print(f"{ctime()} | [🎯 COMPLETED] Shop '{shop_name}' finished cooking '{order.menu_name}'!")

    # อธิบาย: เริ่มสร้าง Dictionary เพื่อใช้เป็นข้อมูลผลลัพธ์/JSON Response
    return {
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "status": "READY_FOR_PICKUP",
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "student_id": order.student_id,
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "shop": shop_name,
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "menu": order.menu_name,
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "cooking_seconds": cooking_time,
        # อธิบาย: กำหนดคู่ key-value หนึ่งรายการภายใน Dictionary
        "timestamp": ctime()
    # อธิบาย: ปิดโครงสร้างข้อมูลหรือคำสั่งหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }

# How to run the server: uvicorn foodcourt_api:app --port 8088
