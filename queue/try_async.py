import asyncio
import sys


async def main():
    print('Hello ...')
    sl = asyncio.sleep(1)
    print('... World!')
    await sl
    print('Nizan')

asyncio.run(main())
