# โจทย์ Asynchronous Task Simulation

import asyncio

async def worker(id: int):
    for i in range(1, 6):
        print(f"Worker-{id} is working round {i}")
        await asyncio.sleep(1)
    print(f"Worker-{id} finished")

async def main():
    tasks = []

    for id in range(1, 4):
        tasks.append(asyncio.create_task(worker(id)))

    await asyncio.gather(*tasks)

asyncio.run(main())
