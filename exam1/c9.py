import asyncio
async def compute():
    return 42
async def main():
    task = asyncio.create_task(compute())
    task.result()
    res = task.result()  # This will raise an exception because the task is not done yet
    print(res)
asyncio.run(main())