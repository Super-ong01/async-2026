# Program 1: The First Coroutine Function
# Concept: Understanding async def and how it differs from a normal function.
import asyncio

async def greet():
    print("Hello from Coroutine!")
print(type(greet))


# from time import ctime, time


# CUSTOMERS = ("A", "B", "C")


# def log(message):
#     print(f"{ctime()} {message}")


# async def greet_customer(customer):
#     log(f"Greeting for Customer-{customer} ...")
#     await asyncio.sleep(1)
#     log(f"Greeting for Customer-{customer} ...Done!")


# async def serve_customer(customer):
#     task_name = f"Task-{customer}"

#     log(f"[{task_name}] Taking Order ...")
#     await asyncio.sleep(1)
#     log(f"[{task_name}] Taking Order ...Done!")

#     log(f"[{task_name}] Cooking Spaghetti ...")
#     await asyncio.sleep(1)
#     log(f"[{task_name}] Cooking Spaghetti ...Done!")

#     log(f"[{task_name}] Manage Bar for Drink ...")
#     await asyncio.sleep(1)
#     log(f"[{task_name}] Manage Bar for Drink ...Done!")

#     log(f"[{task_name}] All served!")


# async def main():
#     start_time = time()

#     for customer in CUSTOMERS:
#         await greet_customer(customer)

#     print()
#     log("--- All customers greeted. Scheduling independent Async Tasks! ---")
#     print()

#     tasks = [
#         asyncio.create_task(serve_customer(customer), name=f"Task-{customer}")
#         for customer in CUSTOMERS
#     ]

#     await asyncio.gather(*tasks)

#     print()
#     log(f"Finished Entire Restaurant Operation in {time() - start_time:.2f} seconds.")


# if __name__ == "__main__":
#     asyncio.run(main())
