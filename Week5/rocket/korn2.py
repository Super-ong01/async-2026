import json
import threading
import webbrowser

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


# =========================================================
# ตั้งค่า Server
# =========================================================

server_ip = (
    input(
        "กรุณากรอก IP ของ WebSocket Server "
        "(กด Enter หากเป็น localhost): "
    ).strip()
    or "localhost"
)

client_port = 8002

# สร้าง ID Rocket_001 ถึง Rocket_100
rocket_ids = [
    f"Rocket_{number:03d}"
    for number in range(1, 101)
]

rocket_ids_json = json.dumps(rocket_ids)

app = FastAPI(
    title="100 Rocket WebSocket Clients"
)


# =========================================================
# หน้าเว็บ Client
# =========================================================

html_code = f"""
<!DOCTYPE html>
<html lang="th">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>100 Rocket Clients</title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 25px;

            background: #0f172a;
            color: #f8fafc;

            font-family: Arial, sans-serif;
        }}

        .container {{
            max-width: 1300px;
            margin: 0 auto;
        }}

        .header {{
            background: #1e293b;
            border-left: 6px solid #38bdf8;
            border-radius: 12px;

            padding: 20px;
            margin-bottom: 20px;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(
                auto-fit,
                minmax(180px, 1fr)
            );

            gap: 12px;
            margin-top: 16px;
        }}

        .summary-card {{
            background: #020617;
            border: 1px solid #334155;
            border-radius: 8px;

            padding: 14px;
            text-align: center;
        }}

        .summary-number {{
            display: block;

            margin-top: 6px;

            font-size: 28px;
            font-weight: bold;
        }}

        .controls {{
            display: grid;
            grid-template-columns: repeat(
                auto-fit,
                minmax(180px, 1fr)
            );

            gap: 12px;

            background: #1e293b;
            border-radius: 12px;

            padding: 18px;
            margin-bottom: 20px;
        }}

        button {{
            min-height: 50px;

            border: none;
            border-radius: 8px;

            color: white;
            font-size: 15px;
            font-weight: bold;

            cursor: pointer;
        }}

        button:active {{
            transform: scale(0.97);
        }}

        .left-button {{
            background: #0284c7;
        }}

        .right-button {{
            background: #4f46e5;
        }}

        .thrust-button {{
            background: #dc2626;
        }}

        .reconnect-button {{
            background: #16a34a;
        }}

        .disconnect-button {{
            background: #ea580c;
        }}

        .rocket-grid {{
            display: grid;
            grid-template-columns: repeat(
                auto-fill,
                minmax(180px, 1fr)
            );

            gap: 10px;
        }}

        .rocket-card {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;

            padding: 12px;
        }}

        .rocket-card.connected {{
            border-color: #22c55e;
        }}

        .rocket-card.disconnected {{
            border-color: #ef4444;
        }}

        .rocket-name {{
            margin: 0 0 8px;

            color: #38bdf8;
            font-weight: bold;
        }}

        .status {{
            color: #fbbf24;
            font-size: 13px;
        }}

        .individual-controls {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;

            gap: 5px;
            margin-top: 10px;
        }}

        .individual-controls button {{
            min-height: 34px;
            padding: 4px;

            font-size: 11px;
        }}

        #eventLog {{
            height: 220px;
            overflow-y: auto;

            margin-top: 20px;
            padding: 12px;

            background: #020617;
            border: 1px solid #334155;
            border-radius: 8px;

            font-family: monospace;
            font-size: 12px;
        }}
    </style>
</head>

<body>

<div class="container">

    <section class="header">
        <h1>🚀 100 Rocket WebSocket Clients</h1>

        <p>
            สร้าง ID ตั้งแต่
            <strong>Rocket_001</strong>
            ถึง
            <strong>Rocket_100</strong>
        </p>

        <p>
            WebSocket Server:
            <strong>
                ws://{server_ip}:8002/ws/&lt;rocket_id&gt;
            </strong>
        </p>

        <div class="summary">

            <div class="summary-card">
                จำนวนทั้งหมด

                <span
                    id="totalCount"
                    class="summary-number"
                >
                    100
                </span>
            </div>

            <div class="summary-card">
                เชื่อมต่อสำเร็จ

                <span
                    id="connectedCount"
                    class="summary-number"
                    style="color:#22c55e;"
                >
                    0
                </span>
            </div>

            <div class="summary-card">
                กำลังเชื่อมต่อ

                <span
                    id="connectingCount"
                    class="summary-number"
                    style="color:#fbbf24;"
                >
                    0
                </span>
            </div>

            <div class="summary-card">
                ไม่ได้เชื่อมต่อ

                <span
                    id="disconnectedCount"
                    class="summary-number"
                    style="color:#ef4444;"
                >
                    100
                </span>
            </div>

        </div>
    </section>


    <section class="controls">

        <button
            class="left-button"
            onclick="sendToAll('ROTATE_LEFT')"
        >
            ↺ หมุนซ้ายทั้ง 100 ID
        </button>

        <button
            class="right-button"
            onclick="sendToAll('ROTATE_RIGHT')"
        >
            หมุนขวาทั้ง 100 ID ↻
        </button>

        <button
            class="thrust-button"
            onclick="sendToAll('THRUST')"
        >
            🔥 THRUST ทั้ง 100 ID
        </button>

        <button
            class="reconnect-button"
            onclick="connectAll()"
        >
            เชื่อมต่อทั้งหมด
        </button>

        <button
            class="disconnect-button"
            onclick="disconnectAll()"
        >
            ตัดการเชื่อมต่อทั้งหมด
        </button>

    </section>


    <section
        id="rocketGrid"
        class="rocket-grid"
    ></section>


    <section id="eventLog"></section>

</div>


<script>
    const serverIp = {json.dumps(server_ip)};

    const rocketIds = {rocket_ids_json};

    // เก็บ WebSocket แยกตาม Rocket ID
    const sockets = {{}};

    const rocketGrid =
        document.getElementById("rocketGrid");

    const eventLog =
        document.getElementById("eventLog");


    // =====================================================
    // สร้างการ์ดทั้งหมด 100 ID
    // =====================================================

    function createRocketCards() {{
        rocketIds.forEach(function(rocketId) {{
            const card =
                document.createElement("div");

            card.id = `card-${{rocketId}}`;
            card.className = "rocket-card disconnected";

            card.innerHTML = `
                <div class="rocket-name">
                    🚀 ${{rocketId}}
                </div>

                <div>
                    สถานะ:

                    <span
                        id="status-${{rocketId}}"
                        class="status"
                    >
                        ยังไม่เชื่อมต่อ
                    </span>
                </div>

                <div class="individual-controls">

                    <button
                        class="left-button"
                        onclick="
                            sendControl(
                                '${{rocketId}}',
                                'ROTATE_LEFT'
                            )
                        "
                    >
                        ↺
                    </button>

                    <button
                        class="thrust-button"
                        onclick="
                            sendControl(
                                '${{rocketId}}',
                                'THRUST'
                            )
                        "
                    >
                        🔥
                    </button>

                    <button
                        class="right-button"
                        onclick="
                            sendControl(
                                '${{rocketId}}',
                                'ROTATE_RIGHT'
                            )
                        "
                    >
                        ↻
                    </button>

                </div>
            `;

            rocketGrid.appendChild(card);
        }});
    }}


    // =====================================================
    // เชื่อมต่อ Rocket แต่ละ ID
    // =====================================================

    function connectRocket(rocketId) {{
        const currentSocket =
            sockets[rocketId];

        if (
            currentSocket &&
            (
                currentSocket.readyState ===
                    WebSocket.OPEN ||
                currentSocket.readyState ===
                    WebSocket.CONNECTING
            )
        ) {{
            return;
        }}

        updateStatus(
            rocketId,
            "กำลังเชื่อมต่อ...",
            "connecting"
        );

        const websocketUrl =
            `ws://${{serverIp}}:8088/ws/${{rocketId}}`;

        const ws =
            new WebSocket(websocketUrl);

        sockets[rocketId] = ws;


        ws.onopen = function() {{
            updateStatus(
                rocketId,
                "เชื่อมต่อแล้ว",
                "connected"
            );

            addLog(
                `${{rocketId}} connected`
            );

            updateSummary();
        }};


        ws.onmessage = function(event) {{
            addLog(
                `RECEIVE: ${{event.data}}`
            );
        }};


        ws.onerror = function() {{
            updateStatus(
                rocketId,
                "เกิดข้อผิดพลาด",
                "disconnected"
            );

            updateSummary();
        }};


        ws.onclose = function(event) {{
            updateStatus(
                rocketId,
                `ตัดการเชื่อมต่อ (${{event.code}})`,
                "disconnected"
            );

            updateSummary();
        }};

        updateSummary();
    }}


    // =====================================================
    // เปิด 100 Connections พร้อมกัน
    // =====================================================

    function connectAll() {{
        addLog(
            "กำลังเปิด WebSocket 100 connections"
        );

        rocketIds.forEach(function(rocketId) {{
            connectRocket(rocketId);
        }});
    }}


    // =====================================================
    // ตัดการเชื่อมต่อทั้งหมด
    // =====================================================

    function disconnectAll() {{
        rocketIds.forEach(function(rocketId) {{
            const ws =
                sockets[rocketId];

            if (ws) {{
                if (
                    ws.readyState === WebSocket.OPEN ||
                    ws.readyState === WebSocket.CONNECTING
                ) {{
                    ws.close(
                        1000,
                        "Disconnect all"
                    );
                }}
            }}
        }});

        addLog(
            "สั่งตัดการเชื่อมต่อทั้งหมดแล้ว"
        );
    }}


    // =====================================================
    // ส่งคำสั่งแยก ID
    // =====================================================

    function sendControl(
        rocketId,
        action
    ) {{
        const ws =
            sockets[rocketId];

        if (
            !ws ||
            ws.readyState !== WebSocket.OPEN
        ) {{
            addLog(
                `${{rocketId}} ยังไม่เชื่อมต่อ`
            );

            return;
        }}

        const command = {{
            type: "CONTROL",
            rocket_id: rocketId,
            action: action,
            timestamp: new Date().toISOString()
        }};

        ws.send(
            JSON.stringify(command)
        );

        addLog(
            `SEND: ${{rocketId}} -> ${{action}}`
        );
    }}


    // =====================================================
    // ส่งคำสั่งให้ทุก ID
    // =====================================================

    function sendToAll(action) {{
        let successCount = 0;

        rocketIds.forEach(function(rocketId) {{
            const ws =
                sockets[rocketId];

            if (
                ws &&
                ws.readyState === WebSocket.OPEN
            ) {{
                const command = {{
                    type: "CONTROL",
                    rocket_id: rocketId,
                    action: action,
                    timestamp:
                        new Date().toISOString()
                }};

                ws.send(
                    JSON.stringify(command)
                );

                successCount++;
            }}
        }});

        addLog(
            `ส่ง ${{action}} สำเร็จ ` +
            `${{successCount}} connections`
        );
    }}


    // =====================================================
    // อัปเดตสถานะ ID
    // =====================================================

    function updateStatus(
        rocketId,
        text,
        state
    ) {{
        const status =
            document.getElementById(
                `status-${{rocketId}}`
            );

        const card =
            document.getElementById(
                `card-${{rocketId}}`
            );

        status.textContent = text;

        card.classList.remove(
            "connected",
            "disconnected"
        );

        if (state === "connected") {{
            status.style.color = "#22c55e";
            card.classList.add("connected");
        }} else if (state === "connecting") {{
            status.style.color = "#fbbf24";
        }} else {{
            status.style.color = "#ef4444";
            card.classList.add("disconnected");
        }}
    }}


    // =====================================================
    // นับจำนวน Connection
    // =====================================================

    function updateSummary() {{
        let connected = 0;
        let connecting = 0;
        let disconnected = 0;

        rocketIds.forEach(function(rocketId) {{
            const ws =
                sockets[rocketId];

            if (!ws) {{
                disconnected++;
                return;
            }}

            if (
                ws.readyState === WebSocket.OPEN
            ) {{
                connected++;
            }} else if (
                ws.readyState ===
                WebSocket.CONNECTING
            ) {{
                connecting++;
            }} else {{
                disconnected++;
            }}
        }});

        document.getElementById(
            "connectedCount"
        ).textContent = connected;

        document.getElementById(
            "connectingCount"
        ).textContent = connecting;

        document.getElementById(
            "disconnectedCount"
        ).textContent = disconnected;
    }}


    // =====================================================
    // Event Log
    // =====================================================

    function addLog(message) {{
        const time =
            new Date().toLocaleTimeString();

        const line =
            document.createElement("div");

        line.textContent =
            `[${{time}}] ${{message}}`;

        eventLog.appendChild(line);

        // จำกัด Log ไม่ให้เกิน 300 บรรทัด
        while (
            eventLog.children.length > 300
        ) {{
            eventLog.removeChild(
                eventLog.firstChild
            );
        }}

        eventLog.scrollTop =
            eventLog.scrollHeight;
    }}


    // =====================================================
    // Keyboard Control
    // =====================================================

    window.addEventListener(
        "keydown",
        function(event) {{
            if (event.key === "ArrowLeft") {{
                sendToAll("ROTATE_LEFT");
            }}

            if (event.key === "ArrowRight") {{
                sendToAll("ROTATE_RIGHT");
            }}

            if (event.key === "ArrowUp") {{
                sendToAll("THRUST");
            }}
        }}
    );


    // =====================================================
    // เริ่มระบบ
    // =====================================================

    createRocketCards();

    // เชื่อมต่อทั้ง 100 ID ทันทีเมื่อเปิดหน้าเว็บ
    connectAll();

    // อัปเดตตัวเลขสรุปเป็นระยะ
    setInterval(
        updateSummary,
        1000
    );
</script>

</body>
</html>
"""


# =========================================================
# FastAPI Endpoint
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTMLResponse(
        content=html_code
    )


# =========================================================
# เปิด Browser
# =========================================================

def open_browser():
    webbrowser.open(
        f"http://127.0.0.1:{client_port}"
    )


# =========================================================
# เริ่ม Client Server
# =========================================================

if __name__ == "__main__":
    threading.Timer(
        1.0,
        open_browser
    ).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=client_port
    )