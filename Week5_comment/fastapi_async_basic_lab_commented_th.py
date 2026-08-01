# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
"""
================================================================================
CS-302: Introduction to FastAPI - Async Basics Lab 02
Topic: Understanding async, await, and Non-blocking Cooperative Multitasking
================================================================================

How to Run This Lab:
--------------------
1. Run the development server:
   $ uvicorn fastapi_async_basic_lab:app --reload --port 8000

2. Open your browser to test endpoints:
   - Sync Blocking:       http://127.0.0.1:8000/sync-delay
   - Async Non-Blocking:  http://127.0.0.1:8000/async-delay
   - Concurrent Tasks:    http://127.0.0.1:8000/concurrent-tasks
"""

# อธิบาย: นำเข้า asyncio สำหรับ Coroutine, Task, Event Loop และงาน Asynchronous
import asyncio
# อธิบาย: นำเข้าโมดูล time เพื่อหน่วงเวลาแบบ Blocking และวัดระยะเวลาการทำงาน
import time
# อธิบาย: นำเข้า FastAPI สำหรับสร้าง Web API/Application
from fastapi import FastAPI

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI(
    # อธิบาย: กำหนดชื่อของ FastAPI Application
    title="CS-302: Basic Async FastAPI Lab",
    # อธิบาย: กำหนดคำอธิบายของ Application ที่จะแสดงใน API Docs
    description="A foundational lab to teach students the difference between blocking synchronous code and cooperative asynchronous code.",
    # อธิบาย: กำหนดเวอร์ชันของ Application
    version="1.0.0"
# อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
)

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/sync-delay")
# อธิบาย: ประกาศ Endpoint แบบ Synchronous สำหรับสาธิต Blocking
def sync_delay():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 1: Traditional Synchronous Blocking (def)
    ----------------------------------------------
    - We use 'time.sleep(3)' to simulate a heavy operation (like a slow database query).
    - Even though FastAPI runs standard 'def' in a thread pool to avoid freezing the main thread,
      each request still occupies and completely blocks an entire OS thread for 3 full seconds.
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Starting synchronous blocking sleep...")

    # This blocks the thread. No other code can run on this thread during this time.
    # อธิบาย: หยุด Thread ปัจจุบันแบบ Blocking ตามจำนวนวินาทีที่กำหนด
    time.sleep(3) 

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Finished sync task in {duration:.2f} seconds!")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "mode": "Synchronous (Blocking)",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "message": "This task completely occupied a thread for 3 seconds.",
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "duration_seconds": round(duration, 2)
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }


# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/async-delay")
# อธิบาย: ประกาศ Endpoint แบบ Asynchronous สำหรับสาธิต Non-Blocking
async def async_delay():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 2: Cooperative Asynchronous (async def)
    ----------------------------------------------
    - We use 'async def' to run this function directly on the main Event Loop.
    - We use 'await asyncio.sleep(3)' to simulate waiting for an external response.
    - Crucial difference: The word 'await' tells the Event Loop, "I am going to wait for 3 seconds.
      Please feel free to pause me and go handle other incoming user requests in the meantime!"
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Starting cooperative asynchronous sleep...")

    # This does NOT block. It yields control back to the Event Loop.
    # อธิบาย: พัก Coroutine แบบ Non-Blocking และคืนสิทธิ์ให้ Event Loop ไปทำงานอื่นระหว่างรอ
    await asyncio.sleep(3) 

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Finished async task in {duration:.2f} seconds!")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "mode": "Asynchronous (Non-Blocking)",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "message": "The server yielded control to help other clients while waiting.",
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "duration_seconds": round(duration, 2)
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }


# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/concurrent-tasks")
# อธิบาย: ประกาศ Endpoint สำหรับสาธิตการรันหลาย Task พร้อมกัน
async def run_concurrent_tasks():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 3: Power of Concurrency (asyncio.gather)
    ---------------------------------------------
    - What if we have to fetch data from 3 different external APIs, and each takes 2 seconds?
    - Synchronous way: 2 + 2 + 2 = 6 seconds of total waiting.
    - Asynchronous way: We can fire all 3 requests at the same time and 'await' them concurrently.
    - Total waiting time drops to just ~2 seconds (the speed of the slowest task)!
    """
    # อธิบาย: บันทึกเวลาเริ่มต้นเพื่อใช้คำนวณระยะเวลาทำงาน
    start_time = time.time()
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Starting 3 concurrent tasks...")

    # Define a simple helper async function inside
    # อธิบาย: ประกาศ Coroutine ช่วยจำลองการดึงข้อมูลจาก API
    async def fetch_data_from_api(api_name: str, wait_time: int):
        # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
        print(f"👉 [Task] Starting fetch from {api_name} (takes {wait_time}s)...")
        # อธิบาย: พัก Coroutine แบบ Non-Blocking และคืนสิทธิ์ให้ Event Loop ไปทำงานอื่นระหว่างรอ
        await asyncio.sleep(wait_time)
        # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
        print(f"✅ [Task] Finished fetch from {api_name}!")
        # อธิบาย: คืนค่าผลลัพธ์จากฟังก์ชันให้ผู้เรียก
        return f"Data from {api_name}"

    # We pack all tasks together and run them in parallel
    # อธิบาย: ใช้ asyncio.gather() รันและรอหลาย Coroutine พร้อมกัน แล้วเก็บผลลัพธ์ตามลำดับ
    results = await asyncio.gather(
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        fetch_data_from_api("API_Alpha", 2),
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        fetch_data_from_api("API_Beta", 3),
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        fetch_data_from_api("API_Gamma", 1)
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    )

    # อธิบาย: คำนวณเวลาที่ใช้ทั้งหมดจากเวลาปัจจุบันลบเวลาเริ่มต้น
    duration = time.time() - start_time
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] All concurrent tasks completed in {duration:.2f} seconds!")

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "mode": "Concurrent Async Execution",
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "results_received": results,
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "efficiency_note": "If executed sequentially, it would have taken 6s (2+3+1). Concurrently, it took only ~3s!",
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "duration_seconds": round(duration, 2)
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }
