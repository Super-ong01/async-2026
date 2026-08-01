# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
"""
uvicorn main:app --host 0.0.0.0 --port 8088 --reload
"""
# อธิบาย: นำเข้า FastAPI, WebSocket และ WebSocketDisconnect เพื่อสร้าง Server และจัดการการเชื่อมต่อ WebSocket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# อธิบาย: นำเข้า Dict สำหรับระบุชนิดข้อมูล Dictionary ด้วย Type Hint
from typing import Dict
# อธิบาย: นำเข้า math เพื่อใช้ฟังก์ชันคณิตศาสตร์ เช่น radians(), sin() และ cos()
import math

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI()

# 📐 กำหนดขนาดขอบเขตสนาม (600x800)
# อธิบาย: กำหนดความกว้างของพื้นที่จำลองจรวด
SCREEN_WIDTH = 800
# อธิบาย: กำหนดความสูงของพื้นที่จำลองจรวด
SCREEN_HEIGHT = 600

# อธิบาย: ประกาศคลาสสำหรับจัดการการเชื่อมต่อ WebSocket และสถานะจรวดทั้งหมด
class RocketSpaceManager:
    # อธิบาย: ประกาศ Constructor สำหรับกำหนดค่าเริ่มต้นของออบเจ็กต์
    def __init__(self):
        # อธิบาย: สร้าง Dictionary สำหรับเก็บ WebSocket Connection โดยใช้รหัส Client เป็น Key
        self.connections: Dict[str, WebSocket] = {}
        # อธิบาย: สร้าง Dictionary สำหรับเก็บสถานะของจรวดแต่ละลำ
        self.rockets: Dict[str, dict] = {}

    # อธิบาย: ประกาศ เมธอดสำหรับรับและบันทึก WebSocket Connection
    async def connect(self, rocket_id: str, websocket: WebSocket, is_dashboard: bool = False):
        # อธิบาย: ยอมรับการเชื่อมต่อ WebSocket จาก Client
        await websocket.accept()
        # อธิบาย: สร้าง Dictionary สำหรับเก็บ WebSocket Connection โดยใช้รหัส Client เป็น Key
        self.connections[rocket_id] = websocket

        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
        if not is_dashboard:
            # สุ่มตำแหน่งเริ่มต้นให้อยู่กลางๆ สนาม
            # อธิบาย: สร้าง Dictionary สำหรับเก็บสถานะของจรวดแต่ละลำ
            self.rockets[rocket_id] = {
                # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
                "x": SCREEN_WIDTH / 2,
                # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
                "y": SCREEN_HEIGHT / 2,
                # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
                "angle": 0,
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                "color": f"hsl({(hash(rocket_id) % 360)}, 80%, 60%)"
            # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
            }

        # อธิบาย: ส่งข้อมูล JSON ผ่าน WebSocket ไปยัง Client
        await websocket.send_json({
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "type": "INIT",
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "rockets": self.rockets,
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            "bounds": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        })

    # อธิบาย: ประกาศ เมธอดสำหรับลบ WebSocket Connection ที่ปิดแล้ว
    def disconnect(self, rocket_id: str):
        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
        if rocket_id in self.connections:
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            del self.connections[rocket_id]
        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
        if rocket_id in self.rockets:
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            del self.rockets[rocket_id]

    # อธิบาย: ประกาศ เมธอดสำหรับส่งข้อมูลไปยัง Client ที่เชื่อมต่ออยู่
    async def broadcast(self, message: dict):
        # อธิบาย: วนลูปผ่านข้อมูลแต่ละรายการตาม Collection ที่กำหนด
        for ws in list(self.connections.values()):
            # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
            try:
                # อธิบาย: ส่ง JSON ไปยัง WebSocket Client ปัจจุบัน
                await ws.send_json(message)
            # อธิบาย: ดักจับ Exception ทั่วไปเพื่อไม่ให้โปรแกรมหยุดทั้งระบบ
            except Exception:
                # อธิบาย: ไม่ทำคำสั่งใดเพิ่มเติมในบล็อกนี้
                pass

