# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
"""
================================================================================
🎓 CS-302: Introduction to FastAPI - Async HTTP Client Lab 03
Topic: Consuming External APIs and Non-Blocking Network I/O with HTTPX
================================================================================

How to Run This Lab:
--------------------
1. Install requirements (httpx is mandatory for async request dispatching):
   $ pip install fastapi uvicorn httpx

2. Run the development server:
   $ uvicorn fastapi_async_external_api_lab:app --reload --port 8000

3. Open your browser:
   - Interactive UI Docs: http://127.0.0.1:8000/docs
"""

# อธิบาย: นำเข้า asyncio สำหรับ Coroutine, Task, Event Loop และงาน Asynchronous
import asyncio
# อธิบาย: นำเข้าโมดูล time เพื่อหน่วงเวลาแบบ Blocking และวัดระยะเวลาการทำงาน
import time
# อธิบาย: นำเข้า httpx สำหรับส่ง HTTP Request แบบ Asynchronous
import httpx
# อธิบาย: นำเข้า FastAPI สำหรับสร้าง API และ HTTPException สำหรับส่ง HTTP Error
from fastapi import FastAPI, HTTPException

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI(
    # อธิบาย: กำหนดชื่อของ FastAPI Application
    title="CS-302: Async External HTTP Requests Lab",
    # อธิบาย: กำหนดคำอธิบายของ Application ที่จะแสดงใน API Docs
    description="A lab session focusing on building async wrappers to fetch third-party public web APIs.",
    # อธิบาย: กำหนดเวอร์ชันของ Application
    version="1.0.0"
# อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
)

# We define highly stable and free public endpoints for our experiments
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
CAT_FACT_API = "https://catfact.ninja/fact"
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
BITCOIN_PRICE_API = "https://api.coindesk.com/v1/bpi/currentprice.json"
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
JOKE_API = "https://official-joke-api.appspot.com/random_joke"

