import asyncio
import random
import time
import json
import redis.asyncio as redis


# ============================================================
# CONFIGURATION
# ============================================================

REDIS_HOST = '172.16.46.79'
REDIS_PORT = 6379

GROUP_ID = 'g02'
STUDENT_ID = '6710301004'

STREAM_KEY = f"f1:telemetry:{GROUP_ID}"

FINISH_DISTANCE = 10000.0       # 10 km

MAX_SPEED_KMH = 330.0           # ห้ามเกิน 330 km/h

SEND_INTERVAL = 0.05            # 20 Hz


# ============================================================
# HELPER
# ============================================================

def clamp(value, minimum, maximum):
    """จำกัดค่าไม่ให้ออกนอกช่วง"""
    return max(minimum, min(value, maximum))


def calculate_gear(speed):
    """กำหนด Gear ให้สัมพันธ์กับ Speed"""

    if speed < 60:
        return 1
    elif speed < 100:
        return 2
    elif speed < 145:
        return 3
    elif speed < 190:
        return 4
    elif speed < 230:
        return 5
    elif speed < 270:
        return 6
    elif speed < 305:
        return 7
    else:
        return 8


def calculate_rpm(speed, gear):
    """คำนวณ RPM ให้สัมพันธ์กับ Speed และ Gear"""

    gear_ranges = {
        1: (0, 60),
        2: (60, 100),
        3: (100, 145),
        4: (145, 190),
        5: (190, 230),
        6: (230, 270),
        7: (270, 305),
        8: (305, 330),
    }

    low_speed, high_speed = gear_ranges[gear]

    speed_range = high_speed - low_speed

    if speed_range <= 0:
        ratio = 0.0
    else:
        ratio = (
            speed - low_speed
        ) / speed_range

    ratio = clamp(
        ratio,
        0.0,
        1.0
    )

    # RPM จะไล่จากประมาณ 8,500 → 14,500
    rpm = 8500 + (ratio * 6000)

    # noise เล็กน้อย
    rpm += random.uniform(
        -80,
        80
    )

    return int(
        clamp(
            rpm,
            8000,
            15000
        )
    )


# ============================================================
# WAIT FOR GREEN
# ============================================================

async def wait_for_new_green_light(r: redis.Redis):

    print(
        f"🏎️ [{GROUP_ID}] "
        f"Checking Race Status..."
    )

    current_status = await r.get(
        "f1:race:status"
    )

    # ถ้า GREEN ค้างจากรอบก่อน
    # รอ Teacher reset ก่อน
    if current_status == "GREEN":

        print(
            f"⏳ [{GROUP_ID}] "
            f"Waiting for Teacher to RESET "
            f"the race status..."
        )

        while True:

            status = await r.get(
                "f1:race:status"
            )

            if status != "GREEN":
                break

            await asyncio.sleep(0.5)

    print(
        f"🚦 [{GROUP_ID}] "
        f"Ready on Grid! "
        f"Waiting for Teacher's GREEN LIGHT..."
    )

    while True:

        status = await r.get(
            "f1:race:status"
        )

        if status == "GREEN":

            print(
                f"🚦 [{GROUP_ID}] "
                f"LIGHTS OUT AND AWAY WE GO!"
            )

            return

        await asyncio.sleep(0.2)


# ============================================================
# TELEMETRY PRODUCER
# ============================================================

