import threading
import webbrowser

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


# 1. รับค่ารหัสนักศึกษาและ IP ของ Server
student_id = input(
    "กรุณากรอกรหัสนักศึกษา (Student ID): "
).strip()

server_ip = input(
    "กรุณากรอก IP ของ Server "
    "(กด Enter หากเป็น localhost): "
).strip() or "localhost"


app = FastAPI(
    title=f"Client Screen - {student_id}"
)


# 2. โค้ด HTML สำหรับหน้าจอ Client
html_code = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        หน้าจอแสดงผล - {student_id}
    </title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: sans-serif;
            margin: 30px;
            background: #0f172a;
            color: #f8fafc;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .card {{
            background: #1e293b;
            padding: 20px;
            border-radius: 8px;
            border-left: 6px solid #38bdf8;
            margin-bottom: 20px;
        }}

        #status {{
            font-weight: bold;
            color: #fbbf24;
        }}

        #messages {{
            border: 1px solid #334155;
            height: 350px;
            overflow-y: auto;
            padding: 12px;
            background: #1e293b;
            border-radius: 6px;
            margin-bottom: 12px;
        }}

        .message {{
            padding: 6px 0;
            border-bottom: 1px solid #334155;
            word-break: break-word;
        }}

        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        input {{
            flex: 1;
            min-width: 220px;
            padding: 10px 14px;
            border-radius: 4px;
            border: none;
            font-size: 14px;
        }}

        button {{
            padding: 10px 14px;
            border-radius: 4px;
            border: none;
            font-size: 14px;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }}

        button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .send-button {{
            background: #3b82f6;
        }}

        .send-button:hover {{
            background: #2563eb;
        }}

        .test-button {{
            background: #22c55e;
        }}

        .test-button:hover {{
            background: #16a34a;
        }}

        .stop-button {{
            background: #ef4444;
        }}

        .stop-button:hover {{
            background: #dc2626;
        }}

        #testResult {{
            margin-top: 12px;
            color: #94a3b8;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="card">
            <h1>หน้าจอแสดงผลนักศึกษา</h1>

            <h3>
                รหัสนักศึกษา:
                <span style="color:#38bdf8;">
                    {student_id}
                </span>
            </h3>

            <p style="font-size:0.85em; color:#94a3b8;">
                เชื่อมต่อไปยัง Server:
                ws://{server_ip}:8088/ws/{student_id}
            </p>

            <p>
                สถานะ:
                <span id="status">
                    กำลังเชื่อมต่อ...
                </span>
            </p>
        </div>

        <div id="messages"></div>

        <div class="controls">
            <input
                type="text"
                id="messageText"
                placeholder="พิมพ์ข้อความ..."
                autocomplete="off"
            >

            <button
                id="sendButton"
                class="send-button"
                onclick="sendMessage()"
                disabled
            >
                ส่งข้อความ
            </button>

            <button
                id="testButton"
                class="test-button"
                onclick="startTestMessages()"
                disabled
            >
                ทดสอบส่ง “ผมกรคับ” 20 ครั้ง
            </button>

            <button
                class="stop-button"
                onclick="stopTestMessages()"
            >
                หยุดส่ง
            </button>
        </div>

        <div id="testResult">
            ยังไม่ได้เริ่มทดสอบ
        </div>
    </div>

    <script>
        const websocketUrl =
            "ws://{server_ip}:8088/ws/{student_id}";

        const ws = new WebSocket(websocketUrl);

        const statusElement =
            document.getElementById("status");

        const messagesElement =
            document.getElementById("messages");

        const inputElement =
            document.getElementById("messageText");

        const sendButton =
            document.getElementById("sendButton");

        const testButton =
            document.getElementById("testButton");

        const testResult =
            document.getElementById("testResult");


        let testInterval = null;
        let sentCount = 0;


        // จำนวนข้อความสูงสุด
        const maxMessages = 20;

        // ระยะห่างระหว่างข้อความ หน่วยมิลลิวินาที
        const delayMilliseconds = 300;


        ws.onopen = function() {{
            statusElement.textContent =
                "เชื่อมต่อสำเร็จ";

            statusElement.style.color =
                "#22c55e";

            sendButton.disabled = false;
            testButton.disabled = false;

            addMessage(
                "[Client] เชื่อมต่อ WebSocket สำเร็จ"
            );
        }};


        ws.onmessage = function(event) {{
            addMessage(event.data);
        }};


        ws.onerror = function() {{
            statusElement.textContent =
                "เกิดข้อผิดพลาด";

            statusElement.style.color =
                "#ef4444";

            addMessage(
                "[Client] เกิดข้อผิดพลาดในการเชื่อมต่อ"
            );
        }};


        ws.onclose = function(event) {{
            statusElement.textContent =
                "ตัดการเชื่อมต่อแล้ว";

            statusElement.style.color =
                "#ef4444";

            sendButton.disabled = true;
            testButton.disabled = true;

            stopTestMessages();

            addMessage(
                "[Client] WebSocket ถูกปิด " +
                "(Code: " + event.code + ")"
            );
        }};


        function addMessage(text) {{
            const message =
                document.createElement("div");

            message.className = "message";
            message.textContent = text;

            messagesElement.appendChild(message);

            messagesElement.scrollTop =
                messagesElement.scrollHeight;
        }}


        function sendMessage() {{
            const message =
                inputElement.value.trim();

            if (message === "") {{
                return;
            }}

            if (
                ws.readyState !== WebSocket.OPEN
            ) {{
                alert(
                    "WebSocket ยังไม่เชื่อมต่อ"
                );

                return;
            }}

            ws.send(message);

            inputElement.value = "";
            inputElement.focus();
        }}


        function startTestMessages() {{
            if (
                ws.readyState !== WebSocket.OPEN
            ) {{
                alert(
                    "WebSocket ยังไม่เชื่อมต่อ"
                );

                return;
            }}

            if (testInterval !== null) {{
                alert(
                    "กำลังทดสอบส่งข้อความอยู่"
                );

                return;
            }}

            sentCount = 0;

            testButton.disabled = true;

            testResult.textContent =
                "กำลังทดสอบส่งข้อความ...";


            testInterval = setInterval(
                function() {{
                    if (
                        ws.readyState !==
                        WebSocket.OPEN
                    ) {{
                        stopTestMessages();
                        return;
                    }}

                    ws.send("ผมกรคับ");

                    sentCount++;

                    testResult.textContent =
                        "ส่งแล้ว " +
                        sentCount +
                        " / " +
                        maxMessages +
                        " ข้อความ";

                    console.log(
                        "ส่งข้อความครั้งที่ " +
                        sentCount
                    );


                    if (
                        sentCount >= maxMessages
                    ) {{
                        stopTestMessages();

                        testResult.textContent =
                            "ทดสอบเสร็จสิ้น " +
                            "ส่งครบ " +
                            maxMessages +
                            " ข้อความ";
                    }}
                }},
                delayMilliseconds
            );
        }}


        function stopTestMessages() {{
            if (testInterval !== null) {{
                clearInterval(testInterval);
                testInterval = null;
            }}

            if (
                ws.readyState === WebSocket.OPEN
            ) {{
                testButton.disabled = false;
            }}

            if (
                sentCount > 0 &&
                sentCount < maxMessages
            ) {{
                testResult.textContent =
                    "หยุดการทดสอบแล้ว " +
                    "ส่งไปทั้งหมด " +
                    sentCount +
                    " ข้อความ";
            }}
        }}


        inputElement.addEventListener(
            "keydown",
            function(event) {{
                if (event.key === "Enter") {{
                    sendMessage();
                }}
            }}
        );
    </script>
</body>
</html>
"""


@app.get("/")
async def get_index():
    return HTMLResponse(
        content=html_code
    )


def open_browser():
    webbrowser.open(
        "http://127.0.0.1:8001"
    )


if __name__ == "__main__":
    client_port = 8001

    # รอให้ Web Server เริ่มทำงานเล็กน้อย
    # ก่อนเปิด Browser
    threading.Timer(
        1.0,
        open_browser
    ).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=client_port
    )