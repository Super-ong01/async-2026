# ให้เขียนโปรแกรมหาจำนวนเฉพาะที่ ≤ n แบบ อะซิงโครนัส
# โปรแกรมต้องรองรับการคำนวณ หลายค่า n พร้อมกัน
# นักศึกษาต้องเติมโค้ดที่ทำการ หาจำนวนเฉพาะ และ สร้าง task

import asyncio
from typing import List

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

async def primes_up_to(n: int) -> List[int]:
    await asyncio.sleep(0)
    return [x for x in range(2, n + 1) if is_prime(x)]

async def main():
    ns = [10, 20, 30]
    tasks = []

    for n in ns:
        tasks.append(asyncio.create_task(primes_up_to(n)))

    for n, task in zip(ns, tasks):
        result = await task
        print(f"Primes <= {n}: {result}")

asyncio.run(main())
