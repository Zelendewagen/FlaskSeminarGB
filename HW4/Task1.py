# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле,
# название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения
# и общем времени выполнения программы.

import time
import threading
from multiprocessing import Process
import asyncio
import aiohttp
import requests

urls = ['https://upload.wikimedia.org/wikipedia/commons/1/1b/De_Campos.JPG',
        'https://upload.wikimedia.org/wikipedia/commons/a/ae/AfricanWildCat.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/3/38/Gata_Bengal%C3%AD_Hembra_Brown_Spotted.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Savannah_Cat_closeup.jpg/1920px-Savannah_Cat_closeup.jpg']


def __thr_start(url, stime):
    name = 'THREADS_' + url.split('/')[-1]
    response = requests.get(url)
    with open(name, 'wb') as f:
        f.write(response.content)
    print(f'{name} - {time.time() - stime:.2f} sec')


def thr(addresses):
    start_time = time.time()
    threads = []
    for url in addresses:
        t = threading.Thread(target=__thr_start, args=(url, start_time))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print(f'Многопоточный: {time.time() - start_time:.2f} sec')


def __multiproc_start(url, stime):
    name = 'MULTIPROC_' + url.split('/')[-1]
    response = requests.get(url)
    with open(name, 'wb') as f:
        f.write(response.content)

    print(f'{name} - {time.time() - stime:.2f} sec')


def multiproc(addresses):
    start_time = time.time()
    processes = []
    if __name__ == '__main__':
        for url in addresses:
            process = Process(target=__multiproc_start, args=(url, start_time))
            processes.append(process)
            process.start()

        for p in processes:
            p.join()
    print(f'Многопроцессорный: {time.time() - start_time:.2f} sec')


async def __async_start(url, stime):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            name = 'ASYNC_' + url.split('/')[-1]
        with open(name, "wb") as f:
            f.write(response.read())
        print(f'{name} - {time.time() - stime:.2f} sec')


async def asc():
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(__async_start(url, start_time))
        tasks.append(task)
    await asyncio.gather(*tasks)


thr(urls)

multiproc(urls)

if __name__ == '__main__':
    asyncio.run(asc())