# อธิบาย: สร้างออบเจ็กต์ Manager เพื่อใช้จัดการ Connection และสถานะร่วมกันทั้ง Server
manager = RocketSpaceManager()

# อธิบาย: ประกาศ WebSocket Endpoint สำหรับรับการเชื่อมต่อแบบสองทางต่อเนื่อง
@app.websocket("/ws/{client_id}")
# อธิบาย: ประกาศ WebSocket Endpoint หลักสำหรับรับ/ส่งข้อมูลกับ Client
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # อธิบาย: ตรวจว่า Client ที่เชื่อมต่อเข้ามาเป็น Dashboard หรือจรวดทั่วไป
    is_dashboard = (client_id == "DASHBOARD")
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    await manager.connect(client_id, websocket, is_dashboard)

    # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
    if not is_dashboard:
        # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
        await manager.broadcast({
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "type": "SPAWN",
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "id": client_id,
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            "rocket": manager.rockets[client_id]
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        })

    # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: เริ่มลูปไม่สิ้นสุดเพื่อรอรับข้อมูลจาก WebSocket ต่อเนื่อง
        while True:
            # อธิบาย: รอรับข้อมูล JSON จาก WebSocket แบบ Asynchronous
            data = await websocket.receive_json()

            # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
            if data["type"] == "CONTROL" and client_id in manager.rockets:
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                rocket = manager.rockets[client_id]
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                action = data["action"]

                # อธิบาย: กำหนดค่าความเร็วที่ใช้ขยับตำแหน่งจรวดต่อหนึ่งคำสั่ง
                speed = 8
                # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
                if action == "ROTATE_LEFT":
                    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                    rocket["angle"] = (rocket["angle"] - 15) % 360
                # อธิบาย: ตรวจเงื่อนไขทางเลือกถัดไป เมื่อเงื่อนไขก่อนหน้าไม่เป็นจริง
                elif action == "ROTATE_RIGHT":
                    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                    rocket["angle"] = (rocket["angle"] + 15) % 360
                # อธิบาย: ตรวจเงื่อนไขทางเลือกถัดไป เมื่อเงื่อนไขก่อนหน้าไม่เป็นจริง
                elif action == "THRUST":
                    # อธิบาย: แปลงมุมจากองศาเป็นเรเดียนเพื่อใช้คำนวณด้วย sin/cos
                    rad = math.radians(rocket["angle"])

                    # คำนวณพิกัดใหม่
                    # อธิบาย: คำนวณตำแหน่งแกน X ใหม่จากมุมและความเร็ว
                    new_x = rocket["x"] + speed * math.cos(rad)
                    # อธิบาย: คำนวณตำแหน่งแกน Y ใหม่จากมุมและความเร็ว
                    new_y = rocket["y"] + speed * math.sin(rad)

                    # 🔒 ล็อคพิกัดไม่ให้หลุดขอบ 800x600 (Padding 20px กันปีกจรวดเกิน)
                    # อธิบาย: จำกัดพิกัดไม่ให้จรวดเคลื่อนออกนอกขอบเขตสนาม
                    rocket["x"] = max(20, min(SCREEN_WIDTH - 20, new_x))
                    # อธิบาย: จำกัดพิกัดไม่ให้จรวดเคลื่อนออกนอกขอบเขตสนาม
                    rocket["y"] = max(20, min(SCREEN_HEIGHT - 20, new_y))

                # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
                await manager.broadcast({
                    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
                    "type": "UPDATE",
                    # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
                    "id": client_id,
                    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                    "rocket": rocket
                # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
                })

    # อธิบาย: ดักจับเหตุการณ์ที่ Client ตัดการเชื่อมต่อ WebSocket
    except WebSocketDisconnect:
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        manager.disconnect(client_id)
        # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
        await manager.broadcast({
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "type": "DESPAWN",
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            "id": client_id
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        })
