import httpx
import asyncio

global_urls = [
    "http://192.168.6.210:8000",
    "http://192.168.6.210:8001",
    "http://192.168.6.210:8002",
]


async def start(ids):
    async with httpx.AsyncClient() as client:
        # for url in global_urls:
        #     endpoint = f"{url}/start_capture"
        #     print(endpoint)
        #     try:
        #         response = await client.post(endpoint)
        #         print(response.json())
        #     except Exception as e:
        #         print(f"Error with {url}: {e}")
        for id in ids:
            endpoint = f"{global_urls[int(id)-1]}/start_capture"
            print(endpoint)
            try:
                response = await client.post(endpoint)
                print(response.json())
            except Exception as e:
                print(f"Error with {global_urls[int(id)-1]}: {e}")
    return True


async def stop(ids):
    async with httpx.AsyncClient() as client:
        # for url in global_urls:
        #     endpoint = f"{url}/stop_capture"
        #     print(endpoint)
        #     try:
        #         response = await client.post(endpoint)
        #         print(response.json())
        #     except Exception as e:
        #         print(f"Error with {url}: {e}")
        for id in ids:
            endpoint = f"{global_urls[int(id)-1]}/stop_capture"
            print(endpoint)
            try:
                response = await client.post(endpoint)
                print(response.json())
            except Exception as e:
                print(f"Error with {global_urls[int(id)-1]}: {e}")
    return True


# import asks

# asks.init("trio")

# global_urls = [
#     "http://192.168.6.151:8000",
#     "http://192.168.6.152:8000",
#     "http://192.168.6.153:8000",
#     "http://192.168.6.154:8000",
#     "http://192.168.6.155:8000",
# ]


# async def start():
#     global global_urls
#     base_url = global_urls
#     for url in base_url:
#         print(f"{url}/start_capture")
#         response = await asks.post(url)
#         print(response.json())
#     return True


# async def stop():
#     global global_urls
#     base_url = global_urls
#     for url in base_url:
#         print(f"{url}/stop_capture")
#         response = await asks.post(url)
#         print(response.json())
#     return True
