# อธิบาย: นำเข้า webbrowser เพื่อเปิดหน้าเว็บใน Browser อัตโนมัติจาก Python
import webbrowser
# อธิบาย: นำเข้า uvicorn ซึ่งเป็น ASGI Server สำหรับรัน FastAPI
import uvicorn
# อธิบาย: นำเข้า FastAPI สำหรับสร้าง Web API/Application
from fastapi import FastAPI
# อธิบาย: นำเข้า HTMLResponse เพื่อส่ง HTML กลับไปยัง Browser
from fastapi.responses import HTMLResponse

# 1. รับค่ารหัสนักศึกษา และ IP ของ Server
# อธิบาย: รับค่าจากผู้ใช้ทาง Terminal แล้วเก็บไว้ในตัวแปร student_id
student_id = input("กรุณากรอกรหัสนักศึกษา (Student ID): ").strip()
# อธิบาย: รับค่าจากผู้ใช้ทาง Terminal แล้วเก็บไว้ในตัวแปร server_ip
server_ip = input("กรุณากรอก IP ของ Server (กด Enter หากเป็น localhost): ").strip() or "localhost"

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI(title=f"Client Screen - {student_id}")

# 2. โค้ด HTML แสดงผลหน้าจอ
# อธิบาย: เริ่มสร้างข้อความหลายบรรทัดเก็บในตัวแปร html_code; ในไฟล์นี้ใช้สำหรับ HTML/JavaScript หรือคำอธิบาย
html_code = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>หน้าจอแสดงผล - {student_id}</title>
        <style>
            body {{ font-family: sans-serif; margin: 30px; background: #0f172a; color: #f8fafc; }}
            .card {{ background: #1e293b; padding: 20px; border-radius: 8px; border-left: 6px solid #38bdf8; margin-bottom: 20px; }}
            #messages {{ border: 1px solid #334155; height: 300px; overflow-y: scroll; padding: 12px; background: #1e293b; border-radius: 6px; }}
            input, button {{ padding: 10px 14px; margin-top: 10px; border-radius: 4px; border: none; font-size: 14px; }}
            button {{ background: #3b82f6; color: white; cursor: pointer; font-weight: bold; }}
            button:hover {{ background: #2563eb; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>หน้าจอแสดงผลนักศึกษา</h1>
            <h3>รหัสนักศึกษา: <span style="color:#38bdf8;">{student_id}</span></h3>
            <p style="font-size: 0.85em; color: #94a3b8;">เชื่อมต่อไปยัง Server: ws://{server_ip}:8088/ws/{student_id}</p>
        </div>

        <div id="messages"></div>

        <input type="text" id="messageText" placeholder="พิมพ์ข้อความ..." autocomplete="off"/>
        <button onclick="sendMessage()">ส่งข้อความ (Broadcast)</button>

        <script>
            // เชื่อมต่อไปยัง Server หลักตาม IP และ Student ID
            const ws = new WebSocket("ws://{server_ip}:8088/ws/{student_id}");

            ws.onmessage = function(event) {{
                const messages = document.getElementById('messages');
                const message = document.createElement('div');
                message.style.padding = '4px 0';
                message.textContent = event.data;
                messages.appendChild(message);
                messages.scrollTop = messages.scrollHeight;
            }};

            function sendMessage() {{
                const input = document.getElementById("messageText");
                if (input.value) {{
                    ws.send(input.value);
                    input.value = '';
                }}
            }}
        </script>
    </body>
</html>
"""

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/")
# อธิบาย: ประกาศ Endpoint หน้าแรกสำหรับส่งหน้า HTML ไปยัง Browser
async def get_index():
    # อธิบาย: ส่ง HTML ที่เตรียมไว้กลับไปยัง Browser ด้วย HTMLResponse
    return HTMLResponse(html_code)

# อธิบาย: ตรวจสอบเงื่อนไขก่อนตัดสินใจทำงานในบล็อกนี้
if __name__ == "__main__":
    # client port
    # อธิบาย: กำหนด Port ที่ FastAPI Client UI จะเปิดให้ Browser เข้าใช้งาน
    client_port = 8001
    # เปิด เบราว์เซอร์ อัตโนมัติไปยังหน้าจอ Client บนเครื่องนั้นๆ
    # อธิบาย: สั่งเปิด URL ใน Browser ของเครื่องผู้ใช้
    webbrowser.open(f"http://127.0.0.1:{8001}")
    # รัน Local Web Server บน Port 8001
    # อธิบาย: สั่งรัน FastAPI Application ด้วย Uvicorn ตาม Host และ Port ที่กำหนด
    uvicorn.run(app, host="127.0.0.1", port=client_port)
