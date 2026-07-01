import asyncio
from time import ctime, time

# Greeting Async
async def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# Take Order
async def take_orders(customer):
    print(f"{ctime()} Taking Order for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Taking Order for Customer-{customer} ...Done!")

# Do Cooking
async def do_cooking(customer):
    print(f"{ctime()} Cooking for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Cooking for Customer-{customer} ...Done!")

# Mini Bar
async def mini_bar(customer):
    print(f"{ctime()} Mini Bar for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Mini Bar for Customer-{customer} ...Done!")

async def serve_customer(customer):
    await take_orders(customer)
    await do_cooking(customer)
    await mini_bar(customer)
    print(f"{ctime()} Customer-{customer} All served!")

async def main():
    customers = ['A', 'B', 'C']

    start_time = time()

    # Greeting ทีละคนก่อน
    for customer in customers:
        await greet_diners(customer)

    print(f"{ctime()} --- All customers greeted. Scheduling Async Tasks! ---")

    # ให้ A, B, C ทำงานพร้อมกัน
    tasks = []

    for customer in customers:
        task = asyncio.create_task(serve_customer(customer))
        tasks.append(task)

    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} Finished Restaurant Operation in {duration:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
# from time import sleep, ctime, time

# # Greeting Synchronous
# def greet_diners(customer):
#     print(f"{ctime()} Greeting for Customer-{customer} ...")
#     sleep(1)
#     print(f"{ctime()} Greeting for Customer-{customer} ...Done!")

# # Take Order
# def take_orders(customer):
#     print(f"{ctime()} Taking Order for Customer-{customer} ...")
#     sleep(1)
#     print(f"{ctime()} Taking Order for Customer-{customer} ...Done!")

# # Do Cooking
# def do_cooking(customer):
#     print(f"{ctime()} Cooking for Customer-{customer} ...")
#     sleep(1)
#     print(f"{ctime()} Cooking for Customer-{customer} ...Done!")

# # Do Cooking
# def mini_bar(customer):
#     print(f"{ctime()} Mini Bar for Customer-{customer} ...")
#     sleep(1)
#     print(f"{ctime()} Mini Bar for Customer-{customer} ...Done!")

# if __name__ == "__main__":
#     # Begin of main thread
#     customers = ['A', 'B', 'C']

#     start_time = time()

#     # Cooking for each customer
#     for customer in customers:
#         greet_diners(customer)
#         take_orders(customer)
#         do_cooking(customer)
#         mini_bar(customer)

#     duration = time() - start_time

#     print(f"{ctime()} Finished Cooking in {duration} seconds")