# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
"""
uvicorn main:app --host 0.0.0.0 --port 8088 --reload
"""
# อธิบาย: นำเข้า asyncio สำหรับ Coroutine, Task, Event Loop และงาน Asynchronous
import asyncio
# อธิบาย: นำเข้า Dict สำหรับระบุชนิดข้อมูล Dictionary ด้วย Type Hint
from typing import Dict
# อธิบาย: นำเข้า FastAPI, WebSocket และ WebSocketDisconnect เพื่อสร้าง Server และจัดการการเชื่อมต่อ WebSocket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI(title="WebSocket Central Server")

# ------------------------------------------------------------------
# WebSocket Connection Manager
# ------------------------------------------------------------------
# อธิบาย: ประกาศคลาสสำหรับเก็บและจัดการ WebSocket Connection ของผู้ใช้
class ConnectionManager:
    # อธิบาย: ประกาศ Constructor สำหรับกำหนดค่าเริ่มต้นของออบเจ็กต์
    def __init__(self):
        # เก็บ WebSocket connection โดยใช้ student_id เป็น Key
        # อธิบาย: สร้าง Dictionary สำหรับเก็บ WebSocket Connection ที่กำลัง Active
        self.active_connections: Dict[str, WebSocket] = {}

    # อธิบาย: ประกาศ เมธอดสำหรับรับและบันทึก WebSocket Connection
    async def connect(self, student_id: str, websocket: WebSocket):
        # อธิบาย: ยอมรับการเชื่อมต่อ WebSocket จาก Client
        await websocket.accept()
        # อธิบาย: สร้าง Dictionary สำหรับเก็บ WebSocket Connection ที่กำลัง Active
        self.active_connections[student_id] = websocket

    # อธิบาย: ประกาศ เมธอดสำหรับลบ WebSocket Connection ที่ปิดแล้ว
    def disconnect(self, student_id: str):
        # อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
        if student_id in self.active_connections:
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            del self.active_connections[student_id]

    # อธิบาย: ประกาศ เมธอดสำหรับส่งข้อมูลไปยัง Client ที่เชื่อมต่ออยู่
    async def broadcast(self, message: str):
        # กระจายข้อความไปยัง Client ทุกเครื่องที่เชื่อมต่ออยู่
        # อธิบาย: วนลูปผ่านข้อมูลแต่ละรายการตาม Collection ที่กำหนด
        for connection in self.active_connections.values():
            # อธิบาย: ส่งข้อความไปยัง WebSocket Connection หนึ่งรายการ
            await connection.send_text(message)

# อธิบาย: สร้างออบเจ็กต์ Manager เพื่อใช้จัดการ Connection และสถานะร่วมกันทั้ง Server
manager = ConnectionManager()

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/")
# อธิบาย: ประกาศ Endpoint สำหรับดูสถานะ Server และรายการ Client ที่เชื่อมต่อ
async def get_status():
    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "status": "Server Online",
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "connected_students": list(manager.active_connections.keys())
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }

# ------------------------------------------------------------------
# WebSocket Endpoint (รับ student_id จาก URL)
# ------------------------------------------------------------------
# อธิบาย: ประกาศ WebSocket Endpoint สำหรับรับการเชื่อมต่อแบบสองทางต่อเนื่อง
@app.websocket("/ws/{student_id}")
# อธิบาย: ประกาศ WebSocket Endpoint หลักสำหรับรับ/ส่งข้อมูลกับ Client
async def websocket_endpoint(websocket: WebSocket, student_id: str):
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    await manager.connect(student_id, websocket)
    # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
    await manager.broadcast(f"[System]: รหัสนักศึกษา {student_id} เชื่อมต่อเข้าสู่ระบบ")

    # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
    try:
        # อธิบาย: เริ่มลูปไม่สิ้นสุดเพื่อรอรับข้อมูลจาก WebSocket ต่อเนื่อง
        while True:
            # รอรับข้อมูลจาก Client
            # อธิบาย: รอรับข้อความ Text จาก Client ผ่าน WebSocket
            data = await websocket.receive_text()
            # กระจายข้อมูลให้ทุกหน้าจอ
            # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
            await manager.broadcast(f"[{student_id}]: {data}")

    # อธิบาย: ดักจับเหตุการณ์ที่ Client ตัดการเชื่อมต่อ WebSocket
    except WebSocketDisconnect:
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        manager.disconnect(student_id)
        # อธิบาย: เรียก Manager เพื่อกระจายข้อมูลไปยัง Client ที่เชื่อมต่อ
        await manager.broadcast(f"[System]: รหัสนักศึกษา {student_id} ออกจากระบบ")
