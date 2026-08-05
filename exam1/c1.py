async def computer(val):
    return val * 2
async def main():
    coro = computer(10)
    res = await coro
    print(res)

asyncio.run(main())