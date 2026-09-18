import asyncio

async def test():
    timeout = asyncio.timeout(90)
    print(type(timeout))

asyncio.run(test())