# Program 5: Sequential Execution (The Wrong Way)
# Concept: Showing that simply awaiting one after another is still sequential (Synchronous behavior).
# Program 5: Sequential Execution (The Wrong Way)
# Concept: Showing that simply awaiting one after another is still sequential (Synchronous behavior).

import asyncio
from time import time,ctime

async def serve_customer(name):
    print(f"{ctime()} | Serving customer: {name}")
    await asyncio.sleep(1)  # Simulate time taken to serve customer
    print(f"{ctime()} | Finished serving customer: {name}")

async def main():
    start = time()
    
    await serve_customer("Alice")
    await serve_customer("Bob")
    
    print(f"Total Time: {time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # Run the main coroutine using the event loop