async def produce_f1_telemetry():

    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

    try:

        # ----------------------------------------------------
        # เช็ก Redis
        # ----------------------------------------------------

        await r.ping()

        print(
            f"✅ [{GROUP_ID}] "
            f"Connected to Redis "
            f"{REDIS_HOST}:{REDIS_PORT}"
        )

        # ----------------------------------------------------
        # รอสัญญาณ GREEN
        # ----------------------------------------------------

        await wait_for_new_green_light(r)

        # ----------------------------------------------------
        # สถานะเริ่มต้น
        # ----------------------------------------------------

        # รถเริ่มจาก 0 จริง
        speed_kmh = 0.0

        total_distance_m = 0.0

        engine_temp = 90.0

        tire_wear = 5.0

        last_time = time.monotonic()

        # ความเร็วเป้าหมายเมื่อขึ้นช่วงความเร็วสูง
        target_speed = 326.0

        next_target_change = (
            time.monotonic() + 1.0
        )

        # ====================================================
        # RACE LOOP
        # ====================================================

        while True:

            loop_start = time.monotonic()

            # ------------------------------------------------
            # ถ้าครูหยุด Race ก็หยุดส่ง
            # ------------------------------------------------

            race_status = await r.get(
                "f1:race:status"
            )

            if race_status != "GREEN":

                print(
                    f"🛑 [{GROUP_ID}] "
                    f"Race stopped. "
                    f"Status = {race_status}"
                )

                break

            # ------------------------------------------------
            # คำนวณเวลาจริง
            # ------------------------------------------------

            now = time.monotonic()

            dt = now - last_time

            last_time = now

            # ถ้าเครื่อง lag ไม่ให้ packet เดียว
            # คิดระยะทางกระโดดเยอะเกินไป
            dt = clamp(
                dt,
                0.0,
                0.10
            )

            # =================================================
            # ACCELERATION
            # ====================================================

            # เริ่มจาก 0 และค่อย ๆ เร่ง

            if speed_kmh < 60:

                # 0 → 60
                acceleration_rate = 30.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 120:

                # 60 → 120
                acceleration_rate = 35.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 180:

                # 120 → 180
                acceleration_rate = 32.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 230:

                # 180 → 230
                acceleration_rate = 28.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 270:

                # 230 → 270
                acceleration_rate = 23.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 300:

                # 270 → 300
                acceleration_rate = 18.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            elif speed_kmh < 320:

                # 300 → 320
                acceleration_rate = 12.0

                speed_kmh += (
                    acceleration_rate * dt
                )

            else:

                # =============================================
                # HIGH SPEED
                # =============================================

                # สุ่มเป้าหมายใหม่ทุกประมาณ 0.6–1.2 วินาที
                if now >= next_target_change:

                    target_speed = random.uniform(
                        324.0,
                        329.5
                    )

                    next_target_change = (
                        now
                        + random.uniform(
                            0.6,
                            1.2
                        )
                    )

                # ค่อย ๆ เข้าใกล้ Target
                speed_difference = (
                    target_speed
                    - speed_kmh
                )

                # ไม่ให้ speed กระโดด
                maximum_change = (
                    3.0 * dt
                )

                speed_change = clamp(
                    speed_difference,
                    -maximum_change,
                    maximum_change
                )

                speed_kmh += speed_change

                # สุ่มเล็กมากให้ค่าดูไม่ตายตัว
                speed_kmh += random.uniform(
                    -0.02,
                    0.02
                )

            # =================================================
            # HARD SPEED LIMIT
            # ====================================================

            # ไม่ว่าการคำนวณข้างบนจะออกมาเท่าไร
            # ค่าที่ส่งออกไม่มีทางเกิน 330

            speed_kmh = clamp(
                speed_kmh,
                0.0,
                MAX_SPEED_KMH
            )

            speed_kmh = round(
                speed_kmh,
                1
            )

            # =================================================
            # DISTANCE
            # ====================================================

            # km/h → m/s
            speed_ms = (
                speed_kmh / 3.6
            )

            # Distance = Speed × Time
            distance_delta = (
                speed_ms * dt
            )

            total_distance_m += (
                distance_delta
            )

            # ป้องกันแสดงเกิน 10,000 m
            total_distance_m = min(
                total_distance_m,
                FINISH_DISTANCE
            )

            # =================================================
            # GEAR
            # ====================================================

            gear = calculate_gear(
                speed_kmh
            )

            # =================================================
            # RPM
            # ====================================================

            rpm = calculate_rpm(
                speed_kmh,
                gear
            )

            # =================================================
            # ENGINE TEMPERATURE
            # ====================================================

            # รถเร็วขึ้น → Temp ค่อย ๆ สูงขึ้น
            # ไม่สุ่ม 90 → 125 แบบทันที

            target_engine_temp = (
                90.0
                + (
                    speed_kmh
                    / MAX_SPEED_KMH
                )
                * 20.0
            )

            engine_temp += (
                target_engine_temp
                - engine_temp
            ) * 0.015

            engine_temp += random.uniform(
                -0.02,
                0.02
            )

            engine_temp = clamp(
                engine_temp,
                88.0,
                115.0
            )

            # =================================================
            # TIRE WEAR
            # ====================================================

            # ยางต้องสึกเพิ่มทีละนิด
            # ไม่ควรสุ่ม 5 → 95 → 10

            tire_wear_rate = (
                0.01
                + (
                    speed_kmh
                    / MAX_SPEED_KMH
                )
                * 0.02
            )

            tire_wear += (
                tire_wear_rate * dt
            )

            tire_wear = clamp(
                tire_wear,
                0.0,
                100.0
            )

            # =================================================
            # PAYLOAD
            # ====================================================

            payload = {

                "timestamp":
                    time.time(),

                "speed":
                    round(
                        speed_kmh,
                        1
                    ),

                "engine_temp":
                    round(
                        engine_temp,
                        1
                    ),

                "tire_wear":
                    round(
                        tire_wear,
                        1
                    ),

                "rpm":
                    rpm,

                "gear":
                    gear,

                "distance":
                    round(
                        total_distance_m,
                        2
                    )
            }

            # =================================================
            # SEND REDIS
            # ====================================================

            msg_id = await r.xadd(
                STREAM_KEY,
                payload,
                maxlen=1000,
                approximate=True
            )

            print(
                f"🏎️ [{GROUP_ID}] "
                f"Speed:{speed_kmh:5.1f} km/h | "
                f"Gear:{gear} | "
                f"RPM:{rpm:5d} | "
                f"Temp:{engine_temp:5.1f}°C | "
                f"Tire:{tire_wear:5.1f}% | "
                f"Dist:{total_distance_m:8.1f} m"
            )

            # =================================================
            # FINISH
            # ====================================================

            if total_distance_m >= FINISH_DISTANCE:

                print()

                print(
                    f"🏁🏆 [{GROUP_ID}] "
                    f"CHEQUERED FLAG!"
                )

                print(
                    f"🏁 [{GROUP_ID}] "
                    f"Finished: "
                    f"{total_distance_m:.1f} m"
                )

                await r.publish(
                    "f1:race:finish",
                    json.dumps(
                        {
                            "group_id":
                                GROUP_ID
                        }
                    )
                )

                break

            # =================================================
            # รักษา 20 Hz
            # ====================================================

            processing_time = (
                time.monotonic()
                - loop_start
            )

            remaining_time = (
                SEND_INTERVAL
                - processing_time
            )

            if remaining_time > 0:

                await asyncio.sleep(
                    remaining_time
                )

    except redis.RedisError as e:

        print(
            f"❌ Redis Error: {e}"
        )

    except asyncio.CancelledError:

        print(
            f"🛑 [{GROUP_ID}] "
            f"Race cancelled."
        )

    except Exception as e:

        print(
            f"❌ [{GROUP_ID}] "
            f"Error: {e}"
        )

    finally:

        await r.aclose()

        print(
            f"🔌 [{GROUP_ID}] "
            f"Redis connection closed."
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(
            produce_f1_telemetry()
        )

    except KeyboardInterrupt:

        print(
            f"\n🛑 [{GROUP_ID}] "
            f"Program stopped."
        )