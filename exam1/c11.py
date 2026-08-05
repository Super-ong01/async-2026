import asyncio
async def bed_coro():
    print("Starting...")
    asyncio.sleep(1)
    print("Finished...")
async def main():
    await bed_coro()
asyncio.run(main())


