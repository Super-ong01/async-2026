import asyncio
async def long_running_task():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Cleaning up...")
        await asyncio.sleep(1)
        print("Cleanup done")
async def main():
    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(0.1)
    task.cancel()
    await task
asyncio.run(main())