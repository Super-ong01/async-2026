import asyncio
import time
import httpx

student_id = "123456"


async def fire_rocket(name: str, t0: float):
    url = f"http://172.16.2.117:8088/fire/{student_id}"
    start_time = time.perf_counter() - t0  # เวลาเริ่มสัมพัทธ์

    # ส่ง GET request แบบ async
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    # อ่านค่า time_to_target จาก API response
    time_to_target = float(data["time_to_target"])

    # เวลาที่ rocket ไปถึงจุดหมาย นับจากเวลาเริ่มชุด rockets
    end_time = time.perf_counter() - t0

    return {
        "name": name,
        "start_time": start_time,
        "time_to_target": time_to_target,
        "end_time": end_time
    }


async def main():
    t0 = time.perf_counter()  # เวลาเริ่มของชุด rockets

    print("Rocket prepare to launch ...")

    # สร้าง task ยิง rocket 3 ลูกพร้อมกัน
    tasks = [
        asyncio.create_task(fire_rocket(f"Rocket-{i}", t0))
        for i in range(1, 4)
    ]

    # รอให้ทุก task เสร็จ และเก็บผลลัพธ์ตามลำดับ task
    results = await asyncio.gather(*tasks)

    print("Rockets fired:")

    # แสดงผลของแต่ละ rocket
    for r in results:
        print(
            f'{r["name"]} | '
            f'start_time: {r["start_time"]:.2f} sec | '
            f'time_to_target: {r["time_to_target"]:.2f} sec | '
            f'end_time: {r["end_time"]:.2f} sec'
        )

    # เวลารวมทั้งหมด = เวลาที่ rocket ลูกสุดท้ายไปถึงจุดหมาย
    t_total = max(r["end_time"] for r in results)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")


asyncio.run(main())
