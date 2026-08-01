# อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
"""
================================================================================
CS-302: Introduction to FastAPI - Basic Lab 01
Topic: First Step with FastAPI, Routing, Parameters, & Basic Validation
================================================================================

How to Run This Lab:
--------------------
1. Install dependencies (if you haven't yet):
   $ pip install fastapi uvicorn

2. Run the development server:
   $ uvicorn fastapi_basic_lab:app --reload

3. Open your browser:
   - Interactive API Docs (Test Area): http://127.0.0.1:8000/docs
   - Hello World endpoint:              http://127.0.0.1:8000/
"""

# อธิบาย: นำเข้า FastAPI สำหรับสร้าง Web API/Application
from fastapi import FastAPI
# อธิบาย: นำเข้า BaseModel จาก Pydantic เพื่อกำหนดโครงสร้างและตรวจสอบข้อมูล Request Body
from pydantic import BaseModel

# อธิบาย: สร้างออบเจ็กต์ FastAPI และกำหนดข้อมูลของ Application
app = FastAPI(
    # อธิบาย: กำหนดชื่อของ FastAPI Application
    title="CS-302: Basic FastAPI Lab",
    # อธิบาย: กำหนดคำอธิบายของ Application ที่จะแสดงใน API Docs
    description="This is the first step lab for students to understand FastAPI routing and data binding.",
    # อธิบาย: กำหนดเวอร์ชันของ Application
    version="1.0.0"
# อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
)

# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/")
# อธิบาย: ประกาศ Endpoint หน้าแรกสำหรับทดสอบว่า Server ทำงาน
def read_root():
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 1: The simplest GET endpoint.
    Returns a basic JSON response to confirm the server is running.
    """
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print("[SERVER LOG] Hello World endpoint was requested!")
    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {"message": "Welcome to CS-302! Your first FastAPI server is alive!"}


# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/items/{item_id}")
# อธิบาย: ประกาศ Endpoint สำหรับรับ Path Parameter item_id
def read_item_by_id(item_id: int):
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 2: Path Parameters and Type Coercion.
    FastAPI reads the URL path. Even though 'item_id' arrives as a string (e.g., "/items/123"),
    FastAPI's type hint 'item_id: int' forces the engine to auto-cast it into a Python Integer.
    """
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Requested Item ID: {item_id} (Type of variable: {type(item_id)})")

    # Notice that we can directly do math operations on item_id because it is already an integer
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    doubled_value = item_id * 2

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "received_item_id": item_id,
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "type_in_python": str(type(item_id)),
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "demonstration_math": f"Your ID doubled is: {doubled_value}"
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }


# อธิบาย: ประกาศ HTTP GET Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.get("/users")
# อธิบาย: ประกาศ Endpoint สำหรับรับ Query Parameters เพื่อค้นหาผู้ใช้
def search_users(username: str, age: int = 18):
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 3: Query Parameters.
    Access via: http://127.0.0.1:8000/users?username=Alice&age=21
    'age' has a default value of 18 if the user does not provide it in the URL.
    """
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] Searching for user: {username}, Age constraint: {age}")
    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "search_term": username,
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "age_filter": age,
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "status": f"Successfully queried user database for {username}"
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }


# อธิบาย: ประกาศ Pydantic Model สำหรับตรวจสอบข้อมูลนักศึกษาที่รับจาก Request Body
class SimpleStudent(BaseModel):
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 4: Creating a Pydantic Model.
    This model acts as a blueprint/contract for incoming POST data.
    """
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    student_id: str
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    nickname: str
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    gpa: float


# อธิบาย: ประกาศ HTTP POST Endpoint ของ FastAPI ตาม Path ที่กำหนด
@app.post("/register/student")
# อธิบาย: ประกาศ Endpoint สำหรับรับ JSON Request Body ของนักศึกษา
def register_student(student: SimpleStudent):
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    """
    Step 5: Receiving JSON Data via POST.
    FastAPI reads the JSON payload from the request body,
    runs it through the SimpleStudent schema, and casts it into a Python Object.
    """
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] New Registration Received!")
    # อธิบาย: แสดงข้อความสถานะหรือ Debug Log ออกทาง Terminal
    print(f"[SERVER LOG] ID: {student.student_id}, Name: {student.nickname}, GPA: {student.gpa}")

    # We can access attributes using dot notation directly!
    # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
    is_academic_probation = student.gpa < 2.00

    # อธิบาย: เริ่มสร้าง Dictionary สำหรับส่งกลับเป็น JSON Response
    return {
        # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
        "message": "Student registration data parsed successfully!",
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "student_object_data": {
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "id": student.student_id,
            # อธิบาย: ระบุอาร์กิวเมนต์หรือสมาชิกหนึ่งรายการในคำสั่งหลายบรรทัด
            "name": student.nickname,
            # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
            "current_gpa": student.gpa
        # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
        },
        # อธิบาย: คำสั่ง Python บรรทัดนี้เป็นส่วนหนึ่งของลำดับการทำงานของโปรแกรม
        "academic_probation_alert": is_academic_probation
    # อธิบาย: ปิดโครงสร้างคำสั่งหรือข้อมูลหลายบรรทัดที่เริ่มไว้ก่อนหน้า
    }
