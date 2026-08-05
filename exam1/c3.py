import asyncio
async def woeker(n):
    await asyncio.sleep(0.5)
    return n*10
async def main():
    tasks = [asyncio.create_task(woeker(i)) for i in range(1,4)]
    for t in tasks:
        res = await t
        print(res,end=" ")
asyncio.run(main())