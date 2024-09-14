import aiohttp, asyncio, os, time

i = 0
image_name = []

base_url = [
    "http://192.168.6.156:8000/",
    "http://192.168.6.155:8000/",
    "http://192.168.6.163:8000/",
    "http://192.168.6.158:8000/",
    "http://192.168.6.159:8000/",
    "http://192.168.6.165:8000/",
    "http://192.168.6.161:8000/",
    "http://192.168.6.160:8000/",
]


async def fetch_images(url, status):

    async with aiohttp.ClientSession() as session:
        async with session.post(url + str(status)) as response:
            if response.status == 200:
                data = await response.json()
                result = data.get("message")
                print(url, result)


async def main_loop(status):
    try:
        tasks = [fetch_images(link, status) for link in base_url]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(e)


asyncio.run(main_loop("stop_capture"))
