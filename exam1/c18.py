import asyncio
@app.get("/sync-blocking")
async def blocking_endpoint():
    time.sleep(10)
    return {"message": "Done"}
