import asyncio
import httpx
import json
URL = "http://localhost:8000/lessons"

async def send_request():
    async with httpx.AsyncClient() as client:
        response = await client.get(url=URL)
        data = json.loads(response.text)
        print(response.status_code, data)
        return data

async def main():
    # Run both requests *at the same time*
    result = await asyncio.gather(
        send_request(),
        send_request()
    )

    print(result)
    assert result[0] != result[1], "Results are the same!"

for i in range(5):
    asyncio.run(main())