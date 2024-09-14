import aiohttp

urls = []


async def start_or_stop(status):
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.post(url + status) as response:
                data = await response.json()
                print(data)
