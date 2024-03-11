import json
import time
import asyncio
from aiohttp import ClientSession
import aiohttp
import aiofiles

async def PostData(url:str,name:str = 'unnamed')->str:
    data = {
        'style': 'art',
        'noise': '2',
        'x2': '1',
        'file_name': 'small.jpg',
        'input': url
    }

    r = aiohttp.request("POST","https://bigjpg.com/api/task/",headers={'X-API-KEY': '0eecf287a8ec40fa9d052c38c9f46bdd'},data=json.dumps(data))
    rc = await r._coro
    rcStr = await rc.text()
    print(rcStr)
    rcDict = json.loads(rcStr)
    print("DATA "+rcDict["tid"])
    return rcDict["tid"]
    
async def GetData(taskId:str):
    print(taskId)
    while True:
        r = aiohttp.request("GET","https://bigjpg.com/api/task/"+taskId)
        rc = await r._coro
        rcStr = await rc.text()
        rcDict = json.loads(rcStr)[taskId]
        print(rcDict)
        print("\n")
        if(rcDict["url"]==""):
            await asyncio.sleep(1)
        else:
            print("Yeeehooo: data is " + rcDict["url"])
            return rcDict["url"]

async def ConvertImage(url:str,name:str="unnamed"):
    r = asyncio.create_task(PostData(url,name))
    await r
    numberStr = r.result()
    r = asyncio.create_task(GetData(r.result()))
    await r
    url = r.result()
    print("Our url:"+url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if(resp.status == 200):
                async with aiofiles.open("images/"+numberStr+".jpg","x") as f:
                    await f.close()
                async with aiofiles.open("images/"+numberStr+".jpg","wb") as f:
                    await f.write(await resp.read())
                    await f.close()
    #r = await GetData(r)

async def main():
    imagesUrls = ["https://ioflood.com/blog/wp-content/uploads/2023/08/Image-depicting-JSON-data-being-loaded-and-parsed-in-Python-using-jsonloads-300x300.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHH8mepO4avVq5NJFuruMoqN02xAqm5Jk7IryH9iVuNw&s","https://i.pinimg.com/736x/3a/8f/4c/3a8f4cb12ebfcd658cb73db7a4112651.jpg"]
    tasks:list[asyncio.Task] = []
    for url in imagesUrls:
        tasks.append(asyncio.create_task(ConvertImage(url)))
    for task in tasks:
        await task
    

asyncio.run(main())