# Define fallback mock data for when remote servers are unreachable or rate-limited
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
MOCK_CAT_FACT = {"fact": "[Fallback Mock] Cats sleep for 70% of their lives.", "length": 41}
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
MOCK_BTC_PRICE = {"bpi": {"USD": {"rate": "95,430.00"}}}
# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
MOCK_JOKE = {"setup": "[Fallback Mock] Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs!"}

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/single-fetch")
# อธิบาย: ประกาศ Endpoint สำหรับดึงข้อมูลจาก External API หนึ่งแหล่งแบบ Asynchronous
async def fetch_single_api():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 1: Fetching a single external API asynchronously (With Fallback Grace)
    -----------------------------------------------------
    - We attempt a live fetch. If the remote server fails, we fall back to mock data
      to keep our endpoint alive and healthy (Graceful Degradation).
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Initiating single fetch request to CatFact API...")
    # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
    fallback_used = False

    # อธิบาย: สร้าง Async HTTP Client ภายใน Context Manager เพื่อใช้งานและปิด Connection ให้อัตโนมัติ
    async with httpx.AsyncClient() as client:
        # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
        try:
            # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            response = await client.get(CAT_FACT_API, timeout=3.0) # Faster timeout to avoid hanging
            # อธิบาย: ตรวจ HTTP Status Code และยก Exception ถ้า Response เป็น Error
            response.raise_for_status() 
            # อธิบาย: แปลง JSON Response เป็นข้อมูล Python เพื่อนำไปใช้งานต่อ
            data = response.json()
        # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจาก HTTPX เช่น Network Error หรือ HTTP Error
        except httpx.HTTPError as err:
            # Print the exact exception so the student/instructor can debug the network issue
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print(f"\n[NETWORK WARNING] CatFact API call failed: {str(err)}")
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print("[RESILIENCE] Gracefully falling back to local simulated data...\n")
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            data = MOCK_CAT_FACT
            # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
            fallback_used = True

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Single fetch completed in {duration:.2f} seconds.")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "status": "Success",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "elapsed_seconds": round(duration, 2),
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "source": "CatFact Ninja",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "fallback_activated": fallback_used,
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "fetched_payload": data
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/sequential-fetch")
# อธิบาย: ประกาศ Endpoint สำหรับดึงข้อมูลหลาย API แบบเรียงลำดับ
async def fetch_sequentially():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 2: The Bad Practice - Sequential Wait Loops (With Fallback Grace)
    ---------------------------------------------------------------------
    - Attempts to pull from all three APIs sequentially.
    - If any server fails or times out, we catch the warning, log it, and inject fallback data.
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Starting sequential requests to 3 endpoints...")

    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    results = {}
    # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
    fallback_active = False

    # อธิบาย: สร้าง Async HTTP Client ภายใน Context Manager เพื่อใช้งานและปิด Connection ให้อัตโนมัติ
    async with httpx.AsyncClient() as client:
        # 1. Fetch Cat Fact
        # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
        try:
            # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            res_cat = await client.get(CAT_FACT_API, timeout=3.0)
            # อธิบาย: ตรวจ HTTP Status Code และยก Exception ถ้า Response เป็น Error
            res_cat.raise_for_status()
            # อธิบาย: แปลง JSON Response เป็นข้อมูล Python เพื่อนำไปใช้งานต่อ
            results["cat_fact"] = res_cat.json().get("fact")
        # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจาก HTTPX เช่น Network Error หรือ HTTP Error
        except httpx.HTTPError as err:
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print(f"[SEQUENTIAL-WARN] CatFact API unavailable: {str(err)}")
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            results["cat_fact"] = MOCK_CAT_FACT.get("fact")
            # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
            fallback_active = True

        # 2. Fetch Bitcoin Price
        # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
        try:
            # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            res_btc = await client.get(BITCOIN_PRICE_API, timeout=3.0)
            # อธิบาย: ตรวจ HTTP Status Code และยก Exception ถ้า Response เป็น Error
            res_btc.raise_for_status()
            # อธิบาย: แปลง JSON Response เป็นข้อมูล Python เพื่อนำไปใช้งานต่อ
            results["bitcoin_rate"] = res_btc.json().get("bpi", {}).get("USD", {}).get("rate")
        # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจาก HTTPX เช่น Network Error หรือ HTTP Error
        except httpx.HTTPError as err:
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print(f"[SEQUENTIAL-WARN] Bitcoin API unavailable: {str(err)}")
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            results["bitcoin_rate"] = MOCK_BTC_PRICE.get("bpi", {}).get("USD", {}).get("rate")
            # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
            fallback_active = True

        # 3. Fetch Random Joke
        # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
        try:
            # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            res_joke = await client.get(JOKE_API, timeout=3.0)
            # อธิบาย: ตรวจ HTTP Status Code และยก Exception ถ้า Response เป็น Error
            res_joke.raise_for_status()
            # อธิบาย: แปลง JSON Response เป็นข้อมูล Python เพื่อนำไปใช้งานต่อ
            joke_data = res_joke.json()
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            results["random_joke"] = f"{joke_data.get('setup')} -> {joke_data.get('punchline')}"
        # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจาก HTTPX เช่น Network Error หรือ HTTP Error
        except httpx.HTTPError as err:
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print(f"[SEQUENTIAL-WARN] Joke API unavailable: {str(err)}")
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            joke_data = MOCK_JOKE
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            results["random_joke"] = f"{joke_data.get('setup')} -> {joke_data.get('punchline')}"
            # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
            fallback_active = True

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Sequential process completed in {duration:.2f} seconds.")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "mode": "Sequential (Non-Parallel)",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "elapsed_seconds": round(duration, 2),
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "fallback_activated": fallback_active,
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "results_accumulated": results,
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "critique": "Each request had to wait for the previous one to fully complete."
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/concurrent-fetch")
# อธิบาย: ประกาศ Endpoint สำหรับดึงข้อมูลหลาย API แบบ Concurrent
async def fetch_concurrently():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 3: The Best Practice - Concurrent Gathering (With Fallback Grace)
    ----------------------------------------------------------------------
    - Fires all requests at once. If any fails, we handle them individually
      to prevent the whole batch from crashing.
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Spawning concurrent async tasks...")
    # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
    fallback_active = False

    # Define a helper that handles its own failure and logs details
    # อธิบาย: ประกาศ Coroutine ช่วยดึงข้อมูลภายนอกพร้อมจัดการ Error และ Fallback
    async def fetch_safely(client: httpx.AsyncClient, url: str, mock_data: dict, name: str):
        # อธิบาย: เริ่มบล็อก try สำหรับโค้ดที่อาจเกิด Exception
        try:
            # อธิบาย: ส่ง HTTP GET Request แบบ Asynchronous และรอ Response โดยไม่บล็อก Event Loop
            response = await client.get(url, timeout=3.0)
            # อธิบาย: ตรวจ HTTP Status Code และยก Exception ถ้า Response เป็น Error
            response.raise_for_status()
            # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
            return response.json(), False
        # อธิบาย: ดักจับข้อผิดพลาดที่เกิดจาก HTTPX เช่น Network Error หรือ HTTP Error
        except httpx.HTTPError as err:
            # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
            print(f"[CONCURRENT-WARN] {name} API failed: {str(err)}")
            # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
            return mock_data, True

    # อธิบาย: สร้าง Async HTTP Client ภายใน Context Manager เพื่อใช้งานและปิด Connection ให้อัตโนมัติ
    async with httpx.AsyncClient() as client:
        # Launch tasks concurrently using helper
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        cat_task = fetch_safely(client, CAT_FACT_API, MOCK_CAT_FACT, "CatFact")
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        btc_task = fetch_safely(client, BITCOIN_PRICE_API, MOCK_BTC_PRICE, "Bitcoin")
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        joke_task = fetch_safely(client, JOKE_API, MOCK_JOKE, "Joke")

        # Gather parallel requests
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        cat_res, btc_res, joke_res = await asyncio.gather(
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            cat_task, btc_task, joke_task
        # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        )

        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        cat_data, cat_fallback = cat_res
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        btc_data, btc_fallback = btc_res
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        joke_data, joke_fallback = joke_res

        # อธิบาย: กำหนด Flag เพื่อบอกว่าระบบใช้ข้อมูลสำรอง Fallback หรือไม่
        fallback_active = cat_fallback or btc_fallback or joke_fallback

        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        processed_results = {
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "cat_fact": cat_data.get("fact"),
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "bitcoin_rate": btc_data.get("bpi", {}).get("USD", {}).get("rate"),
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            "random_joke": f"{joke_data.get('setup')} -> {joke_data.get('punchline')}"
        # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        }

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Concurrent process completed in {duration:.2f} seconds!")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "mode": "Concurrent Async (Parallel Network I/O)",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "elapsed_seconds": round(duration, 2),
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "fallback_activated": fallback_active,
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "results_accumulated": processed_results,
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "efficiency_note": "If sequential took ~3s, this took only the time of the slowest single request!"
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }
