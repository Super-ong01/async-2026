import asyncio
async def my_coro():
    print("A")
    await asyncio.sleep(1)